/**
 * State comparison utilities for gym-proj3
 */

export interface ComparisonResult {
  equal: boolean;
  report?: string;
}

/**
 * Deep compare two states, normalizing IDs
 */
export function deepCompareIdsOnly(
  initialState: any,
  currentState: any
): [boolean, string] {
  // TODO: Implement state comparison logic
  // This should normalize IDs and timestamps before comparison
  
  if (JSON.stringify(initialState) === JSON.stringify(currentState)) {
    return [true, ''];
  }
  
  return [false, 'States differ'];
}

/**
 * Normalize state by removing IDs and timestamps
 */
export function normalizeState(state: any): any {
  // TODO: Implement normalization logic
  return state;
}


