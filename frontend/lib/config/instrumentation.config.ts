/**
 * Centralized instrumentation configuration
 * All instrumentation settings are defined here with type safety
 */

export interface InstrumentationConfig {
  /** Whether instrumentation is enabled */
  enabled: boolean;
  
  /** Service name for telemetry */
  serviceName: string;
  
  /** Endpoint URL for sending metrics */
  endpoint: string;
  
  /** Interval in milliseconds for exporting metrics */
  exportInterval: number;
  
  /** Whether to track HTTP requests */
  trackHttpRequests: boolean;
  
  /** Headers to include in export requests */
  exportHeaders: Record<string, string>;
  
  /** Run ID header name for correlation */
  runIdHeaderName: string;
  
  /** Paths to exclude from tracking */
  excludedPaths: string[];
}

/**
 * Get instrumentation configuration from environment variables
 */
export function getInstrumentationConfig(): InstrumentationConfig {
  const isBrowser = typeof window !== "undefined";
  const enabled = isBrowser && 
    process.env.NEXT_PUBLIC_ENABLE_INSTRUMENTATION === "true";
  
  // Point directly to OpenTelemetry collector OTLP HTTP endpoint
  // Use environment variable if set, otherwise default to localhost for browser
  const otelEndpoint = process.env.NEXT_PUBLIC_OTEL_ENDPOINT || 
    "http://localhost:4318/v1/metrics";
  
  return {
    enabled,
    serviceName: process.env.NEXT_PUBLIC_SERVICE_NAME || "proj3-frontend",
    endpoint: otelEndpoint,
    exportInterval: parseInt(
      process.env.NEXT_PUBLIC_OTEL_EXPORT_INTERVAL || "30000",
      10
    ),
    trackHttpRequests: true,
    exportHeaders: {
      "Content-Type": "application/json",
    },
    runIdHeaderName: "X-Run-ID",
    excludedPaths: ["/otel-metrics", "/health"],
  };
}

/**
 * Singleton configuration instance
 */
export const instrumentationConfig = getInstrumentationConfig();
