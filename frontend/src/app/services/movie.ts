import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

export interface Movie {
  id: number;
  title: string;
  genre: string[];
  year: number;
  director: string;
  runtime: number;
  imdbRating: number;
  posterUrl: string;
  description: string;
  mainGenre: string;
  contentRating: string;
  starCast: string;
  completionLikelihood?: number;
  dropoffProbability?: number;
}

export interface UserSurveyData {
  favoriteGenres: string[];
  averageWatchTime: number;
  attentionSpan: number;
}

export interface MoviesResponse {
  movies: Movie[];
}


@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiKey = '9bedd8178358fe73088aaca74b58c6a8';
  // private baseUrl = 'https://api.themoviedb.org/3';
  private baseUrl = 'https://api.example.com/predict'; // replace with your actual prediction API
  private tmdbApiKey = '9bedd8178358fe73088aaca74b58c6a8'; // 🔑 Replace this with your TMDb API key
  private tmdbBaseUrl = 'https://api.themoviedb.org/3';

  constructor(private http: HttpClient) {}

  getMovies(limit: number, genre: string, minRating: number): Observable<MoviesResponse> {
    const url = `${this.baseUrl}/movies?limit=${limit}&genre=${genre}&minRating=${minRating}`;
    return this.http.get<MoviesResponse>(url);
  }

  predictMovieCompletion(movieId: number, userData: UserSurveyData): Observable<any> {
    const url = `${this.baseUrl}/completion`;
    return this.http.post(url, { movieId, userData });
  }

  getMoviesFromTMDb(count: number = 6): Observable<any> {
    const url = `${this.tmdbBaseUrl}/movie/popular?api_key=${this.tmdbApiKey}&language=en-US&page=1`;
    return this.http.get<any>(url);
  }

  // (Optional) fetch genres list if you want to map genre_ids to names
  getTMDbGenres(): Observable<any> {
    const url = `${this.tmdbBaseUrl}/genre/movie/list?api_key=${this.tmdbApiKey}&language=en-US`;
    return this.http.get<any>(url);
  }

  getPopularMovies() {
    return this.http.get<any>(`${this.baseUrl}/movie/popular?api_key=${this.apiKey}`)
      .pipe(
        map(res => res.results.map((movie: { id: any; title: any; overview: any; poster_path: any; }) => ({
          id: movie.id,
          title: movie.title,
          overview: movie.overview,
          posterPath: `https://image.tmdb.org/t/p/w500${movie.poster_path}`,
          completionLikelihood: Math.floor(Math.random() * 100) + 1
        })))
      );
  }
}
