"""OpenTelemetry instrumentation for backend."""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import OpenTelemetry packages
try:
    from opentelemetry import metrics
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    logger.warning(
        "OpenTelemetry packages not installed. "
        "Install with: pip install opentelemetry-api opentelemetry-sdk "
        "opentelemetry-exporter-otlp-proto-http"
    )


def setup_instrumentation() -> Optional[MeterProvider]:
    """Setup OpenTelemetry instrumentation for backend.
    
    Returns:
        MeterProvider instance if setup successful, None otherwise
    """
    if not OTEL_AVAILABLE:
        logger.warning("OpenTelemetry not available, skipping instrumentation setup")
        return None
    
    # Check if instrumentation is disabled
    if os.getenv("OTEL_SDK_DISABLED", "false").lower() == "true":
        logger.info("OpenTelemetry SDK is disabled via OTEL_SDK_DISABLED")
        return None
    
    try:
        # Get OTLP endpoint from environment
        otel_endpoint = os.getenv(
            "OTEL_EXPORTER_OTLP_ENDPOINT",
            "http://otel-collector:4318/v1/metrics"
        )
        
        logger.info(f"Setting up OpenTelemetry instrumentation with endpoint: {otel_endpoint}")
        
        # Create resource
        resource = Resource.create({
            "service.name": "proj3-backend",
            "service.version": "1.0.0",
        })
        
        # Create exporter
        exporter = OTLPMetricExporter(
            endpoint=otel_endpoint,
            headers={}
        )
        
        # Create metric reader
        reader = PeriodicExportingMetricReader(
            exporter=exporter,
            export_interval_millis=30000  # 30 seconds
        )
        
        # Create meter provider
        provider = MeterProvider(
            resource=resource,
            metric_readers=[reader]
        )
        
        # Set global meter provider
        metrics.set_meter_provider(provider)
        
        logger.info("✅ OpenTelemetry instrumentation initialized successfully")
        return provider
        
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry instrumentation: {e}")
        return None
