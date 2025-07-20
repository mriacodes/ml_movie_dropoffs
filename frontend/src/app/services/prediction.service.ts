import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UserSurveyData {
  boring_plot: number;
  total_stopping_reasons: number;
  stop_historical: number;
  enjoy_action: number;
  genre_completion_ratio?: number;
  patience_score?: number;
  attention_span_score?: number;
  total_multitasking_behaviors?: number;
  social_influence_score?: number;
  is_weekend?: number;
}

export interface PredictionResponse {
  input_data: UserSurveyData;
  prediction: {
    dropoff_probability: number;
    risk_level: string;
    user_segment: string;
    recommendations: string[];
    model_type: string;
    confidence_score: number;
    timestamp: string;
  };
  status: string;
}

export interface ApiHealthResponse {
  status: string;
  message: string;
  model_status: string;
  model_type: string;
  version: string;
  timestamp: string;
}

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

export interface MoviesResponse {
  movies: Movie[];
  total: number;
  filters_applied: {
    genre: string | null;
    min_rating: number | null;
    year_from: number | null;
    year_to: number | null;
    limit: number;
  };
}

export interface MoviePredictionResponse {
  movie_id: number;
  completion_likelihood: number;
  dropoff_probability: number;
  risk_level: string;
  recommendations: string[];
  confidence: number;
  factors: string[];
}

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  /**
   * Test API connection and health
   */
  testConnection(): Observable<ApiHealthResponse> {
    return this.http.get<ApiHealthResponse>(`${this.apiUrl}/health`);
  }

  /**
   * Get prediction from user survey data
   */
  predictDropoff(userData: UserSurveyData): Observable<PredictionResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return this.http.post<PredictionResponse>(
      `${this.apiUrl}/predict`, 
      userData, 
      { headers }
    );
  }

  /**
   * Run test prediction with sample data
   */
  testPrediction(): Observable<any> {
    return this.http.get(`${this.apiUrl}/test`);
  }

  /**
   * Get model information
   */
  getModelInfo(): Observable<any> {
    return this.http.get(`${this.apiUrl}/model/info`);
  }

  /**
   * Get API information
   */
  getApiInfo(): Observable<any> {
    return this.http.get(`${this.apiUrl}/`);
  }

  /**
   * Get movies from the IMDB dataset
   */
  getMovies(
    limit: number = 50,
    genre?: string,
    minRating?: number,
    yearFrom?: number,
    yearTo?: number
  ): Observable<MoviesResponse> {
    let params: string[] = [];
    params.push(`limit=${limit}`);
    
    if (genre && genre !== 'all') {
      params.push(`genre=${encodeURIComponent(genre)}`);
    }
    if (minRating) {
      params.push(`min_rating=${minRating}`);
    }
    if (yearFrom) {
      params.push(`year_from=${yearFrom}`);
    }
    if (yearTo) {
      params.push(`year_to=${yearTo}`);
    }

    const queryString = params.length > 0 ? `?${params.join('&')}` : '';
    return this.http.get<MoviesResponse>(`${this.apiUrl}/movies${queryString}`);
  }

  /**
   * Get prediction for a specific movie
   */
  predictMovieCompletion(movieId: number, userData: UserSurveyData): Observable<MoviePredictionResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return this.http.post<MoviePredictionResponse>(
      `${this.apiUrl}/movies/${movieId}/predict`,
      userData,
      { headers }
    );
  }

  /**
   * Transform survey responses to API format
   */
  transformSurveyToApiFormat(surveyResponses: any): UserSurveyData {
    return {
      boring_plot: surveyResponses.boring_plot || 0,
      total_stopping_reasons: surveyResponses.total_stopping_reasons || 3,
      stop_historical: surveyResponses.stop_historical || 0,
      enjoy_action: surveyResponses.enjoy_action || 1,
      genre_completion_ratio: surveyResponses.genre_completion_ratio || 0.5,
      patience_score: surveyResponses.patience_score || 0.5,
      attention_span_score: surveyResponses.attention_span_score || 0.5,
      total_multitasking_behaviors: surveyResponses.total_multitasking_behaviors || 2,
      social_influence_score: surveyResponses.social_influence_score || 4,
      is_weekend: surveyResponses.is_weekend || 0
    };
  }
}
