"use client";

import { useEffect } from "react";
import { initializeInstrumentation, shutdownInstrumentation } from "@/lib/instrumentation/factory";

export function InstrumentationLoader() {
  useEffect(() => {
    // Initialize instrumentation on mount
    initializeInstrumentation();

    // Cleanup on unmount
    return () => {
      shutdownInstrumentation().catch((error) => {
        console.error("Error shutting down instrumentation:", error);
      });
    };
  }, []);

  return null;
}
