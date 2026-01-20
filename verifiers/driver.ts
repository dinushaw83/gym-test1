/**
 * Verifier driver for gym-proj3
 * Uses framework verifier client
 */

// TODO: Import framework verifier client when available
// import { VerifierClient } from '@ui-gym/framework';
import type { AppState } from '../types';

// Example verifier driver
export class proj3VerifierDriver {
  // TODO: Initialize with framework verifier client
  // private verifierClient: VerifierClient;

  constructor() {
    // TODO: Initialize verifier client
    // this.verifierClient = new VerifierClient('proj3', this.extractState);
  }

  /**
   * Extract state from app state for verification
   */
  private extractState(appState: AppState) {
    return {
      domain: appState.domainState,
      ui: appState.uiState,
    };
  }

  /**
   * Run a verifier
   */
  async runVerifier(verifierNumber: number, currentState: AppState) {
    // TODO: Implement using framework verifier client
    // return await this.verifierClient.runVerifier(verifierNumber, currentState);
    throw new Error('Verifier client not yet implemented');
  }
}


