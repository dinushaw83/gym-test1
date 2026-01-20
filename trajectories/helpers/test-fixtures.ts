import { test as base, Page } from '@playwright/test';
import { 
  logJourneyStart, 
  logJourneyComplete,
} from './journey-utils';

/**
 * Extended Test Fixtures
 * 
 * Custom fixtures that provide additional functionality
 * for journey testing.
 */

// Define custom fixture types
type CustomFixtures = {
  /** Page with journey logging enabled */
  journeyPage: Page;
  /** Test data generator */
  testData: TestDataGenerator;
  /** Journey context for tracking */
  journeyContext: JourneyContext;
};

/**
 * Journey Context for tracking test execution
 */
interface JourneyContext {
  journeyId: string;
  startTime: number;
  stepsCompleted: number;
  addStep: () => void;
}

/**
 * Test Data Generator
 */
interface TestDataGenerator {
  /** Generate a unique email */
  email: () => string;
  /** Generate a unique username */
  username: () => string;
  /** Generate random string */
  randomString: (length: number) => string;
  /** Generate timestamp-based ID */
  uniqueId: () => string;
}

/**
 * Extended test with custom fixtures
 */
export const test = base.extend<CustomFixtures>({
  // Journey page with automatic logging
  journeyPage: async ({ page }, use, testInfo) => {
    const journeyId = testInfo.title.replace(/\s+/g, '-').toLowerCase();
    
    // Log journey start
    logJourneyStart(journeyId, testInfo.title);
    const startTime = Date.now();
    
    // Use the page
    await use(page);
    
    // Log journey completion
    const status = testInfo.status === 'passed' ? 'passed' : 'failed';
    logJourneyComplete(journeyId, status, Date.now() - startTime);
  },

  // Test data generator
  testData: async ({}, use) => {
    const generator: TestDataGenerator = {
      email: () => `test-${Date.now()}@example.com`,
      username: () => `user_${Date.now()}`,
      randomString: (length: number) => {
        const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
          result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
      },
      uniqueId: () => `id_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    };
    await use(generator);
  },

  // Journey context for step tracking
  journeyContext: async ({}, use, testInfo) => {
    const context: JourneyContext = {
      journeyId: testInfo.title.replace(/\s+/g, '-').toLowerCase(),
      startTime: Date.now(),
      stepsCompleted: 0,
      addStep: function() {
        this.stepsCompleted++;
      },
    };
    await use(context);
  },
});

/**
 * Re-export expect from base
 */
export { expect } from '@playwright/test';

/**
 * Journey test helper decorator
 * Wraps a test with journey logging
 */
export function journeyTest(
  name: string,
  tags: string[],
  testFn: (fixtures: { page: Page; testData: TestDataGenerator }) => Promise<void>
) {
  const tagString = tags.join(' ');
  test(`${name} ${tagString}`, async ({ journeyPage, testData }) => {
    await testFn({ page: journeyPage, testData });
  });
}

