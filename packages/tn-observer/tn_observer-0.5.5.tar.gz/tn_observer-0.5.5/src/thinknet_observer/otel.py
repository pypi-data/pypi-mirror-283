
import os, json

from urllib.parse import urlparse

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor, ConsoleSpanExporter

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor

from opentelemetry.semconv.trace import SpanAttributes

from .metrics.metrics import PrometheusMiddleware
from .metrics.collector import MetricCollector


DEBUG_LOG_OTEL_TO_PROVIDER = False
DISABLE_TRACE = (os.getenv("OTEL_DISABLE_TRACE", False) == True)

DEFAULT_EXCLUDED_ROUTES = "metrics,healthy,healthz,readyz,livez,startz,favicon.ico"
OTEL_EXCLUDED_URLS = os.getenv("OTEL_EXCLUDED_URLS", DEFAULT_EXCLUDED_ROUTES)
OTEL_EXCLUDED_TRACES_URLS = os.getenv("OTEL_EXCLUDED_TRACES_URLS","")
OTEL_EXCLUDED_METRICS_URLS = os.getenv("OTEL_EXCLUDED_METRICS_URLS","")
OTEL_EXCLUDED_LOGS_URLS = os.getenv("OTEL_EXCLUDED_LOGS_URLS","")


class TNObserver:

    metric_client = MetricCollector.histogram(
        "http_client_duration_milliseconds_count",
        "metric for measurement to other api/service",
        labels=["http_request_method", "service_address", "http_response_status_code"]
    )

    def __init__(self, service_name: str, service_namespace:str=None, service_version=None):
        service_namespace = service_namespace if service_namespace else "local" 
        self.resource = TNObserver.setup_resource(service_name, service_namespace, service_version)


    @classmethod
    def with_default_service_info(cls):
        package_json = TNObserver.get_package_json()
        service_name = os.getenv("SERVICE_NAME", package_json.get("name", ""))
        service_namespace = os.getenv("SERVICE_NAME_PREFIX", "local")
        service_version = os.getenv("APP_VERSION", package_json.get("version", ""))
        print (service_version)
        return cls(service_name, service_namespace, service_version)
        

    @staticmethod
    def get_package_json():
        json_path = f"{os.getcwd()}/package.json" 
        with open(json_path) as json_file:
            json_data = json.load(json_file)

        return json_data


    @property
    def resources(self,) -> Resource:
        return self.resource


    @staticmethod
    def setup_resource(service_name: str, service_namespace: str, service_version: str):
        resource =  Resource.create({
            "service.name": f"{service_namespace}/{service_name}",
            "service.version": service_version if service_version else "1.0.0",
            "service.namespace": service_namespace,
            "app.name": service_name,
        })
        return resource
    


    @staticmethod
    def setup_trace(name, resource=None):

        trace_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(trace_provider)

        if not DISABLE_TRACE:
            if DEBUG_LOG_OTEL_TO_PROVIDER :
                span_process = SimpleSpanProcessor(ConsoleSpanExporter())
            else:
                otel_endpoint_url = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
                # otlp_span_exporter = OTLPSpanExporter(endpoint=otel_endpoint_url,headers=otel_http_headers)
                otlp_span_exporter = OTLPSpanExporter(endpoint=otel_endpoint_url)
                span_process = BatchSpanProcessor(otlp_span_exporter)
                # trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))

            trace.get_tracer_provider().add_span_processor(span_process)
            tracer = trace.get_tracer(name)

            return tracer
        
        return None


    @staticmethod
    def setup_metrics(name, resource=None):
        # print (DEBUG_LOG_OTEL_TO_PROVIDER)
        if DEBUG_LOG_OTEL_TO_PROVIDER :
            metric_provider = MeterProvider(
                metric_readers=[PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)],
                resource=resource
                )
        else:
            otel_endpoint_url = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', "http://localhost:4317")
            metric_provider = MeterProvider(
                metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=otel_endpoint_url), export_interval_millis=50000)],
                resource=resource
                )

        metrics.set_meter_provider(metric_provider)
        meter = metrics.get_meter(name)
        return meter
    

    @staticmethod
    def _trace_exclude_urls(excluded_urls) -> str:

        str_excludes_routes = ''

        if OTEL_EXCLUDED_TRACES_URLS == 'none' or (OTEL_EXCLUDED_URLS == 'none' and OTEL_EXCLUDED_TRACES_URLS == ''):
            return ''
        elif OTEL_EXCLUDED_TRACES_URLS == '':
            str_excludes_routes = OTEL_EXCLUDED_URLS
        else:
            str_excludes_routes = OTEL_EXCLUDED_TRACES_URLS
        
        if isinstance(excluded_urls, list):
            temp_urls = []
            for url in excluded_urls:
                if isinstance(url, dict) and "route" in url:
                    url = url["route"][1:] if url["route"][0] == "/" else url["route"]
                    temp_urls.append(url)
                elif isinstance(url, str):
                    url = url [1:] if url[0] == "/" else url
                    temp_urls.append(url)

            str_urls = ",".join(temp_urls)
            return str_excludes_routes + "," + str_urls
        elif isinstance(excluded_urls, str):
            return str_excludes_routes + "," + excluded_urls
        else:
            return str_excludes_routes


    @staticmethod
    def flask_instrumentation(app, excluded_urls=None):
        excluded_urls = TNObserver._trace_exclude_urls(excluded_urls)
        return FlaskInstrumentor().instrument_app(app, excluded_urls=excluded_urls)
    
    
    @staticmethod
    def fast_instrumentation(app, excluded_urls=None):
        excluded_urls = TNObserver._trace_exclude_urls(excluded_urls)
        return FastAPIInstrumentor().instrument_app(app, excluded_urls=excluded_urls)
    
    
    @staticmethod
    def pymongo_instrumentation():
        return PymongoInstrumentor().instrument()
    

    @staticmethod
    def _requests_request_hook(span: trace.Span, req):
        url = req.url
        o = urlparse(url)
        if span and span.is_recording():
            span.update_name(f"{req.method} {o.path}")
            span.set_attribute(SpanAttributes.HTTP_ROUTE, o.path)


    @staticmethod
    def _requests_response_hook(span: trace.Span, req, res):
        duration = int(res.elapsed.total_seconds() * 1000)
        TNObserver.metric_client.labels(req.method ,req.url, res.status_code).observe(duration)
    

    @staticmethod
    def requests_instrumentation():
        return RequestsInstrumentor().instrument(
            request_hook=TNObserver._requests_request_hook, 
            response_hook=TNObserver._requests_response_hook)
    

    @staticmethod
    def kafka_instrumentation():
        return KafkaInstrumentor().instrument()
    

    @staticmethod
    def pika_instrumentation():
        return PikaInstrumentor().instrument()
    

    @staticmethod
    def pika_instrumentor():
        return PikaInstrumentor()
    

    @staticmethod
    def _list_str_exclude_urls(str_exclude: str, is_metrics:bool = False):
        if is_metrics:
            return [{"route": f"/{url}"} for url in str_exclude.split(",")]
        else:
            return [f"/{url}" for url in str_exclude.split(",")]
    

    @staticmethod
    def _metrics_exclude_urls(excluded_urls) -> list:
        list_excluded_route = []

        if OTEL_EXCLUDED_METRICS_URLS  == 'none' or (OTEL_EXCLUDED_URLS == 'none' and OTEL_EXCLUDED_METRICS_URLS == ''):
            return list_excluded_route
        elif OTEL_EXCLUDED_METRICS_URLS  == '':
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(OTEL_EXCLUDED_URLS, True))
        else:
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(OTEL_EXCLUDED_METRICS_URLS, True))

        if isinstance(excluded_urls, str):
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(excluded_urls, True))

        if isinstance(excluded_urls, list):
            for url in excluded_urls:
                if isinstance(url, str):
                    list_excluded_route.append({"route": f"/{url}"})
                elif isinstance(url, dict):
                    url['route'] = f"/{url['route']}" if url['route'][0] != "/" else url['route']
                    list_excluded_route.append(url)
                    
        return list_excluded_route
    

    @staticmethod
    def register_metrics(app, resource: Resource, is_multiprocessing: bool=False, excluded_urls:list=[]):
        namespace = resource.attributes['service.namespace']
        service_name = resource.attributes['app.name']
        prom_middleware = PrometheusMiddleware(app, is_multiprocessing=is_multiprocessing, 
                                               service_name=service_name, namespace=namespace)
        
        list_exclude = TNObserver._metrics_exclude_urls(excluded_urls)
        print ('list_exclude route metric', list_exclude)
        prom_middleware.add_exclude(list_exclude)
        prom_middleware.register_metrics()


    @staticmethod
    def logs_exclude_urls() -> list:
        list_excluded_route = []

        if OTEL_EXCLUDED_LOGS_URLS  == 'none' or (OTEL_EXCLUDED_URLS == 'none' and OTEL_EXCLUDED_LOGS_URLS == ''):
            return list_excluded_route
        elif OTEL_EXCLUDED_LOGS_URLS  == '':
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(OTEL_EXCLUDED_URLS))
        else:
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(OTEL_EXCLUDED_LOGS_URLS))
                    
        return list_excluded_route
