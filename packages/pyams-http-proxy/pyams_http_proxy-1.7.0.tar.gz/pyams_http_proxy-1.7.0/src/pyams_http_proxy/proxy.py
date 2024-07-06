#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_http_proxy.proxy module

This module defines the main proxy application.
"""

__docformat__ = 'restructuredtext'

import importlib
import json
import logging
import os
import re
from urllib.parse import urlsplit

import httpx
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse


LOGGER = logging.getLogger('PyAMS (proxy)')

EXTENSION_PATH = re.compile(r'(?P<base>.*)'
                            r'/\+\+(?P<ext>[a-z]+)\+\+'
                            r'(?P<path>/.+)', re.VERBOSE)


class ProxyApplication(Starlette):
    """Starlette proxy handler"""

    @classmethod
    async def create(cls, config):
        """Application factory"""
        app = cls(config)
        return app

    def __init__(self, config):
        super().__init__()
        self.config = config
        # initialize plugins
        plugins = self.plugins = self.init_plugins(config)
        # initialize remotes
        self.remotes = self.init_remotes(config, plugins)
        # initialize HTTP client
        self.client = httpx.AsyncClient(verify=config.get('ssl_certificates', None),
                                        follow_redirects=False)

    @classmethod
    def init_plugins(cls, config):
        """Initialize plugins"""
        plugins = {}
        for key, names in config['plugins'].items():
            pkg, klass = names.split()
            try:
                module = importlib.import_module(pkg)
                plugin = plugins[key] = getattr(module, klass)
                plugin.init_plugin()
            except ImportError:
                LOGGER.warning("Can't import plug-in package: %s", pkg)
            except AttributeError:
                LOGGER.warning("Can't load plug-in: %s", klass)
        return plugins

    @classmethod
    def init_remotes(cls, config, plugins):
        """Initialize remote configurations"""
        remotes = {}
        for base_path, settings in config.get('remotes', {}).items():
            remotes[base_path] = cls.init_remote(base_path, settings, plugins)
        cls.init_includes(remotes, config, plugins)
        return remotes

    @classmethod
    def init_includes(cls, remotes, config, plugins):
        """Initialize includes"""
        for item in config.get('includes'):
            if os.path.isdir(item):
                for path, dirnames, filenames in os.walk('item'):
                    for filename in filenames:
                        cls.init_config(remotes, os.path.join(path, filename), plugins)
            elif os.path.isfile(item):
                cls.init_config(remotes, item, plugins)

    @classmethod
    def init_config(cls, remotes, path, plugins):
        """Initialize configuration from included file"""
        with open(path, 'r') as config_file:
            for base_path, settings in json.load(config_file).items():
                remotes[base_path] = cls.init_remote(base_path, settings, plugins)

    @classmethod
    def init_remote(cls, base_path, settings, plugins):
        """Initialize remote configuration"""
        remote = {
            'remote': settings['remote'],
            'config': settings.get('config', {}),
            'timeout': settings.get('timeout', 5.0) or None
        }
        for plugin_name in settings.get('plugins', ''):
            plugin = plugins.get(plugin_name)
            if plugin is not None:
                plugin.init_proxy(base_path, settings)
                remote.setdefault('plugins', []).append(plugin)
        return remote

    async def __call__(self, scope, receive, send):
        """Async proxy call"""
        if scope['type'] == 'http':
            request = Request(scope, receive=receive)
            config, remote = self.get_config(request)
            plugins_config = config.get('config', {})
            for plugin in config.get('plugins', ()):
                if hasattr(plugin, 'pre_handler') and \
                        plugin.apply_to(request, plugins_config[plugin.config_name]):
                    request = await plugin.pre_handler(request,
                                                       plugins_config[plugin.config_name])

            # remote = config.get('remote')
            if not remote:
                response = Response()
                for plugin in config.get('plugins', ()):
                    if hasattr(plugin, 'post_handler') and \
                            plugin.apply_to(request, plugins_config[plugin.config_name]):
                        response = await plugin.post_handler(request, response,
                                                             plugins_config[plugin.config_name])
                await response(scope, receive, send)

            else:
                async with self.client.stream(method=self.get_method(request),
                                              url=remote,
                                              headers=self.get_headers(request),
                                              params=self.get_params(request),
                                              data=self.get_body(request),
                                              timeout=config.get('timeout')) as response:
                    for plugin in config.get('plugins', ()):
                        if hasattr(plugin, 'post_handler') and \
                                plugin.apply_to(request, plugins_config[plugin.config_name]):
                            response = await plugin.post_handler(request, response,
                                                                 plugins_config[plugin.config_name])
                    if isinstance(response, Response):
                        app = response
                    else:
                        app = StreamingResponse(status_code=response.status_code,
                                                headers=response.headers,
                                                content=response.aiter_raw())
                    await app(scope, receive, send)

        elif scope['type'] == 'lifespan':
            message = await receive()
            assert message['type'] == 'lifespan.startup'

            async with self.client:
                await send({'type': 'lifespan.startup.complete'})
                message = await receive()

            assert message['type'] == 'lifespan.complete'
            await send({'type': 'lifespan.shutdown.complete'})

    def get_config(self, request):
        """Request config getter"""
        path = request.url.path[1:]
        path_elements = path.split('/')
        try:
            context = path_elements[0]
            match = EXTENSION_PATH.match(path)
            if match:  # path with '++ext++' element
                base, ext, ext_path = match.groups()
                config = self.remotes['{}-{}'.format(context, ext)]
                target = self.get_url(request, config.get('remote'), ext_path)
            else:
                config = self.remotes[context]
                target = self.get_url(request, config.get('remote'))
            return config, target
        except KeyError as exc:
            raise HTTPException(404) from exc

    @staticmethod
    def get_method(request):
        """Request method getter"""
        return request.method

    @staticmethod
    def get_url(request, remote, path=None):
        """Request remote URL getter"""
        if not remote:
            return None
        components = urlsplit(remote)
        if not path:
            path = request.url.path[1:]
        if isinstance(path, str):
            path = path.split('/')
        return str(request.url.replace(scheme=components.scheme,
                                       netloc=components.netloc,
                                       path='/{}'.format('/'.join(path[1:]))))

    @staticmethod
    def get_headers(source, decode=False):
        """Request headers getter"""
        state = getattr(source, 'state', None)
        headers = None
        if state is not None:
            headers = getattr(source.state, 'headers', None)
        if headers:
            headers = list(headers.items())
        else:
            headers = source.headers.raw
        if decode:
            return [
                (key.decode() if isinstance(key, bytes) else key,
                 value.decode() if isinstance(value, bytes) else value)
                for key, value in headers
                if key not in ('host', b'host')
            ]
        return [
            (key, value)
            for key, value in headers
            if key not in ('host', b'host')
        ]

    @staticmethod
    def get_params(request, decode=False):
        """Request params getter"""
        if decode:
            return [
                (key.decode() if isinstance(key, bytes) else key,
                 value.decode() if isinstance(value, bytes) else value)
                for key, value in request.query_params.items()
            ]
        return [
            (key, value)
            for key, value in request.query_params.items()
        ]

    @staticmethod
    def get_body(request):
        """Request body getter"""
        if 'content-length' in request.headers or 'transfer-encoding' in request.headers:
            return request.stream()
        return None
