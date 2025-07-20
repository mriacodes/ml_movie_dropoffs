import { Component, signal, computed, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

interface Movie {
  id: number;
  title: string;
  genre: string[];
  year: number;
  director: string;
  runtime: number;
  imdbRating: number;
  posterUrl: string;
  description: string;
  dropoffProbability?: number;
  completionLikelihood?: number;
}

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
  
  filters = signal<FilterOptions>({
    genre: 'all',
    sortBy: 'prediction',
    sortOrder: 'desc'
  });

  availableGenres = signal<string[]>([
    'all', 'Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 
    'Romance', 'Sci-Fi', 'Thriller', 'Animation', 'Documentary'
  ]);

  // Computed properties
  hasSurveyData = computed(() => {
    // TODO: Check if user has completed survey
    return true; // Simulated for now
  });

  ngOnInit() {
    this.loadMovies();
  }

  async loadMovies() {
    this.isLoading.set(true);
    
    try {
      // TODO: Replace with actual API call to Django backend
      // For now, we'll simulate movie data with predictions
      const simulatedMovies: Movie[] = [
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
          completionLikelihood: 92
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
          completionLikelihood: 78
        },
        {
          id: 3,
          title: "The Notebook",
          genre: ["Romance", "Drama"],
          year: 2004,
          director: "Nick Cassavetes",
          runtime: 123,
          imdbRating: 7.8,
          posterUrl: "💕",
          description: "A poor yet passionate young man falls in love with a rich young woman.",
          completionLikelihood: 45
        },
        {
          id: 4,
          title: "Avengers: Endgame",
          genre: ["Action", "Adventure", "Drama"],
          year: 2019,
          director: "Anthony Russo",
          runtime: 181,
          imdbRating: 8.4,
          posterUrl: "🦸",
          description: "The Avengers assemble once more to reverse Thanos' actions.",
          completionLikelihood: 88
        },
        {
          id: 5,
          title: "Parasite",
          genre: ["Comedy", "Drama", "Thriller"],
          year: 2019,
          director: "Bong Joon-ho",
          runtime: 132,
          imdbRating: 8.6,
          posterUrl: "🏠",
          description: "A poor family schemes to become employed by a wealthy family.",
          completionLikelihood: 73
        },
        {
          id: 6,
          title: "The Conjuring",
          genre: ["Horror", "Mystery", "Thriller"],
          year: 2013,
          director: "James Wan",
          runtime: 112,
          imdbRating: 7.5,
          posterUrl: "👻",
          description: "Paranormal investigators help a family terrorized by a dark presence.",
          completionLikelihood: 35
        }
      ];

      // Add dropoff probability (inverse of completion likelihood)
      const moviesWithPredictions = simulatedMovies.map(movie => ({
        ...movie,
        dropoffProbability: 100 - (movie.completionLikelihood || 50)
      }));

      this.movies.set(moviesWithPredictions);
      this.applyFilters();
      
    } catch (error) {
      console.error('Error loading movies:', error);
    } finally {
      this.isLoading.set(false);
    }
  }

  applyFilters() {
    let filtered = [...this.movies()];
    const currentFilters = this.filters();

    // Filter by genre
    if (currentFilters.genre !== 'all') {
      filtered = filtered.filter(movie => 
        movie.genre.includes(currentFilters.genre)
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
          comparison = a.year - b.year;
          break;
        case 'rating':
          comparison = a.imdbRating - b.imdbRating;
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
    this.applyFilters();
  }

  selectMovie(movie: Movie) {
    this.selectedMovie.set(movie);
  }

  closeMovieDetail() {
    this.selectedMovie.set(null);
  }

  getPredictionColor(likelihood: number): string {
    if (likelihood >= 80) return 'success';
    if (likelihood >= 60) return 'warning';
    if (likelihood >= 40) return 'info';
    return 'error';
  }

  getPredictionText(likelihood: number): string {
    if (likelihood >= 80) return 'Very Likely to Complete';
    if (likelihood >= 60) return 'Likely to Complete';
    if (likelihood >= 40) return 'Might Drop Off';
    return 'Likely to Drop Off';
  }

  async getPrediction(movieId: number) {
    // TODO: Call Django API to get prediction for specific movie
    // This would use the user's survey responses + movie data
    console.log(`Getting prediction for movie ${movieId}`);
  }
}
