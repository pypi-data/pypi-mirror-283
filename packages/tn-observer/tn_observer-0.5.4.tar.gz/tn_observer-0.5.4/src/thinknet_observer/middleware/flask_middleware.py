import time

from flask import request, Response

from ..metrics.metrics import PrometheusMiddleware
from ..utils.http import HttpContext
from ..loggers.loggers import TNAccessLogger

from . import get_resource_info
        

class FlaskObserverMiddleware:

    def __init__(self, app, resource=None, is_multiprocessing: bool=False, excluded_urls:list=[]) -> None:
        self._is_multiprocessing = is_multiprocessing
        self._excluded_urls = excluded_urls
        self._resource = resource

        if app is not None:
            self.init_app(app)


    def _setup_metrics (self, app,):
        namespace, service_name = get_resource_info(self._resource)

        self._metrics = PrometheusMiddleware(app, namespace, service_name, 
                                            is_multiprocessing=self._is_multiprocessing)
        self._metrics.add_exclude(self._excluded_urls)
        self._metrics.register_flask_metrics()


    def init_app(self, app, ):
        self.app = app
        self._request = request

        self._setup_metrics(app)
        self._access_log = TNAccessLogger(self._resource)

        self.app.before_request(self._before_request)
        self.app.after_request(self._after_response)


    def _before_request(self,):
        self.tick = time.time()


    def _after_response(self, response: Response):
        duration  = time.time() - self.tick

        http_context = HttpContext(self._request.method, self._request.path, self._request.referrer, 
                                self._request.remote_addr, duration, self._request.user_agent, 
                                self._request.url_rule, response.status_code)
        
        self._access_log.logging(http_context)
        self._metrics.add_flask_metrics(http_context)
        
        
        return response
