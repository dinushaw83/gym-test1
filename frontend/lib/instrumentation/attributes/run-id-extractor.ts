/**
 * Extracts run ID from various header formats
 */

import type { AttributeExtractor } from "../types";

export class RunIdExtractor implements AttributeExtractor {
  public readonly headerName: string;
  
  constructor(headerName: string = "X-Run-ID") {
    this.headerName = headerName;
  }

  extractRunId(
    headers: Headers | Record<string, string> | [string, string][]
  ): string | null {
    if (headers instanceof Headers) {
      return headers.get(this.headerName);
    }

    if (Array.isArray(headers)) {
      const entry = headers.find(
        ([key]) => key.toLowerCase() === this.headerName.toLowerCase()
      );
      return entry ? entry[1] : null;
    }

    if (typeof headers === "object") {
      for (const key in headers) {
        if (key.toLowerCase() === this.headerName.toLowerCase()) {
          return headers[key];
        }
      }
    }

    return null;
  }
}
