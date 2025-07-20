import { Component, signal, computed, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { PredictionService, Movie, MoviesResponse, UserSurveyData } from '../../services/prediction.service';

interface FilterOptions {
  genre: string;
  sortBy: 'title' | 'year' | 'rating' | 'prediction';
  sortOrder: 'asc' | 'desc';
}

@Component({
  selector: 'app-movies',
  imports: [RouterLink, CommonModule],
  templateUrl: './movies.html',
  styleUrl: './movies.scss'
})
export class MoviesComponent implements OnInit {
  isLoading = signal(false);
  movies = signal<Movie[]>([]);
  filteredMovies = signal<Movie[]>([]);
  selectedMovie = signal<Movie | null>(null);
  errorMessage = signal<string | null>(null);
  userSurveyData = signal<UserSurveyData | null>(null);
  
  filters = signal<FilterOptions>({
    genre: 'all',
    sortBy: 'rating',
    sortOrder: 'desc'
  });

  availableGenres = signal<string[]>([
    'all', 'Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 
    'Romance', 'Sci-Fi', 'Thriller', 'Animation', 'Documentary'
  ]);

  constructor(private predictionService: PredictionService) {}

  // Computed properties
  hasSurveyData = computed(() => {
    // Check if user has completed survey data in session storage
    const surveyData = sessionStorage.getItem('userSurveyData');
    if (surveyData) {
      try {
        this.userSurveyData.set(JSON.parse(surveyData));
        return true;
      } catch {
        return false;
      }
    }
    return false;
  });

  ngOnInit() {
    this.loadMovies();
  }

  async loadMovies() {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    
    try {
      // Get movies from the real API
      this.predictionService.getMovies(100, this.filters().genre, 6.0).subscribe({
        next: (response: MoviesResponse) => {
          console.log('Loaded movies from API:', response);
          this.movies.set(response.movies);
          
          // If user has survey data, get predictions for movies
          if (this.hasSurveyData() && this.userSurveyData()) {
            this.loadMoviePredictions();
          } else {
            this.applyFilters();
          }
          
          this.isLoading.set(false);
        },
        error: (error) => {
          console.error('Error loading movies:', error);
          this.errorMessage.set('Failed to load movies from API. Using sample data.');
          this.loadFallbackMovies();
          this.isLoading.set(false);
        }
      });
      
    } catch (error) {
      console.error('Error loading movies:', error);
      this.errorMessage.set('Failed to load movies. Using sample data.');
      this.loadFallbackMovies();
      this.isLoading.set(false);
    }
  }

  loadFallbackMovies() {
    // Fallback static data for when API is not available
    const fallbackMovies: Movie[] = [
      {
        id: 1,
        title: "The Matrix",
        genre: ["Action", "Sci-Fi"],
        year: 1999,
        director: "The Wachowskis",
        runtime: 136,
        imdbRating: 8.7,
        posterUrl: "🎬",
        description: "A computer hacker learns from mysterious rebels about the true nature of his reality.",
        mainGenre: "Action",
        contentRating: "R",
        starCast: "Keanu Reeves, Laurence Fishburne",
        completionLikelihood: 92,
        dropoffProbability: 8
      },
      {
        id: 2,
        title: "Inception",
        genre: ["Action", "Sci-Fi", "Thriller"],
        year: 2010,
        director: "Christopher Nolan",
        runtime: 148,
        imdbRating: 8.8,
        posterUrl: "🎭",
        description: "A thief who steals corporate secrets through dream-sharing technology.",
        mainGenre: "Sci-Fi",
        contentRating: "PG-13",
        starCast: "Leonardo DiCaprio, Marion Cotillard",
        completionLikelihood: 78,
        dropoffProbability: 22
      }
    ];
    
    this.movies.set(fallbackMovies);
    this.applyFilters();
  }

  async loadMoviePredictions() {
    const userData = this.userSurveyData();
    if (!userData) return;

    const moviesWithPredictions = await Promise.all(
      this.movies().map(async (movie) => {
        try {
          const prediction = await this.predictionService.predictMovieCompletion(movie.id, userData).toPromise();
          return {
            ...movie,
            completionLikelihood: Math.round((prediction?.completion_likelihood || 0.5) * 100),
            dropoffProbability: Math.round((prediction?.dropoff_probability || 0.5) * 100)
          };
        } catch (error) {
          console.error(`Error predicting for movie ${movie.title}:`, error);
          // Return movie with default prediction
          return {
            ...movie,
            completionLikelihood: 50,
            dropoffProbability: 50
          };
        }
      })
    );

    this.movies.set(moviesWithPredictions);
    this.applyFilters();
  }

  applyFilters() {
    let filtered = [...this.movies()];
    const currentFilters = this.filters();

    // Filter by genre
    if (currentFilters.genre !== 'all') {
      filtered = filtered.filter(movie => 
        movie.genre.some(g => g.toLowerCase().includes(currentFilters.genre.toLowerCase()))
      );
    }

    // Sort movies
    filtered.sort((a, b) => {
      let comparison = 0;
      
      switch (currentFilters.sortBy) {
        case 'title':
          comparison = a.title.localeCompare(b.title);
          break;
        case 'year':
          comparison = (a.year || 0) - (b.year || 0);
          break;
        case 'rating':
          comparison = (a.imdbRating || 0) - (b.imdbRating || 0);
          break;
        case 'prediction':
          comparison = (a.completionLikelihood || 0) - (b.completionLikelihood || 0);
          break;
      }
      
      return currentFilters.sortOrder === 'desc' ? -comparison : comparison;
    });

    this.filteredMovies.set(filtered);
  }

  updateFilter(key: keyof FilterOptions, value: any) {
    this.filters.update(filters => ({
      ...filters,
      [key]: value
    }));
    
    // If genre filter changed, reload movies to get fresh data
    if (key === 'genre') {
      this.loadMovies();
    } else {
      this.applyFilters();
    }
  }

  selectMovie(movie: Movie) {
    this.selectedMovie.set(movie);
  }

  closeMovieDetails() {
    this.selectedMovie.set(null);
  }

  getCompletionColor(likelihood: number | undefined): string {
    if (!likelihood) return 'var(--color-gray-400)';
    
    if (likelihood >= 80) return 'var(--color-success)';
    if (likelihood >= 60) return 'var(--color-warning)';
    if (likelihood >= 40) return 'var(--color-primary-medium)';
    return 'var(--color-danger)';
  }

  getRiskLevel(likelihood: number | undefined): string {
    if (!likelihood) return 'Unknown';
    
    if (likelihood >= 80) return 'Very High';
    if (likelihood >= 60) return 'High'; 
    if (likelihood >= 40) return 'Medium';
    return 'Low';
  }

  refreshMovies() {
    this.loadMovies();
  }
}
