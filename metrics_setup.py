from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource


def setup_metrics(service_name: str, otlp_endpoint: str):
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=otlp_endpoint))
    resource = Resource.create({"service.name": service_name})
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))


# 예: setup_metrics("code-review-agent", "http://prometheus:9090/api/v1/otlp/v1/metrics")
