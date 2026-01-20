/**
 * Core instrumentation setup and initialization
 */

import { metrics } from "@opentelemetry/api";
import { MeterProvider, PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";
import { resourceFromAttributes } from "@opentelemetry/resources";
import type { InstrumentationConfig } from "../types";
import { ConditionalExporter } from "../exporters/conditional-exporter";
import { HttpRequestCollector } from "../collectors/http-collector";

export interface InstrumentationInstance {
  collector: HttpRequestCollector;
  shutdown: () => Promise<void>;
}

/**
 * Setup and initialize instrumentation
 */
export function setupInstrumentation(
  config: InstrumentationConfig
): InstrumentationInstance | null {
  if (!config.enabled) {
    return null;
  }

  // Create exporter
  const exporter = new ConditionalExporter(
    config.endpoint,
    config.exportHeaders
  );

  // Create metric reader
  const metricReader = new PeriodicExportingMetricReader({
    exporter: exporter as any,
    exportIntervalMillis: config.exportInterval,
  });

  // Create meter provider
  const meterProvider = new MeterProvider({
    resource: resourceFromAttributes({
      "service.name": config.serviceName,
    }),
    readers: [metricReader],
  });

  // Set global meter provider
  metrics.setGlobalMeterProvider(meterProvider);

  // Setup HTTP request collector if enabled
  let collector: HttpRequestCollector | null = null;
  if (config.trackHttpRequests) {
    collector = new HttpRequestCollector(
      config.runIdHeaderName,
      config.excludedPaths
    );
    collector.start();
  }

  return {
    collector: collector!,
    shutdown: async () => {
      if (collector) {
        collector.stop();
      }
      await metricReader.forceFlush();
      await metricReader.shutdown();
      await exporter.shutdown();
    },
  };
}
