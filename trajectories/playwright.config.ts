import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for proj3 UI Journey Tests
 * 
 * This configuration supports both major and minor user journeys
 * with comprehensive browser coverage and reporting.
 */

export default defineConfig({
  // Test directory containing all journey specs
  testDir: './journeys',
  
  // Run tests in parallel for faster execution
  fullyParallel: true,
  
  // Fail the build on CI if test.only is accidentally committed
  forbidOnly: !!process.env.CI,
  
  // Retry failed tests (more retries on CI)
  retries: process.env.CI ? 2 : 0,
  
  // Number of parallel workers
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter configuration
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
    ['list'],
  ],
  
  // Global test settings
  use: {
    // Base URL for the application under test
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // Collect trace on first retry
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video recording on first retry
    video: 'on-first-retry',
    
    // Default navigation timeout
    navigationTimeout: 30000,
    
    // Default action timeout
    actionTimeout: 15000,
  },

  // Configure projects for different browsers
  projects: [
    // Desktop Browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile Browsers
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // Output directory for test artifacts
  outputDir: 'test-results/',

  // Web server configuration
  // Runs the Next.js frontend dev server for testing
  webServer: {
    command: 'npm run dev',
    cwd: '../frontend',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});

