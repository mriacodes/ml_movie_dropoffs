import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MoviesPage } from './movies-page';

describe('MoviesPage', () => {
  let component: MoviesPage;
  let fixture: ComponentFixture<MoviesPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MoviesPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MoviesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
