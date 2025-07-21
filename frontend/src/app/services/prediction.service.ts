import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

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


  riskLevel?: string;
  recommendations?: string[];
  confidence?: number;
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
  // private apiUrl = 'http://localhost:8000';
  private apiUrl = 'http://localhost:8000/predict/';
    private testApiUrl = 'http://localhost:8000';
      private tmdbApiKey = '9bedd8178358fe73088aaca74b58c6a8'; // Replace with your actual TMDb API key
  private tmdbBaseUrl = 'https://api.themoviedb.org/3';
  private apiUrl2 = 'http://localhost:8000/';

  
    constructor(private http: HttpClient) {}
  
    // Transforms raw survey data to match backend expectations
   transformSurveyToApiFormat(surveyResponses: any): UserSurveyData {
  const expectedFields = [
    'attention_span_score',
    'patience_score',
    'social_influence_score',
    'genre_completion_ratio',
    'is_weekend',
    'total_genres_stopped',
    'total_multitasking_behaviors',
    'total_stopping_reasons',
    'boring_plot',
    'do_you_usually_do_other_things_while_watching_movies_i_chat_or_text_with_others',
    'do_you_usually_do_other_things_while_watching_movies_no_i_usually_focus_only_on_the_movie',
    'how_do_you_usually_discover_movies_you_decide_to_watch_reviews_or_ratings',
    'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_distractions_or_interruptions',
    'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_technical_issues_buffering_audio_etc.',
    'where_do_you_usually_watch_movies_streaming_at_home_netflix_disney+_etc.',
    'which_genres_do_you_enjoy_watching_the_most_action',
    'which_genres_do_you_enjoy_watching_the_most_romance',
    'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_action',
    'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical',
    'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_romance',
    'why_do_you_usually_choose_to_watch_movies_awards_or_critical_acclaim',
    'why_do_you_usually_choose_to_watch_movies_trailer_or_promotional_material',
    'why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested',
    'why_do_you_usually_pause_the_movie_lost_focus_or_distracted',
    'why_do_you_usually_pause_the_movie_to_discuss_something_with_others_watching'
  ];

  // Start with empty object
  const data: UserSurveyData = {};

  // 1. Normalize input values from raw form
  Object.keys(surveyResponses).forEach(key => {
    let value = surveyResponses[key];
    if (typeof value === 'boolean') {
      value = value ? 1 : 0;
    }
    (data as any)[key] = value;
  });

  // 2. Add computed/default fields if missing
  const computedDefaults = {
    total_genres_stopped: 2,
    total_stopping_reasons: 3,
    genre_completion_ratio: 0.6,
    patience_score: 0.5,
    attention_span_score: 0.5,
    total_multitasking_behaviors: 2,
    social_influence_score: 5,
    is_weekend: new Date().getDay() === 0 || new Date().getDay() === 6 ? 1 : 0
  };

  Object.keys(computedDefaults).forEach(key => {
    if (!(key in data) || data[key as keyof UserSurveyData] === undefined) {
      (data as any)[key] = (computedDefaults as any)[key];
    }
  });

  // 3. Ensure all expected fields are present for the API
  const apiFormatted: UserSurveyData = {} as any;

  for (const field of expectedFields) {
    if (field in data) {
      apiFormatted[field as keyof UserSurveyData] = data[field as keyof UserSurveyData];

    } else {
      console.warn(`Missing optional field: ${field}`);
      apiFormatted[field as keyof UserSurveyData] = 0; // Fallback (boolean converted to 0)
    }
  }

  return apiFormatted;
}

  
    // Make POST request to FastAPI backend
    // predictDropoff(data: UserSurveyData): Observable<PredictionResponse> {
    //   return this.http.post<PredictionResponse>(this.apiUrl, data);
    // }
  
  //   predictDropoff(userData: UserSurveyData): Observable<PredictionResponse> {
  //     const headers = new HttpHeaders({
  //       'Content-Type': 'application/json',
  //     });
  
  //     return this.http.post<PredictionResponse>(
  //       `${this.apiUrl}/predict`,
  //       userData,
  //       { headers }
  //     );
  //   } //version 1 , 

  //    predictDropoff(userData: UserSurveyData): Observable<PredictionResponse> {
  //   const headers = new HttpHeaders({
  //     'Content-Type': 'application/json',
  //   });

  //   return this.http.post<PredictionResponse>(
  //     `${this.apiUrl}/predict`, 
  //     userData, 
  //     { headers }
  //   );
  // } //version 2

  predictDropoff(userData: UserSurveyData): Observable<PredictionResponse> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });

    return this.http.post<PredictionResponse>(
      `${this.apiUrl}`,
      userData,
      { headers }
    ).pipe(
      catchError(error => {
        console.error('Prediction API error:', error);
        return throwError(() => new Error('Prediction failed. Please try again later.'));
      })
    );
  }

  // constructor(private http: HttpClient) { }

  /**
   * Test API connection and health
   */
  // testConnection(): Observable<ApiHealthResponse> {
  //   return this.http.get<ApiHealthResponse>(`${this.apiUrl}/health`);
  // }

  testConnection(): Observable<boolean> {
  return this.http.get(`${this.testApiUrl}/ping`, { responseType: 'text' }).pipe(
    map(response => {
      console.log('API Connection Successful:', response);
      return true;
    }),
    catchError(error => {
      console.error('API Connection Failed:', error);
      return of(false);
    })
  );
}


  /**
   * Get prediction from user survey data
   */
 

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
  // getMovies(
  //   limit: number = 50,
  //   genre?: string,
  //   minRating?: number,
  //   yearFrom?: number,
  //   yearTo?: number
  // ): Observable<MoviesResponse> {
  //   let params: string[] = [];
  //   params.push(`limit=${limit}`);
    
  //   if (genre && genre !== 'all') {
  //     params.push(`genre=${encodeURIComponent(genre)}`);
  //   }
  //   if (minRating) {
  //     params.push(`min_rating=${minRating}`);
  //   }
  //   if (yearFrom) {
  //     params.push(`year_from=${yearFrom}`);
  //   }
  //   if (yearTo) {
  //     params.push(`year_to=${yearTo}`);
  //   }

  //   const queryString = params.length > 0 ? `?${params.join('&')}` : '';
  //   return this.http.get<MoviesResponse>(`${this.apiUrl}/movies${queryString}`);
  // }

  getMovies(limit: number = 100, genre?: string, minRating: number = 6): Observable<MoviesResponse> {
    let params = new HttpParams()
      .set('api_key', this.tmdbApiKey)
      .set('language', 'en-US')
      .set('sort_by', 'popularity.desc')
      .set('include_adult', 'false')
      .set('vote_average.gte', minRating.toString())
      .set('page', '1');

    if (genre && genre !== 'all') {
      // Genre filtering must map from name to TMDb genre ID
      const genreMap: Record<string, number> = {
        Action: 28,
        Adventure: 12,
        Animation: 16,
        Comedy: 35,
        Documentary: 99,
        Drama: 18,
        Horror: 27,
        Romance: 10749,
        'Sci-Fi': 878,
        Thriller: 53
      };

      const genreId = genreMap[genre];
      if (genreId) {
        params = params.set('with_genres', genreId.toString());
      }
    }

    return this.http.get<any>(`${this.tmdbBaseUrl}/discover/movie`, { params }).pipe(
  map((response) => {
    const movies: Movie[] = response.results.slice(0, limit).map((item: any) => ({
      id: item.id,
      title: item.title,
      genre: [], // Populate with actual names if desired
      year: item.release_date ? parseInt(item.release_date.slice(0, 4)) : 0,
      posterUrl: item.poster_path
        ? `https://image.tmdb.org/t/p/w500${item.poster_path}`
        : 'https://via.placeholder.com/500x750?text=No+Image',
      imdbRating: item.vote_average,
      description: item.overview,
    }));

    return {
  movies,
  total: response.total_results || movies.length,
  filters_applied: {
    genre: genre || null,
    min_rating: minRating ?? null,
    year_from: null,
    year_to: null,
    limit: limit
  }
};

  })
);
  }


  /**
   * Get prediction for a specific movie
   */
  predictMovieCompletion(movieId: number, userData: UserSurveyData): Observable<MoviePredictionResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return this.http.post<MoviePredictionResponse>(
      `${this.apiUrl2}movies/${movieId}/predict`,
      userData,
      { headers }
    );
  }

  /**
   * Transform survey responses to API format
   */
 
}
