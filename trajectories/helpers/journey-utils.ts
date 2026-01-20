import { Page, expect, Locator } from '@playwright/test';
import { JourneyStep, JourneyResult } from './types';

/**
 * Journey Utilities
 * 
 * Helper functions for managing user journey tests
 */

/**
 * Execute a journey step with logging and error handling
 */
export async function executeStep(
  page: Page,
  step: JourneyStep,
  action: () => Promise<void>
): Promise<void> {
  console.log(`📍 Step: ${step.name}`);
  console.log(`   Description: ${step.description}`);
  
  try {
    await action();
    console.log(`   ✅ Expected: ${step.expectedOutcome}`);
  } catch (error) {
    console.error(`   ❌ Step failed: ${step.name}`);
    throw error;
  }
}

/**
 * Wait for element to be visible with custom timeout
 */
export async function waitForElement(
  page: Page,
  selector: string,
  timeout: number = 10000
): Promise<Locator> {
  const element = page.locator(selector);
  await element.waitFor({ state: 'visible', timeout });
  return element;
}

/**
 * Safe click with retry mechanism
 */
export async function safeClick(
  page: Page,
  selector: string,
  options: { timeout?: number; retries?: number } = {}
): Promise<void> {
  const { timeout = 10000, retries = 3 } = options;
  
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await page.locator(selector).click({ timeout });
      return;
    } catch (error) {
      if (attempt === retries) throw error;
      console.log(`   Retry ${attempt}/${retries} for click on ${selector}`);
      await page.waitForTimeout(500);
    }
  }
}

/**
 * Safe text input with clearing
 */
export async function safeType(
  page: Page,
  selector: string,
  text: string,
  options: { clear?: boolean; timeout?: number } = {}
): Promise<void> {
  const { clear = true, timeout = 10000 } = options;
  
  const element = page.locator(selector);
  await element.waitFor({ state: 'visible', timeout });
  
  if (clear) {
    await element.clear();
  }
  
  await element.fill(text);
}

/**
 * Take a named screenshot for documentation
 */
export async function takeNamedScreenshot(
  page: Page,
  name: string,
  journeyId: string
): Promise<string> {
  const filename = `${journeyId}-${name}-${Date.now()}.png`;
  await page.screenshot({ 
    path: `test-results/screenshots/${filename}`,
    fullPage: false 
  });
  return filename;
}

/**
 * Assert page URL contains expected path
 */
export async function assertUrlContains(
  page: Page,
  expectedPath: string
): Promise<void> {
  await expect(page).toHaveURL(new RegExp(expectedPath));
}

/**
 * Assert element text matches expected value
 */
export async function assertElementText(
  page: Page,
  selector: string,
  expectedText: string | RegExp
): Promise<void> {
  const element = page.locator(selector);
  await expect(element).toHaveText(expectedText);
}

/**
 * Assert element is visible on page
 */
export async function assertElementVisible(
  page: Page,
  selector: string
): Promise<void> {
  const element = page.locator(selector);
  await expect(element).toBeVisible();
}

/**
 * Wait for network idle (no pending requests)
 */
export async function waitForNetworkIdle(
  page: Page,
  timeout: number = 5000
): Promise<void> {
  await page.waitForLoadState('networkidle', { timeout });
}

/**
 * Generate journey result summary
 */
export function generateJourneyResult(
  journeyId: string,
  status: 'passed' | 'failed' | 'skipped',
  startTime: number,
  stepsCompleted: number,
  totalSteps: number,
  error?: string
): JourneyResult {
  return {
    journeyId,
    status,
    duration: Date.now() - startTime,
    stepsCompleted,
    totalSteps,
    error,
  };
}

/**
 * Log journey start
 */
export function logJourneyStart(journeyId: string, journeyName: string): void {
  console.log('\n' + '═'.repeat(60));
  console.log(`🚀 Starting Journey: ${journeyName}`);
  console.log(`   ID: ${journeyId}`);
  console.log('═'.repeat(60) + '\n');
}

/**
 * Log journey completion
 */
export function logJourneyComplete(
  journeyId: string,
  status: 'passed' | 'failed',
  duration: number
): void {
  const emoji = status === 'passed' ? '✅' : '❌';
  console.log('\n' + '─'.repeat(60));
  console.log(`${emoji} Journey Complete: ${journeyId}`);
  console.log(`   Status: ${status.toUpperCase()}`);
  console.log(`   Duration: ${duration}ms`);
  console.log('─'.repeat(60) + '\n');
}

