/**
 * Collects HTTP request metrics by intercepting fetch and XMLHttpRequest
 */

import { metrics, ValueType } from "@opentelemetry/api";
import type { RequestCollector, RequestMetadata } from "../types";
import { RunIdExtractor } from "../attributes/run-id-extractor";

export class HttpRequestCollector implements RequestCollector {
  private meter = metrics.getMeter("network-requests-meter");
  private requestDurationHistogram = this.meter.createHistogram(
    "http_request_duration_milliseconds",
    {
      description: "Duration of HTTP requests in milliseconds",
      unit: "ms",
      valueType: ValueType.DOUBLE,
    }
  );
  private requestCountCounter = this.meter.createCounter("http_request_count", {
    description: "Count of HTTP requests",
    valueType: ValueType.INT,
  });

  private originalFetch: typeof fetch;
  private originalXHR: typeof XMLHttpRequest;
  private runIdExtractor: RunIdExtractor;
  private excludedPaths: string[];

  constructor(
    runIdHeaderName: string = "X-Run-ID",
    excludedPaths: string[] = []
  ) {
    this.runIdExtractor = new RunIdExtractor(runIdHeaderName);
    this.excludedPaths = excludedPaths;
    this.originalFetch = window.fetch;
    this.originalXHR = window.XMLHttpRequest;
  }

  start(): void {
    this.interceptFetch();
    this.interceptXMLHttpRequest();
  }

  stop(): void {
    window.fetch = this.originalFetch;
    window.XMLHttpRequest = this.originalXHR;
  }

  isTracking(path: string): boolean {
    return !this.excludedPaths.some((excluded) => path.includes(excluded));
  }

  private recordMetrics(metadata: RequestMetadata): void {
    const index = metadata.path.indexOf("?");
    const pathname = index === -1 ? metadata.path : metadata.path.substring(0, index);
    const query = index !== -1 ? metadata.path.substring(index + 1) : undefined;

    const attributes: Record<string, string | number> = {
      method: metadata.method.toUpperCase(),
      path: pathname,
      status_code: metadata.statusCode || 0,
      success: metadata.success ? "true" : "false",
    };

    if (query) {
      attributes.query = query;
    }

    if (metadata.runId) {
      attributes.run_id = metadata.runId;
    }

    this.requestDurationHistogram.record(metadata.duration, attributes);
    this.requestCountCounter.add(1, attributes);
  }

  private getUrlPath(url: string | URL | Request): string {
    try {
      if (typeof url === "string") {
        const parsed = new URL(url, window.location.href);
        return parsed.pathname + parsed.search;
      }
      if (url instanceof URL) {
        return url.pathname + url.search;
      }
      if (url instanceof Request) {
        return new URL(url.url).pathname + new URL(url.url).search;
      }
      return "unknown";
    } catch {
      return typeof url === "string" ? url : "unknown";
    }
  }

  private interceptFetch(): void {
    const self = this;
    window.fetch = async function (...args) {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url || "unknown";
      const method = args[1]?.method || "GET";
      const startTime = performance.now();
      const urlPath = self.getUrlPath(args[0] as string | Request);
      const runId = args[1]?.headers
        ? self.runIdExtractor.extractRunId(
            args[1].headers as Headers | Record<string, string>
          )
        : null;

      if (!self.isTracking(urlPath)) {
        return self.originalFetch.apply(this, args);
      }

      try {
        const response = await self.originalFetch.apply(this, args);
        const duration = performance.now() - startTime;

        self.recordMetrics({
          method,
          path: urlPath,
          statusCode: response.status,
          duration,
          success: response.ok,
          runId: runId || undefined,
        });

        return response;
      } catch (error) {
        const duration = performance.now() - startTime;

        self.recordMetrics({
          method,
          path: urlPath,
          statusCode: 0,
          duration,
          success: false,
          runId: runId || undefined,
        });

        throw error;
      }
    };
  }

  private interceptXMLHttpRequest(): void {
    const self = this;
    const OriginalXHR = this.originalXHR;

    window.XMLHttpRequest = function (this: XMLHttpRequest) {
      const xhr = new OriginalXHR();

      let method = "GET";
      let urlPath = "unknown";
      let startTime = 0;
      let runId: string | null = null;

      const originalOpen = xhr.open;
      xhr.open = function (m: string, url: string, ...rest: any[]) {
        method = m;
        urlPath = self.getUrlPath(url);
        return originalOpen.apply(this, [m, url, ...rest]);
      };

      const originalSetRequestHeader = xhr.setRequestHeader;
      xhr.setRequestHeader = function (header: string, value: string) {
        if (header.toLowerCase() === self.runIdExtractor.headerName.toLowerCase()) {
          runId = value;
        }
        return originalSetRequestHeader.apply(this, [header, value]);
      };

      const originalSend = xhr.send;
      xhr.send = function (...args: any[]) {
        startTime = performance.now();
        return originalSend.apply(this, args);
      };

      xhr.addEventListener("loadend", function () {
        if (self.isTracking(urlPath)) {
          const duration = performance.now() - startTime;
          self.recordMetrics({
            method,
            path: urlPath,
            statusCode: xhr.status,
            duration,
            success: xhr.status >= 200 && xhr.status < 400,
            runId: runId || undefined,
          });
        }
      });

      xhr.addEventListener("error", function () {
        if (self.isTracking(urlPath)) {
          const duration = performance.now() - startTime;
          self.recordMetrics({
            method,
            path: urlPath,
            statusCode: 0,
            duration,
            success: false,
            runId: runId || undefined,
          });
        }
      });

      xhr.addEventListener("abort", function () {
        if (self.isTracking(urlPath)) {
          const duration = performance.now() - startTime;
          self.recordMetrics({
            method,
            path: urlPath,
            statusCode: 0,
            duration,
            success: false,
            runId: runId || undefined,
          });
        }
      });

      return xhr;
    };

    // Copy static properties and prototype
    Object.keys(OriginalXHR).forEach((key) => {
      try {
        (window.XMLHttpRequest as any)[key] = (OriginalXHR as any)[key];
      } catch (e) {
        // Some properties may not be writable
      }
    });
    window.XMLHttpRequest.prototype = OriginalXHR.prototype;
  }
}
