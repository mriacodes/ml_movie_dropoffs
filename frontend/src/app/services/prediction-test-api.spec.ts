import { TestBed } from '@angular/core/testing';

import { PredictionTestApi } from './prediction-test-api';

describe('PredictionTestApi', () => {
  let service: PredictionTestApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredictionTestApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
