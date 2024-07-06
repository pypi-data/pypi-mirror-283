import os
import logging
from fastapi import FastAPI
from opentelemetry import trace, _logs, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider, ConcurrentMultiSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource
)
from src import (
    APP_ENV,
    IS_LOCAL,
    KUBE_SERVICE_NAMESPACE,
    KUBE_SERVICE_NAME,
    PACKAGE_NAME,
    __version__
)
DEPLOYMENT_ENV = "local" if IS_LOCAL else APP_ENV
OTEL_EXPORTER_OTLP_ENDPOINT_TRACES = "https://datadog-agent.svc.eogresources.com/v1/traces"
OTEL_EXPORTER_OTLP_ENDPOINT_METRICS = "https://datadog-agent.svc.eogresources.com/v1/metrics"
OTEL_EXPORTER_OTLP_ENDPOINT_LOGS = "https://datadog-agent.svc.eogresources.com/v1/logs"
################################################################################################
# Manual OpenTelemetry Instrumentation for FastAPI

#FIXME: This is required to link the correct environment to datadog
resource = Resource(attributes={
        SERVICE_NAMESPACE: KUBE_SERVICE_NAMESPACE or PACKAGE_NAME,
        SERVICE_NAME: KUBE_SERVICE_NAME or PACKAGE_NAME,
        DEPLOYMENT_ENVIRONMENT: DEPLOYMENT_ENV,
        SERVICE_VERSION: __version__,
})
#V2
trace_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter() #Blank for default (will grab from env)
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)
trace.set_tracer_provider(trace_provider)

# Define a global tracer object for custom spans
TRACER = trace.get_tracer(f"tracer_{__name__}")

# Set up OTLP Metrics
otlp_metric_exporter = OTLPMetricExporter() #Blank for default (will grab from env)
metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(meter_provider)

# Define a global meter provider
METRICS = metrics.get_meter(f"meter_{__name__}")

# Set up OTLP Logging
logger_provider = LoggerProvider() #TODO: resource= on prod
handler = LoggingHandler(logger_provider=logger_provider)
otlp_log_exporter = OTLPLogExporter() #Blank for default (will grab from env)
log_processor = BatchLogRecordProcessor(otlp_log_exporter)
logger_provider.add_log_record_processor(log_processor)
_logs.set_logger_provider(logger_provider)
otel_logging_handler = LoggingHandler(logger_provider=logger_provider)

#Custom Instruments: must create an instance before calling instrument()
httpx_instrumentor = HTTPXClientInstrumentor()
httpx_instrumentor.instrument()

###########################################################################
# To be used in entry point (app.py)
#No need for async because no network calls or I/O-bound tasks
def mount_telemetry(app: FastAPI):
    LOGGER.addHandler(otel_logging_handler) #Must add logging handler on mount to export to collector
    FastAPIInstrumentor.instrument_app(
        app=app,
        tracer_provider=trace_provider,
        meter_provider=meter_provider
    )

def dismount_telemetry():
    logger_provider.shutdown()
    trace_provider.shutdown()