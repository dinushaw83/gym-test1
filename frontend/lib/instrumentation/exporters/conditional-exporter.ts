/**
 * Conditional exporter that only sends metrics when there's actual data
 */

import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-http";
import type { MetricExporter } from "../types";
import type { MetricData } from "@opentelemetry/sdk-metrics";

export class ConditionalExporter implements MetricExporter {
  private baseExporter: OTLPMetricExporter;

  constructor(
    endpoint: string,
    headers: Record<string, string> = {}
  ) {
    this.baseExporter = new OTLPMetricExporter({
      url: endpoint,
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    });
  }

  async export(metrics: MetricData, resultCallback?: (result: any) => void): Promise<void> {
    // Check if there's any actual data to send
    const hasData = metrics.scopeMetrics?.some((sm) =>
      sm.metrics?.some(
        (m) =>
          m.dataPoints?.length > 0 ||
          (m as any).histogram?.dataPoints?.length > 0 ||
          (m as any).sum?.dataPoints?.length > 0 ||
          (m as any).gauge?.dataPoints?.length > 0
      )
    );

    if (!hasData) {
      // No data, skip export
      if (resultCallback) {
        resultCallback({ code: 0 }); // Success without sending
      }
      return;
    }

    // Has data, forward to actual exporter
    return new Promise((resolve, reject) => {
      this.baseExporter.export(metrics, (result) => {
        if (result.code === 0) {
          resolve();
          if (resultCallback) resultCallback(result);
        } else {
          reject(new Error(`Export failed: ${result.code}`));
          if (resultCallback) resultCallback(result);
        }
      });
    });
  }

  async forceFlush(): Promise<void> {
    return this.baseExporter.forceFlush();
  }

  async shutdown(): Promise<void> {
    return this.baseExporter.shutdown();
  }
}
