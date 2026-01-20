/**
 * Type definitions for instrumentation components
 */

import { MetricData } from "@opentelemetry/sdk-metrics";

/**
 * Configuration for instrumentation
 */
export interface InstrumentationConfig {
  enabled: boolean;
  serviceName: string;
  endpoint: string;
  exportInterval: number;
  trackHttpRequests: boolean;
  exportHeaders: Record<string, string>;
  runIdHeaderName: string;
  excludedPaths: string[];
}

/**
 * Request metadata for tracking
 */
export interface RequestMetadata {
  method: string;
  path: string;
  query?: string;
  statusCode: number;
  duration: number;
  success: boolean;
  runId?: string;
}

/**
 * Metric exporter interface
 */
export interface MetricExporter {
  export(metrics: MetricData): Promise<void>;
  forceFlush(): Promise<void>;
  shutdown(): Promise<void>;
}

/**
 * Request collector interface
 */
export interface RequestCollector {
  start(): void;
  stop(): void;
  isTracking(path: string): boolean;
}

/**
 * Attribute extractor interface
 */
export interface AttributeExtractor {
  extractRunId(headers: Headers | Record<string, string> | [string, string][]): string | null;
}
