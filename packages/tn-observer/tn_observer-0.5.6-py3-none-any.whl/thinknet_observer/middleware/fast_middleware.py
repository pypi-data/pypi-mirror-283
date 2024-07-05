import time

from fastapi import Request, HTTPException
from starlette.responses import Response
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware

from ..loggers.loggers import TNAccessLogger, TNLogger, UnExpectedError
from ..metrics.metrics import PrometheusMiddleware
from ..utils.http import HttpContext

from . import get_resource_info


class FastObserverMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, resource, is_multiprocessing: bool=False, excluded_urls:list=[] ) -> None:
        super().__init__(app)
        self._resource = resource
        self._is_multiprocessing = is_multiprocessing
        self._excluded_urls = excluded_urls
        
        self._access_log = TNAccessLogger(self._resource)
        # self._setup_metrics(app)


    def _setup_metrics (self, app,):
        namespace, service_name = get_resource_info(self._resource)

        self._metrics = PrometheusMiddleware(app, namespace, service_name, 
                                            is_multiprocessing=self._is_multiprocessing)
        self._metrics.add_exclude(self._excluded_urls)
        self._metrics.register_fastapi_metrics()
    

    async def dispatch(self, request: Request, call_next) -> Response: 
        tick = time.time()
        response = await call_next(request)
        duration = time.time() - tick

        http_context = HttpContext(request.method, request.scope.get("path", request.url.path), request.headers.get('referer', ""),
                                request.client.host, duration, request.headers.get('user-agent',""),
                                request.app.routes, response.status_code )
        
        self._access_log.logging(http_context)
        # self._metrics.add_fastapi_metrics(http_context)
        
        return response
        
        