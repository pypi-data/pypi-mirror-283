import time
import re, os

from flask import Flask
from flask import request as flask_request

from fastapi import FastAPI
from fastapi import Request as fastapi_request
from fastapi.middleware.wsgi import WSGIMiddleware

from prometheus_client import Counter, Histogram, Summary, Info
from prometheus_client import make_wsgi_app
from prometheus_client import REGISTRY as PROMETHEUS_REGISTRY
from prometheus_client import (
    CollectorRegistry,
    generate_latest,
    multiprocess,
    CONTENT_TYPE_LATEST,
)

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .fastapi_metrics_redirect import MetricsRedirect
from ..utils.singleton import SingletonMeta
from ..utils.bcolor import Bcolors
from ..utils.gunicorn_multiprocess import clear_multiproc_dir
from ..utils.http import HttpContext

from .config import (
    _DEFAULT_BUCKETS,
    _DEFAULT_LABELS,
    NAMESPACE,
    SERVICENAME,
    EXCLUDE_URLS,
    SECONDTOMS
)


class PrometheusMiddleware(metaclass=SingletonMeta):

    namespace = NAMESPACE
    service_name = SERVICENAME

    _DEFAULT_BUCKETS = _DEFAULT_BUCKETS

    METRICS_REQUEST_LATENCY_HISTOGRAM = Histogram(
        "http_server_duration_milliseconds",
        "Duration of HTTP requests in ms (Histogram)",
        labelnames=_DEFAULT_LABELS,
        buckets=_DEFAULT_BUCKETS,
    )

    METRICS_REQUEST_LATENCY_SUMMARY = Summary(
        "http_server_duration_milliseconds_summary",
        "Duration of HTTP requests in ms (Summary)",
        labelnames=_DEFAULT_LABELS,
    )

    METRICS_REQUEST_COUNT = Counter(
        "http_requests_total",
        "Number of HTTP requests",
        labelnames=_DEFAULT_LABELS,
    )

    METRICS_INFO = Info("app_version", "Application Version")

    def __init__(
        self,
        app,
        namespace: str = None,
        service_name: str = None,
        app_version: str = None,
        is_multiprocessing: bool = False,
    ):
        """
        :param app: web application framework can be either 'Flask' or 'fastapi' instance.
        :type app: 'astapi.applications.FastAPI' or 'flask.app.Flask'

        :param namespace: can be use to override namespace that read from .env
        :type namespace: str

        :param service_name: can be use to override service_name that read from .env
        :type service_name: str

        :param app_version: optional param can be use for track version of the application
        :type app_version: str
        """
        self.app = app
        self.exclude_list = [
            {"route": "/metrics/"},
            {"route": "/metrics"},
            {"route": "/metrics/{path}"},
        ]
        self._is_registered = False
        self.is_multiprocessing = is_multiprocessing
        if app_version:
            self.METRICS_INFO.info({"version": app_version})

        if namespace:
            self.namespace = namespace
        if service_name:
            self.service_name = service_name

        self._add_exclude_route_env()
        self._check_env(self.namespace, self.service_name)
        

    @staticmethod
    def _check_invalid_exclude_format(list_input):
        """
        raise an error when invalid exclude format is found.
        """
        tuple_keys = ("method", "route", "status_code")
        for idx, val in reversed(list(enumerate(list_input))):
            if not isinstance(val, dict):
                error_msg = f"{Bcolors.FAIL}ERROR : Invalid exclude found : '{val}' is not valid exclude format. exclude must be instance of dict(){Bcolors.ENDC}"
                list_input.pop(idx)
                raise TypeError(error_msg)
            elif not any(key in val.keys() for key in tuple_keys):
                error_msg = f'{Bcolors.FAIL}ERROR : Invalid exclude found : \'{val}\' is not valid exclude format. exclude must contain atleast 1 key from this list ["method","route","status_code"]{Bcolors.ENDC}'
                list_input.pop(idx)
                raise ValueError(error_msg)
            elif "route" in val.keys():
                if val["route"][0] != "/":
                    warning_msg = f"{Bcolors.WARNING}WARNING : exclude {val} route's value is not start with '/'. This exclude will likely to be ignored{Bcolors.ENDC}"
                    print(warning_msg)
        return list_input
    

    def _add_exclude_route_env(self,):
        str_exclude_url = EXCLUDE_URLS
        list_exclude_env = []

        if len(str_exclude_url) != 0:
            split_exclude_url = str_exclude_url.split(",")
            for url in split_exclude_url:
                list_exclude_env.append({'route': f"/{url}"})

        self.add_exclude(list_exclude_env)



    def _check_env(self, namespace, service_name):
        print (namespace)
        if namespace == "UNDEFINED" or namespace is None:
            print(
                f"{Bcolors.WARNING}WARNING: env variable : for label 'namespace' is not found.\nPlease provide SERVICE_NAME_PREFIX in .env file{Bcolors.ENDC}"
            )
        if service_name == "UNDEFINED" or service_name is None:
            print(
                f"{Bcolors.WARNING}WARNING: env variable : for label 'serviceName' is not found.\nPlease provide SERVICE_NAME in .env file{Bcolors.ENDC}"
            )

    def clear_default_metrics(self):
        """
        Clear all observed default metrics.
        Generally being use in testing only.
        """
        for default_metric in self.default_metrics:
            default_metric.clear()

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, new_app):
        if isinstance(new_app, Flask):
            self._app = new_app
            self.request = flask_request
        elif isinstance(new_app, FastAPI):
            self._app = new_app
            self.request = fastapi_request
        else:
            raise TypeError("app type have to be etiher 'Flask' or 'fastapi'.")

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request_class):
        self._request = request_class

    @property
    def exclude_list(self):
        return self._exclude_list

    @exclude_list.setter
    def exclude_list(self, value: list):
        if isinstance(value, list):
            value = self._check_invalid_exclude_format(value)
            self._exclude_list = value
        else:
            raise TypeError("Invalid PrometheusMiddleware.exclude format")

    @property
    def default_metrics(self):
        """
        return a list of default metrics.
        """
        list_default_metrics = [
            self.METRICS_INFO,
            self.METRICS_REQUEST_LATENCY_HISTOGRAM,
            self.METRICS_REQUEST_LATENCY_SUMMARY,
            self.METRICS_REQUEST_COUNT,
        ]
        return list_default_metrics

    @property
    def default_exclude_list(self):
        return [{"route": "/metrics/"}, {"route": "/metrics"}]

    @property
    def PROMETHEUS_REGISTRY(self):
        """
        return REGISTRY object from prometheus client
        PROMETHEUS_REGISTRY can be use to access colleted metric
        Ex.
        PROMETHEUS_REGISTRY.get_sample_value(
        "http_request_duration_ht_ms_sum",
        labels={"http_status": "200", "method": "get", "route": "/sleep"},
        )
        this will retrieve data from "http_request_duration_ht_ms_sumq"
        """
        return PROMETHEUS_REGISTRY

    def add_exclude(self, added_exclude: list):
        """
        :param added_exclude: list of dict that contain atleast 1 key from this list ["method","route","status_code"]
        :type added_exclude: list(dict())

        Ex . [{"route":"/index"}] will exclude all metrics from route /index

        Ex . [{"route":"/index","status_code":"200"}] will exclude all metrics from route="/index" with status_code="200" (if error still collect metric)
        """
        list_buffer = self.exclude_list
        list_buffer.extend(added_exclude)
        self.exclude_list = list_buffer

    def is_exclude(self, method, route, status_code):
        """
        :param method: method of the endpoint
        :type method: str

        :param route: route of the endpoint
        :type route: str

        :param status_code: returned status of the request
        :type status_code: str
        """
        if not self.exclude_list:
            return False

        for exclude_item in self.exclude_list:
            cond_method = (
                True
                if exclude_item.get("method") is None
                else (exclude_item.get("method").lower() == method.lower())
            )
            cond_route = (
                True
                if exclude_item.get("route") is None
                else (exclude_item.get("route") == route)
            )
            cond_status_code = (
                True
                if exclude_item.get("status_code") is None
                else (exclude_item.get("status_code") == status_code)
            )

            if cond_method and cond_route and cond_status_code:
                return True

        return False
    
    
    @staticmethod
    def _app_multiprocess(environ, start_response):
        environ["PATH_INFO"] = "/metrics"
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)

        status = "200 OK"
        response_headers = [
                        ("Content-type", CONTENT_TYPE_LATEST),
                        ("Content-Length", str(len(data))),
                    ]
        start_response(status, response_headers)
        return iter([data])
    

    @staticmethod
    def _make_wsgi_multiprocess_app():
        return PrometheusMiddleware._app_multiprocess


    def register_flask_metrics(self, ):
        self._is_registered = True

        if self.is_multiprocessing:
            clear_multiproc_dir()

            self.app.wsgi_app = DispatcherMiddleware(
                self.app.wsgi_app, {"/metrics": PrometheusMiddleware._make_wsgi_multiprocess_app()}
            )
        else:
            self.app.wsgi_app = self.app.wsgi_app = DispatcherMiddleware(
                self.app.wsgi_app, {"/metrics": make_wsgi_app()}
            )


    def add_metrics(self, method, url, status_code, duration):
        if not self.is_exclude(method, url, status_code):
            request_latency = int(duration) * SECONDTOMS

            self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                method,
                url,
                status_code,
                self.service_name,
                self.namespace,
            ).observe(request_latency)

            self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                method,
                url,
                status_code,
                self.service_name,
                self.namespace,
            ).observe(request_latency)

            self.METRICS_REQUEST_COUNT.labels(
                method,
                url,
                status_code,
                self.service_name,
                self.namespace,
            ).inc()
    
        
    def add_flask_metrics( self,  http_context: HttpContext):
        method = http_context.method
        url = http_context.url
        status_code = http_context.status_code
        duration = http_context.duration

        url_rule = (url.rule if url else http_context.route)

        self.add_metrics(method, url_rule, status_code, duration)


    def before_request(self):
        """
        Get start time of a request.
        This method get will call before a request processed.
        """
        self.request._tick= time.time()


    @staticmethod
    def get_path_format(app_routes, path):
        """loop through all endpoint to get parh_format"""
        path_format = path
        for route in app_routes:
            if re.search(route.path_regex, path) is not None:
                return route.path_format
        return path_format
        

    def register_fastapi_metrics(self, ):
        self._is_registered = True
        self.app.add_middleware(MetricsRedirect)

        if self.is_multiprocessing:
            clear_multiproc_dir()

            self.app.mount("/metrics", WSGIMiddleware(PrometheusMiddleware.make_wsgi_multiprocess_app()))
        else:
            self.app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

    
    def add_fastapi_metrics(self, request, response):
        url = self.get_path_format(request.app.routes, request.scope.get("path", request.url.path))
        raw_path = request.scope.get("raw_path", b"/").decode("utf-8")
        if raw_path == "/metrics/":
            request.scope["path"] = "/metrics"

        duration = int(time.time() - request._tick) * SECONDTOMS

        self.add_metrics(request.method, url, response.status_code, duration)
        return response

    
    def add_fastapi_middleware(self,):
        self.register_fastapi_metrics()

        @self.app.middleware("http")
        async def add_process_time_header(request: fastapi_request, call_next):
            self.before_request()
            response = await call_next(request)
            self.add_fastapi_metrics(request, response)
            return response
        

    def register_metrics(self):
        """
        Register PrometheusMiddleware to collect all default metrics for all endpoint.
        With exception of condition is meet with excluded list.
        """
        if isinstance(self.app, Flask) and not self._is_registered:
            # self.add_flask_middleware()
            self._is_registered = True
        elif isinstance(self.app, FastAPI) and not self._is_registered:
            self.add_fastapi_middleware()
            self._is_registered = True
