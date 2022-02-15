from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.api_registry import api_registry
from app.config import ConfigClass
from app.resources.error_handler import APIException


def create_app():
    """Initialize and configure app."""

    app = FastAPI(
        title='Service Data Download',
        description='Service for data download usage',
        docs_url='/v1/api-doc',
        version=ConfigClass.VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.exception_handler(APIException)
    async def http_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.content,
        )

    api_registry(app)

    instrument_app(app)

    return app


def instrument_app(app: FastAPI) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    if not ConfigClass.OPEN_TELEMETRY_ENABLED:
        return

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: ConfigClass.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    AsyncPGInstrumentor().instrument()

    jaeger_exporter = JaegerExporter(
        agent_host_name=ConfigClass.OPEN_TELEMETRY_HOST, agent_port=ConfigClass.OPEN_TELEMETRY_PORT
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
