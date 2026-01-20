"""HTTP metrics middleware for collecting request metrics."""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Try to import OpenTelemetry
try:
    from opentelemetry import metrics
    
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP request metrics."""
    
    def __init__(self, app):
        super().__init__(app)
        self.meter = None
        self.request_duration_histogram = None
        self.request_count_counter = None
        
        if OTEL_AVAILABLE:
            try:
                self.meter = metrics.get_meter("http-requests-meter")
                # Create histogram for request duration in milliseconds
                self.request_duration_histogram = self.meter.create_histogram(
                    "http_request_duration_milliseconds",
                    description="Duration of HTTP requests in milliseconds",
                    unit="ms",
                )
                # Create counter for request count
                self.request_count_counter = self.meter.create_counter(
                    "http_request_count",
                    description="Count of HTTP requests",
                )
                logger.info("✅ HTTP metrics middleware initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize metrics: {e}")
    
    async def dispatch(self, request: Request, call_next):
        """Process request and collect metrics."""
        if not self.request_duration_histogram or not self.request_count_counter:
            # Metrics not available, just pass through
            return await call_next(request)
        
        # Start timing
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Extract path (remove query string)
        path = request.url.path
        if "?" in path:
            path = path.split("?")[0]
        
        # Build attributes
        attributes = {
            "method": request.method,
            "path": path,
            "status_code": response.status_code,
        }
        
        # Add run_id if available
        if hasattr(request.state, "run_id") and request.state.run_id:
            attributes["run_id"] = request.state.run_id
        
        # Record metrics
        try:
            self.request_duration_histogram.record(duration_ms, attributes)
            self.request_count_counter.add(1, attributes)
        except Exception as e:
            logger.debug(f"Failed to record metrics: {e}")
        
        return response


def metrics_middleware(app):
    """Add metrics middleware to FastAPI app."""
    app.add_middleware(MetricsMiddleware)
    return app
