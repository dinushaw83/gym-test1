import { test, expect } from '@playwright/test';
import { 
  executeStep, 
  logJourneyStart, 
  logJourneyComplete,
} from '../../helpers/journey-utils';
import { UserJourney } from '../../helpers/types';

/**
 * Template Page Journey - Major User Flow
 * 
 * This journey tests the core functionality of the Next.js template UI page,
 * ensuring all critical elements are present and interactive.
 * 
 * Tags: @major @smoke @critical
 */

// Define the journey metadata
const templatePageJourney: UserJourney = {
  id: 'template-page-001',
  name: 'Template Page Core Journey',
  description: 'Validates the Next.js template UI page loads correctly with all essential components',
  priority: 'major',
  category: 'navigation',
  tags: ['@major', '@smoke', '@critical'],
  preconditions: [
    'Next.js dev server is running',
    'No user authentication required for landing page',
  ],
  steps: [
    {
      name: 'Navigate to Template Page',
      description: 'User navigates to the main template page URL',
      expectedOutcome: 'Page loads successfully with status 200',
    },
    {
      name: 'Verify Page Title',
      description: 'Check that the page title is correct',
      expectedOutcome: 'Title contains proj3',
    },
    {
      name: 'Verify Welcome Heading',
      description: 'Validate the welcome heading is visible',
      expectedOutcome: 'H1 with "Welcome to proj3" is visible',
    },
    {
      name: 'Verify Description Text',
      description: 'Check the skeleton description text',
      expectedOutcome: 'Description paragraph is visible',
    },
    {
      name: 'Verify Page Layout',
      description: 'Page should be properly rendered with centered layout',
      expectedOutcome: 'No visual regressions or layout breaks',
    },
  ],
  expectedFinalState: 'Template page is fully loaded and displays welcome message',
};

test.describe('Template Page Journey @major @smoke', () => {
  
  test.beforeEach(async ({ page }) => {
    logJourneyStart(templatePageJourney.id, templatePageJourney.name);
  });

  test('Complete template page core user journey @critical', async ({ page }) => {
    const startTime = Date.now();
    let stepsCompleted = 0;

    // Step 1: Navigate to Template Page
    await executeStep(page, templatePageJourney.steps[0], async () => {
      const response = await page.goto('/');
      expect(response?.status()).toBeLessThan(400);
      await page.waitForLoadState('domcontentloaded');
    });
    stepsCompleted++;

    // Step 2: Verify Page Title
    await executeStep(page, templatePageJourney.steps[1], async () => {
      await expect(page).toHaveTitle(/proj3/);
    });
    stepsCompleted++;

    // Step 3: Verify Welcome Heading
    await executeStep(page, templatePageJourney.steps[2], async () => {
      const heading = page.locator('h1');
      await expect(heading).toBeVisible();
      await expect(heading).toContainText('Welcome to proj3');
    });
    stepsCompleted++;

    // Step 4: Verify Description Text
    await executeStep(page, templatePageJourney.steps[3], async () => {
      const description = page.locator('p');
      await expect(description).toBeVisible();
      await expect(description).toContainText('skeleton frontend application');
    });
    stepsCompleted++;

    // Step 5: Verify Page Layout
    await executeStep(page, templatePageJourney.steps[4], async () => {
      // Verify centered layout container exists
      const container = page.locator('.min-h-screen');
      await expect(container).toBeVisible();
      
      // Verify text-center styling is applied
      const textCenter = page.locator('.text-center');
      await expect(textCenter).toBeVisible();
      
      // Take a screenshot for visual verification
      await page.screenshot({ 
        path: `test-results/template-page-final-${Date.now()}.png`,
        fullPage: true 
      });
    });
    stepsCompleted++;

    // Log journey completion
    logJourneyComplete(
      templatePageJourney.id, 
      'passed', 
      Date.now() - startTime
    );
    
    expect(stepsCompleted).toBe(templatePageJourney.steps.length);
  });

  test('Template page loads within acceptable time @major', async ({ page }) => {
    // Warm up - first request may be slow due to Next.js compilation
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    
    // Measure actual page reload time
    const startTime = Date.now();
    await page.reload();
    await page.waitForLoadState('domcontentloaded');
    
    const loadTime = Date.now() - startTime;
    console.log(`   Page reload time: ${loadTime}ms`);
    
    // Page reload should complete within 5 seconds
    expect(loadTime).toBeLessThan(5000);
  });

  test('Template page has correct HTML structure @major', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    
    // Check for correct HTML lang attribute
    const html = page.locator('html');
    const langAttr = await html.getAttribute('lang');
    expect(langAttr).toBe('en');
    console.log(`   Page language: ${langAttr}`);
    
    // Check page structure
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Verify heading hierarchy
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBe(1);
    console.log(`   H1 elements: ${h1Count}`);
    
    // Verify the main content div structure
    const mainContainer = page.locator('div.min-h-screen');
    await expect(mainContainer).toBeVisible();
    console.log('   ✓ Main container with Tailwind classes found');
  });

  test('Template page is responsive @major', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    
    // Test at different viewport sizes
    const viewports = [
      { width: 1920, height: 1080, name: 'Desktop HD' },
      { width: 1280, height: 720, name: 'Desktop' },
      { width: 768, height: 1024, name: 'Tablet' },
      { width: 375, height: 667, name: 'Mobile' },
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      // Verify content is still visible at each size
      const heading = page.locator('h1');
      await expect(heading).toBeVisible();
      
      console.log(`   ✓ ${viewport.name} (${viewport.width}x${viewport.height}): Content visible`);
    }
  });
});

