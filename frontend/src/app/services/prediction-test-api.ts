import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PredictionResponse {
  prediction: {
    dropoff_probability: number;
    risk_level: string;
  };
}

export interface UserSurveyData {
  [key: string]: any;
}

export interface PredictionResponse2 {
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


@Injectable({
  providedIn: 'root'
})
export class PredictionTestApi {
  private apiUrl = 'http://localhost:8000/predict';

  constructor(private http: HttpClient) {}

  // Transforms raw survey data to match backend expectations
  transformSurveyToApiFormat(data: UserSurveyData): UserSurveyData {
    const expectedFields = [
      'attention_span_score',
      'patience_score',
      'social_influence_score',
      'genre_completion_ratio',
      'is_weekend',
      'total_genres_stopped',
      'total_multitasking_behaviors',
      'total_stopping_reasons',
      'boring_plot',  // required by backend!
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

    const apiFormatted: any = {};
    for (const field of expectedFields) {
      if (field in data) {
        apiFormatted[field] = data[field];
      } else {
        console.warn(`Missing optional field: ${field}`);
        // Provide a fallback if necessary
        apiFormatted[field] = false;
      }
    }

    return apiFormatted;
  }

  // Make POST request to FastAPI backend
  // predictDropoff(data: UserSurveyData): Observable<PredictionResponse> {
  //   return this.http.post<PredictionResponse>(this.apiUrl, data);
  // }

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
}