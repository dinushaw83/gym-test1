import { test, expect } from '@playwright/test';
import { 
  executeStep, 
  logJourneyStart, 
  logJourneyComplete,
} from '../../helpers/journey-utils';
import { UserJourney } from '../../helpers/types';

/**
 * Page Interactions Journey - Minor User Flow
 * 
 * This journey tests secondary user flows and interactions
 * on the template page.
 * 
 * Tags: @minor @regression
 */

// Define the journey metadata
const interactionsJourney: UserJourney = {
  id: 'interactions-001',
  name: 'Page Interactions Journey',
  description: 'Tests page interactions and state management',
  priority: 'minor',
  category: 'navigation',
  tags: ['@minor', '@regression'],
  preconditions: [
    'Application is running',
    'Page is accessible',
  ],
  steps: [
    {
      name: 'Access Page',
      description: 'Navigate to the main page',
      expectedOutcome: 'Page is displayed',
    },
    {
      name: 'Verify Page Elements',
      description: 'Check all elements are rendered',
      expectedOutcome: 'All elements are visible',
    },
    {
      name: 'Test Page State',
      description: 'Verify page maintains state',
      expectedOutcome: 'Page state is consistent',
    },
    {
      name: 'Verify No Console Errors',
      description: 'Check for JavaScript errors',
      expectedOutcome: 'No console errors',
    },
  ],
  expectedFinalState: 'Page is stable and error-free',
};

test.describe('Page Interactions Journey @minor @regression', () => {

  test.beforeEach(async ({ page }) => {
    logJourneyStart(interactionsJourney.id, interactionsJourney.name);
  });

  test('User can view and interact with page elements @minor', async ({ page }) => {
    const startTime = Date.now();

    // Step 1: Navigate to the main page
    await executeStep(page, interactionsJourney.steps[0], async () => {
      await page.goto('/');
      await page.waitForLoadState('domcontentloaded');
    });

    // Step 2: Verify all elements are rendered
    await executeStep(page, interactionsJourney.steps[1], async () => {
      // Check heading
      const heading = page.locator('h1');
      await expect(heading).toBeVisible();
      console.log('   ✓ Heading is visible');
      
      // Check description
      const description = page.locator('p');
      await expect(description).toBeVisible();
      console.log('   ✓ Description is visible');
      
      // Check container
      const container = page.locator('.min-h-screen');
      await expect(container).toBeVisible();
      console.log('   ✓ Main container is visible');
    });

    // Step 3: Test page state
    await executeStep(page, interactionsJourney.steps[2], async () => {
      // Get initial content
      const initialHeadingText = await page.locator('h1').textContent();
      
      // Reload page
      await page.reload();
      await page.waitForLoadState('domcontentloaded');
      
      // Verify content is the same
      const reloadedHeadingText = await page.locator('h1').textContent();
      expect(reloadedHeadingText).toBe(initialHeadingText);
      console.log('   ✓ Page state is consistent after reload');
    });

    // Step 4: Verify no console errors
    await executeStep(page, interactionsJourney.steps[3], async () => {
      const errors: string[] = [];
      page.on('pageerror', error => errors.push(error.message));
      
      // Navigate and wait for any errors
      await page.reload();
      await page.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(500);
      
      if (errors.length > 0) {
        console.log(`   ⚠️ Console errors found: ${errors.length}`);
        errors.forEach(e => console.log(`      - ${e}`));
      } else {
        console.log('   ✓ No console errors');
      }
      
      expect(errors.length).toBe(0);
    });

    logJourneyComplete(interactionsJourney.id, 'passed', Date.now() - startTime);
  });

  test('Page maintains state during navigation @minor', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Get initial page state
    const initialUrl = page.url();
    const initialTitle = await page.title();

    // Verify URL structure
    expect(initialUrl).toContain('localhost:3000');
    console.log(`   URL: ${initialUrl}`);
    console.log(`   Title: ${initialTitle}`);

    // Verify page has expected content
    const heading = page.locator('h1');
    await expect(heading).toContainText('Welcome to proj3');
    
    console.log('   ✓ Page state verified');
  });

  test('Page has proper styling applied @minor', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Verify Tailwind CSS classes are applied
    const container = page.locator('.min-h-screen');
    await expect(container).toHaveClass(/flex/);
    await expect(container).toHaveClass(/items-center/);
    await expect(container).toHaveClass(/justify-center/);
    console.log('   ✓ Flex centering classes applied');

    // Verify background styling
    await expect(container).toHaveClass(/bg-gray-50/);
    console.log('   ✓ Background color class applied');

    // Verify heading styling
    const heading = page.locator('h1');
    await expect(heading).toHaveClass(/text-4xl/);
    await expect(heading).toHaveClass(/font-bold/);
    console.log('   ✓ Heading typography classes applied');

    // Verify description styling
    const description = page.locator('p');
    await expect(description).toHaveClass(/text-gray-600/);
    console.log('   ✓ Description text color applied');
  });
});

