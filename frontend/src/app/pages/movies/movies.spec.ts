import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MoviesComponent } from './movies';

describe('MoviesComponent', () => {
  let component: MoviesComponent;
  let fixture: ComponentFixture<MoviesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MoviesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MoviesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load movies on init', () => {
    expect(component.movies().length).toBeGreaterThan(0);
  });

  it('should filter movies by genre', () => {
    component.updateFilter('genre', 'Action');
    const actionMovies = component.filteredMovies().filter(movie => 
      movie.genre.includes('Action')
    );
    expect(component.filteredMovies().length).toBe(actionMovies.length);
  });

  it('should calculate prediction colors correctly', () => {
    expect(component.getPredictionColor(90)).toBe('success');
    expect(component.getPredictionColor(70)).toBe('warning');
    expect(component.getPredictionColor(50)).toBe('info');
    expect(component.getPredictionColor(30)).toBe('error');
  });
});
