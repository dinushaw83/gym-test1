# Trajectories - UI Journey Testing

> **Playwright-based automated testing for user journeys**

This directory contains all UI journey tests organized by priority (major/minor) for comprehensive user flow validation against the Next.js frontend.

---

## Quick Start

### Installation

```bash
cd trajectories
npm install
npx playwright install

# Ensure frontend dependencies are installed
cd ../frontend && npm install && cd ../trajectories
```

### Running Tests

```bash
# Run all tests
npm test

# Run with browser visible
npm run test:headed

# Run with Playwright UI
npm run test:ui

# Run in debug mode
npm run test:debug
```

### Filtering Tests

```bash
# Run only major journeys
npm run test:major

# Run only minor journeys
npm run test:minor

# Run smoke tests
npm run test:smoke

# Run regression tests
npm run test:regression
```

---

## Directory Structure

```
trajectories/
├── journeys/                    # All journey test specs
│   ├── major/                   # Critical user flows
│   │   └── template-page.journey.spec.ts
│   ├── minor/                   # Secondary user flows
│   │   └── page-interactions.journey.spec.ts
│   └── index.ts                 # Journey registry
├── helpers/                     # Utility modules
│   ├── types.ts                 # TypeScript type definitions
│   ├── journey-utils.ts         # Journey helper functions
│   ├── test-fixtures.ts         # Custom Playwright fixtures
│   └── index.ts                 # Central exports
├── fixtures/                    # Test data fixtures
├── reports/                     # Test reports (generated)
├── test-results/                # Test artifacts (generated)
├── playwright.config.ts         # Playwright configuration
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript config
└── README.md                    # This file
```

---

## Journey Classification

### Major Journeys (@major)
Critical user flows that must always work:
- Page loading and core functionality
- Essential user interactions
- Primary navigation paths
- Critical form submissions

### Minor Journeys (@minor)
Secondary flows that enhance UX:
- Settings and preferences
- Optional features
- Edge cases
- Accessibility checks

---

## Writing New Journeys

### 1. Create Journey Spec File

```typescript
// journeys/major/my-journey.journey.spec.ts
import { test, expect } from '@playwright/test';
import { executeStep, logJourneyStart, logJourneyComplete } from '../../helpers/journey-utils';
import { UserJourney } from '../../helpers/types';

const myJourney: UserJourney = {
  id: 'my-journey-001',
  name: 'My Journey Name',
  description: 'What this journey tests',
  priority: 'major',
  category: 'navigation',
  tags: ['@major', '@smoke'],
  steps: [
    {
      name: 'Step 1',
      description: 'What happens',
      expectedOutcome: 'Expected result',
    },
  ],
  expectedFinalState: 'Final state description',
};

test.describe('My Journey @major', () => {
  test('complete journey test @smoke', async ({ page }) => {
    // Test implementation
  });
});
```

### 2. Use Helper Functions

```typescript
import { 
  executeStep,
  safeClick,
  safeType,
  waitForElement,
  assertElementVisible,
} from '../../helpers/journey-utils';

// Execute a step with logging
await executeStep(page, step, async () => {
  await safeClick(page, 'button#submit');
});

// Safe element interaction
await safeType(page, 'input#email', 'test@example.com');

// Wait for elements
const element = await waitForElement(page, '.modal', 5000);
```

---

## Test Tags

Use tags to organize and filter tests:

| Tag | Description |
|-----|-------------|
| `@major` | Critical user flows |
| `@minor` | Secondary flows |
| `@smoke` | Quick sanity checks |
| `@regression` | Full regression suite |
| `@critical` | Must-pass tests |
| `@flaky` | Known flaky tests |
| `@slow` | Long-running tests |

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Application base URL | `http://localhost:3000` |
| `CI` | CI environment flag | - |

### Frontend Setup

The tests run against the Next.js frontend in `../frontend/`. The Playwright config automatically starts the Next.js dev server when running tests.

To run the frontend manually:
```bash
cd ../frontend
npm run dev
```

---

## Reports

After running tests, view reports:

```bash
# Open HTML report
npm run report

# Reports are saved to:
# - reports/html/index.html  (HTML report)
# - reports/results.json     (JSON results)
```

---

## Best Practices

1. **One Journey Per File** - Keep specs focused
2. **Use Descriptive Names** - Clear test names help debugging
3. **Add Tags** - Enable filtering and categorization
4. **Log Steps** - Use `executeStep()` for visibility
5. **Handle Failures Gracefully** - Use try-catch where appropriate
6. **Keep Tests Independent** - No test should depend on another
7. **Use Page Objects** - For complex pages, create PO classes

---

## Troubleshooting

### Tests failing to find elements

- Verify selectors match actual DOM
- Increase timeouts if page loads slowly
- Use `test:debug` to step through tests

### Browser not installed

```bash
npx playwright install chromium
```

### Port conflicts

Update `BASE_URL` in environment or config.

---

## Related Documentation

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Testing Best Practices](https://playwright.dev/docs/best-practices)

