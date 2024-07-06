from typing import Union
from .Resource import Resource
from fastapi import FastAPI
from flask import Flask
import logging
'''
Constructs Observer with Resource object
'''
from opentelemetry import trace, _logs, metrics
from opentelemetry.sdk.trace import TracerProvider, ConcurrentMultiSpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource as OTEL_Resource
# from opentelemetry.sdk.resources import (
#     DEPLOYMENT_ENVIRONMENT,
#     SERVICE_NAME,
#     SERVICE_NAMESPACE,
#     SERVICE_VERSION,
# )
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

class Observer:
    ########################################################################
    # Constructor
    def __init__(self, resource_data: Resource):
        # Exit Case: Standardized app environment naming
        accepted_environments = ["dev", "stage", "prod", "local"]
        if resource_data.app_env not in accepted_environments:
            raise ValueError("Supported env input are: 'dev'|'stage'|'prod'|'local'.")

        self.resource_data = resource_data

        # Dynamic variables determined on runtime (Checkers)
        self.app_type = self._determine_app_type(resource_data.app)
        self.app_title = self._determine_app_title(resource_data.app)
        self.app_version = self._determine_app_version(resource_data.app)

        # Open Telemetry members
        # self.tracer_provider = None
        # self.meter_provider = None
        # self.logger_provider = None
        # self.otel_logging_handler = None
        # self.TRACER = None
        # self.METRICS = None

        self.mount_telemetry(resource_data.app)


    ########################################################################
    # Checkers
    @staticmethod
    def _determine_app_type(app: Union[FastAPI, Flask]) -> str:
        if isinstance(app, FastAPI):
            return "FastAPI"
        elif isinstance(app, Flask):
            return "Flask"
        else:
            raise ValueError("Unsupported app type. Only FastAPI and Flask are supported.")
    
    def _determine_app_title(self, app: Union[FastAPI, Flask]) -> str:
        if self.app_type == "FastAPI":
            return app.title
        elif self.app_type == "Flask":
            return app.import_name
    
    def _determine_app_version(self, app: Union[FastAPI, Flask]) -> str:
        if self.app_type == "FastAPI":
            return app.version
        elif self.app_type == "Flask":
            return app.__version__

    ########################################################################
    # Setters FIXME: Access Resource object instead
    @classmethod
    def edit_options(cls, observer: 'Observer', **kwargs):
        for key, value in kwargs.items():
            if hasattr(observer.resource_data, key):
                setattr(observer.resource_data, key, value)
            else:
                error = f"'Resource' object has no attribute '{key}'"
                raise AttributeError(error)
        return observer
    ########################################################################
    # Getters
    def get_resource(self):
        return self.resource_data
    ########################################################################
    # Methods
    def mount_telemetry(self, app):
        print("mounting..")#FIXME
        otel_resource = OTEL_Resource(
            attributes={
                "service.name": self.app_title, #obtain from app object
                "deployment.environment": self.resource_data.app_env,
                "service.version": self.app_version, #obtain from app object
            }
        )
        # # Set up Tracer & Exporter
        # Initialize TracerProvider and Exporter
        trace.set_tracer_provider(TracerProvider(resource=otel_resource))
        trace_provider = trace.get_tracer_provider()
        otlp_trace_exporter = OTLPSpanExporter(endpoint=self.resource_data.export_endpoint + "/v1/traces")
        span_processor = BatchSpanProcessor(otlp_trace_exporter)
        # console_span_exporter = ConsoleSpanExporter()
        # span_processor = BatchSpanProcessor(console_span_exporter)
        trace_provider.add_span_processor(span_processor)

        # Set up Meter & Exporter
        #console_metric_exporter = ConsoleMetricExporter() 
        otlp_metrics_exporter = OTLPMetricExporter(endpoint=self.resource_data.export_endpoint + "/v1/metrics")
        metrics.set_meter_provider(MeterProvider([PeriodicExportingMetricReader(otlp_metrics_exporter)], resource=otel_resource))
        # to configure custom metrics
        configuration = {
            "system.memory.usage": ["used", "free", "cached"],
            "system.cpu.time": ["idle", "user", "system", "irq"],
            "system.network.io": ["transmit", "receive"],
            "system.network.dropped.packets": ["receive", "transmit"], 
            "process.runtime.memory": ["rss", "vms"],
            "process.runtime.cpu.time": ["user", "system"],
            "process.runtime.context_switches": ["involuntary", "voluntary"],
        }
        SystemMetricsInstrumentor(config=configuration).instrument()

        # Set up OTLP Logging FIXME (test and try)
        logger_provider = LoggerProvider(resource=otel_resource)
        #console_log_exporter = ConsoleLogExporter()
        #log_processor = BatchLogRecordProcessor(console_log_exporter)
        otlp_log_exporter = OTLPLogExporter(endpoint=self.resource_data.export_endpoint + "/v1/logs") #Blank for default (will grab from env)
        log_processor = BatchLogRecordProcessor(otlp_log_exporter)
        logger_provider.add_log_record_processor(log_processor)
        _logs.set_logger_provider(logger_provider)

        print("..done mounting")

        #TODO: ISOLATE INSTRUMENTATION
        print("instrumenting..")
        try:
            FastAPIInstrumentor.instrument_app(app)
            HTTPXClientInstrumentor().instrument()
            RequestsInstrumentor().instrument()
            #AsyncioInstrumentor.instrument() FIXME: breaking
        except:
            raise Exception("Could not instrument app")
        '''
        TODO: Refactor to instrument properly:
        app = ... 
        instrumentations = [
            ("opentelemetry.instrumentation.fastapi", "FastAPIInstrumentor", "instrument_app", {"app": app}),
            ("opentelemetry.instrumentation.starlette", "StarletteInstrumentor", "instrument_app", {"app": app}),
            ("opentelemetry.instrumentation.psycopg", "PsycopgInstrumentor", "instrument", {"enable_commenter": True, "commenter_options": {}}),
            ("opentelemetry.instrumentation.psycopg2", "Psycopg2Instrumentor", "instrument", {"enable_commenter": True, "commenter_options": {}}),
            ("opentelemetry.instrumentation.sqlalchemy", "SQLAlchemyInstrumentor", "instrument", {"enable_commenter": True, "commenter_options": {}}),
            ("opentelemetry.instrumentation.httpx", "HTTPXClientInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.aio_pika", "AioPikaInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.kafka", "KafkaInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.asyncio", "AsyncioInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.mysql", "MySQLInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.mysqlclient", "MySQLClientInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.pymemcache", "PymemcacheInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.pymongo", "PymongoInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.pymysql", "PyMySQLInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.redis", "RedisInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.requests", "RequestsInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.sqlite3", "SQLite3Instrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.threading", "ThreadingInstrumentor", "instrument", {}),
            ("opentelemetry.instrumentation.urllib3", "URLLib3Instrumentor", "instrument", {}),
        ]

        for module_name, class_name, method, args in instrumentations:
            try:
                module = __import__(module_name, fromlist=[class_name])
                instrumentor_class = getattr(module, class_name)
                instrumentor = instrumentor_class()
                getattr(instrumentor, method)(**args)
            except ImportError as e:
                print(f"Skipping {class_name} instrumentation due to missing dependency: {e}")
        '''

        print("..done instrumenting")

    def dismount_telemetry(self):
        self.logger_provider.shutdown()
        self.trace_provider.shutdown()
        self.meter_provider.shutdown()

    ########################################################################
    # Destructor
    def __del__(self):
        self.dismount_telemetry()
        logging.log(f"Observer for {self.resource_data.app_name} has been cleaned up.")
        print("dismounted")#FIXME

#steer away from CLI edits
#the class object will have state for startup and shutdown
#just tell people where to place it (in or after startup of app service object)


# mount and dismount the app object since you have access to it in here
# do for open telemetry and separate for ddtrace (TODO)