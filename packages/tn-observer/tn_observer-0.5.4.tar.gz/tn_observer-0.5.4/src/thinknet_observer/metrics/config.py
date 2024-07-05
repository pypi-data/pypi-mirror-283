import os


_DEFAULT_BUCKETS_BACKUP = [0.05, 0.1, 0.5, 0.9, 0.95]
# buckets in milliseconds #
_DEFAULT_BUCKETS = [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000,]
_DEFAULT_LABELS = ["http_request_method", "http_route", "http_response_status_code", "service_name", "service_namespace"]

UNDEFINED = "UNDEFINED"

NAMESPACE = os.getenv("SERVICE_NAME_PREFIX", UNDEFINED)
SERVICENAME = os.getenv("SERVICE_NAME", UNDEFINED)
SERVICEVERSION = os.getenv("SERVICE_VERSION", "1.0.0")
EXCLUDE_URLS = os.getenv("OTEL_PYTHON_EXCLUDED_URLS", "")
DICT_REQURIED_LABELS = {"service_namespace": NAMESPACE, "service_name": SERVICENAME}
SECONDTOMS = 1000
