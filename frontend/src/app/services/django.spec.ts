import { TestBed } from '@angular/core/testing';

import { Django } from './django';

describe('Django', () => {
  let service: Django;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Django);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
