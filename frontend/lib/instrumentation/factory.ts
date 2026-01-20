/**
 * Factory for creating and managing instrumentation instances
 */

import { instrumentationConfig } from "../config/instrumentation.config";
import { setupInstrumentation } from "./core/setup";
import type { InstrumentationInstance } from "./core/setup";

let instrumentationInstance: InstrumentationInstance | null = null;

/**
 * Get or create instrumentation instance
 */
export function getInstrumentation(): InstrumentationInstance | null {
  if (!instrumentationConfig.enabled) {
    return null;
  }

  if (!instrumentationInstance) {
    instrumentationInstance = setupInstrumentation(instrumentationConfig);
  }

  return instrumentationInstance;
}

/**
 * Initialize instrumentation (called on app startup)
 */
export function initializeInstrumentation(): void {
  if (instrumentationConfig.enabled) {
    getInstrumentation();
  }
}

/**
 * Shutdown instrumentation (called on app shutdown)
 */
export async function shutdownInstrumentation(): Promise<void> {
  if (instrumentationInstance) {
    await instrumentationInstance.shutdown();
    instrumentationInstance = null;
  }
}
