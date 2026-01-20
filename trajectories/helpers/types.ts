/**
 * Type definitions for UI Journey Testing
 * 
 * These types help organize and categorize user journeys
 * for comprehensive test coverage.
 */

/**
 * Journey Priority Classification
 * - MAJOR: Critical user flows that must work (login, checkout, core features)
 * - MINOR: Secondary flows that enhance UX (settings, preferences, edge cases)
 */
export type JourneyPriority = 'major' | 'minor';

/**
 * Journey Category
 * Groups journeys by functional area
 */
export type JourneyCategory = 
  | 'authentication'
  | 'navigation'
  | 'data-entry'
  | 'data-display'
  | 'search'
  | 'settings'
  | 'notifications'
  | 'error-handling'
  | 'accessibility';

/**
 * Test Tags for filtering and organizing tests
 */
export type TestTag = 
  | '@major'
  | '@minor'
  | '@smoke'
  | '@regression'
  | '@critical'
  | '@flaky'
  | '@slow';

/**
 * Journey Step Definition
 */
export interface JourneyStep {
  /** Step name for logging */
  name: string;
  /** Step description */
  description: string;
  /** Expected outcome after step completion */
  expectedOutcome: string;
}

/**
 * User Journey Definition
 * Represents a complete user flow through the application
 */
export interface UserJourney {
  /** Unique identifier for the journey */
  id: string;
  /** Human-readable name */
  name: string;
  /** Detailed description of the journey */
  description: string;
  /** Journey priority classification */
  priority: JourneyPriority;
  /** Functional category */
  category: JourneyCategory;
  /** Tags for test filtering */
  tags: TestTag[];
  /** Ordered list of steps */
  steps: JourneyStep[];
  /** Preconditions that must be met */
  preconditions?: string[];
  /** Expected final state */
  expectedFinalState: string;
}

/**
 * Journey Result for reporting
 */
export interface JourneyResult {
  journeyId: string;
  status: 'passed' | 'failed' | 'skipped';
  duration: number;
  stepsCompleted: number;
  totalSteps: number;
  error?: string;
  screenshots?: string[];
}

/**
 * Test Configuration
 */
export interface JourneyTestConfig {
  /** Base URL for the application */
  baseUrl: string;
  /** Default timeout in milliseconds */
  timeout: number;
  /** Number of retries on failure */
  retries: number;
  /** Enable screenshot capture */
  screenshots: boolean;
  /** Enable video recording */
  video: boolean;
  /** Enable trace collection */
  trace: boolean;
}

/**
 * Page Object Interface
 * Base interface for Page Object Model pattern
 */
export interface PageObject {
  /** Navigate to the page */
  goto(): Promise<void>;
  /** Wait for the page to be fully loaded */
  waitForLoad(): Promise<void>;
  /** Check if the page is visible */
  isVisible(): Promise<boolean>;
}

