import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SurveyComponent } from './survey';

describe('SurveyComponent', () => {
  let component: SurveyComponent;
  let fixture: ComponentFixture<SurveyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SurveyComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SurveyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should start at step 0', () => {
    expect(component.currentStep()).toBe(0);
  });

  it('should have 12 questions', () => {
    expect(component.questions.length).toBe(12);
  });

  it('should calculate progress correctly', () => {
    expect(component.progress).toBe(100 / 12); // First question
  });
});
