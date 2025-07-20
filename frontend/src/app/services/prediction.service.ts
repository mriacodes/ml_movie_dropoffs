import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UserSurveyData {
  which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical?: number;
  why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested?: number;
  total_genres_stopped?: number;
  total_stopping_reasons?: number;
  why_do_you_usually_choose_to_watch_movies_trailer_or_promotional_material?: number;
  genre_completion_ratio?: number;
  why_do_you_usually_choose_to_watch_movies_awards_or_critical_acclaim?: number;
  why_do_you_usually_pause_the_movie_lost_focus_or_distracted?: number;
  in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_distractions_or_interruptions?: number;
  in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_technical_issues_buffering_audio_etc?: number;
  patience_score?: number;
  total_multitasking_behaviors?: number;
  do_you_usually_do_other_things_while_watching_movies_i_chat_or_text_with_others?: number;
  attention_span_score?: number;
  why_do_you_usually_pause_the_movie_to_discuss_something_with_others_watching?: number;
  social_influence_score?: number;
  do_you_usually_do_other_things_while_watching_movies_no_i_usually_focus_only_on_the_movie?: number;
  which_genres_do_you_find_yourself_stopping_more_often_before_finishing_romance?: number;
  how_do_you_usually_discover_movies_you_decide_to_watch_reviews_or_ratings?: number;
  which_genres_do_you_find_yourself_stopping_more_often_before_finishing_action?: number;
  which_genres_do_you_enjoy_watching_the_most_action?: number;
  where_do_you_usually_watch_movies_streaming_at_home_netflix_disney_etc?: number;
  which_genres_do_you_enjoy_watching_the_most_romance?: number;
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
    // Create the data object with all the actual model features
    const data: UserSurveyData = {};
    
    // Map each survey response to the corresponding model feature
    Object.keys(surveyResponses).forEach(key => {
      // Convert boolean responses to 0/1
      let value = surveyResponses[key];
      if (typeof value === 'boolean') {
        value = value ? 1 : 0;
      }
      
      // Assign to the correct property name
      (data as any)[key] = value;
    });

    // Set default values for missing fields
    const defaults = {
      total_genres_stopped: 2,
      total_stopping_reasons: 3,
      genre_completion_ratio: 0.6,
      patience_score: 0.5,
      attention_span_score: 0.5,
      total_multitasking_behaviors: 2,
      social_influence_score: 5,
      is_weekend: new Date().getDay() === 0 || new Date().getDay() === 6 ? 1 : 0
    };

    // Apply defaults for missing values
    Object.keys(defaults).forEach(key => {
      if (!(key in data) || data[key as keyof UserSurveyData] === undefined) {
        (data as any)[key] = (defaults as any)[key];
      }
    });

    return data;
  }
}
