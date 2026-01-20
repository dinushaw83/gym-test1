/**
 * Journey Tests Index
 * 
 * This file exports journey definitions for documentation and reporting purposes.
 * Actual tests are in the respective .spec.ts files.
 */

import { UserJourney } from '../helpers/types';

/**
 * Major Journeys Registry
 * Critical user flows that must always work
 */
export const majorJourneys: UserJourney[] = [
  {
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
        expectedOutcome: 'Title contains application name',
      },
      {
        name: 'Verify Welcome Heading',
        description: 'Validate the welcome heading is visible',
        expectedOutcome: 'H1 with welcome message is visible',
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
  },
];

/**
 * Minor Journeys Registry
 * Secondary flows that enhance user experience
 */
export const minorJourneys: UserJourney[] = [
  {
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
  },
];

/**
 * Get all registered journeys
 */
export function getAllJourneys(): UserJourney[] {
  return [...majorJourneys, ...minorJourneys];
}

/**
 * Get journeys by priority
 */
export function getJourneysByPriority(priority: 'major' | 'minor'): UserJourney[] {
  return priority === 'major' ? majorJourneys : minorJourneys;
}

/**
 * Get journey by ID
 */
export function getJourneyById(id: string): UserJourney | undefined {
  return getAllJourneys().find(j => j.id === id);
}

