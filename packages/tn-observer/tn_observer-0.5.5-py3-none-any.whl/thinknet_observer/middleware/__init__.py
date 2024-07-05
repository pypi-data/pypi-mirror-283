from opentelemetry.sdk.resources import Resource

def get_resource_info(resource: Resource):
    if resource:
        return resource.attributes['service.namespace'], resource.attributes['app.name']
    else:
        return 'unknown_namespace', 'unknown_service_name'