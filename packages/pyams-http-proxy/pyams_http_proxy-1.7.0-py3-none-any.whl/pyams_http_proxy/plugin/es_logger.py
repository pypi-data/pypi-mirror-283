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

"""PyAMS_http_proxy.plugin.es_logger module

A plug-in used to log proxy requests to an Elasticsearch index.

You must install the *elasticsearch* package in your dependencies for
this plug-in to work!

Plug-in specific configuration:
 - es_servers: array of Elasticsearch connections
 - verify_certs: flag to specify if SSL certificates should be used; True by default
 - ca_certs: optional path to CA bundle
 - client_cert: path to the file containing the private key and the certificate, or cert
   only if using client key
 - client_key: path to the file containing the private key if using separate cert and key files
 - timeout: Elasticsearch query timeout
 - retry_on_timeout: flag to specify if ES request should be retried on timeout; False
   by default
 - max_retries: maximum number of request retries, if enabled
 - es_index: name of Elasticsearch index; name may be compatible with date's "strftime"
   function
 - expressions: list of Python expressions which should be applied on data before indexing
 - properties: object with additional properties
"""

__docformat__ = 'restructuredtext'

import json
import uuid
from datetime import date, datetime
from json import JSONDecodeError

from elasticsearch import AsyncElasticsearch, TransportError
from starlette.responses import JSONResponse, Response

from pyams_http_proxy.plugin import ProxyPlugin
from pyams_http_proxy.proxy import LOGGER, ProxyApplication


class ElasticLogger(ProxyPlugin):
    """A proxy plugin used to log JSON body in Elasticsearch"""

    config_name = 'es_logger'

    @staticmethod
    def init_plugin():
        """Plugin global initialization"""
        LOGGER.info("Loaded Elasticsearch body logger")

    @staticmethod
    def init_proxy(base_path, settings):
        """Plugin base path initialization"""
        LOGGER.info("Elasticsearch logger init: %s (%s)", base_path, settings)

    @staticmethod
    async def pre_handler(request, config):  # pylint: disable=unused-argument
        """Logger pre-handler"""
        try:
            request.state.payload = await request.json()
        except JSONDecodeError:
            request.state.payload = {}
        return request

    @staticmethod
    async def post_handler(request, response, config):
        """Logger post-handler"""
        payload = request.state.payload
        try:
            if isinstance(response, Response):
                result = json.loads(response.body)
            else:
                result = ''
                async for chunk in response.aiter_text():
                    result += chunk
                result = json.loads(result)
        except JSONDecodeError:
            result = {
                "status": "error",
                "message": "Proxy JSON decoding error"
            }
        api_key = config.get('api_key')
        api_key = api_key.split(':', 1) if api_key else None
        basic_auth = config.get('basic_auth')
        basic_auth = basic_auth.split(':', 1) if basic_auth else None
        client = AsyncElasticsearch(config['es_servers'],
                                    cloud_id=config.get('cloud_id', None),
                                    api_key=api_key,
                                    basic_auth=basic_auth,
                                    bearer_auth=config.get('bearer_auth', None),
                                    verify_certs=config.get('verify_certs', True),
                                    ca_certs=config.get('ca_certs', None),
                                    client_cert=config.get('client_cert', None),
                                    client_key=config.get('client_key', None),
                                    request_timeout=config.get('timeout', 10.0),
                                    retry_on_timeout=config.get('retry_on_timeout', False),
                                    max_retries=config.get('max_retries', 0))
        try:
            index = date.today().strftime(config['es_index'])
            # update payload before indexing
            expressions = config.get('expressions')
            if expressions:
                for expr in expressions:
                    try:
                        eval(expr, {}, {'payload': payload})
                    except (SyntaxError, ValueError, TypeError, AttributeError):
                        pass
            data = {
                '@timestamp': datetime.utcnow(),
                'request': {
                    'method': request.method,
                    'scheme': request.url.scheme,
                    'host': request.url.netloc,
                    'path': request.url.path,
                    'headers': dict(ProxyApplication.get_headers(request, decode=True)),
                    'params': dict(ProxyApplication.get_params(request, decode=True)),
                    'payload': json.dumps(payload)
                },
                'response': {
                    'status_code': response.status_code,
                    'headers': dict(ProxyApplication.get_headers(response, decode=True)),
                    'payload': json.dumps(result)
                },
                'properties': config.get('properties')
            }
            if not isinstance(response, Response):
                # can't get URL info for newly crafted responses!!
                data['response'].update({
                    'scheme': response.url.scheme,
                    'host': response.url.netloc.decode(),
                    'path': response.url.path
                })
            try:
                await client.index(index=index,
                                   id=uuid.uuid4(),
                                   body=data)
            except TransportError:
                LOGGER.exception("Elasticsearch exception")
        finally:
            await client.close()
        return JSONResponse(result, status_code=response.status_code)
