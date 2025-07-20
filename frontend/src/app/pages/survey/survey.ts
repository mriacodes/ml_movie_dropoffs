import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PredictionService, UserSurveyData, PredictionResponse } from '../../services/prediction.service';

interface SurveyQuestion {
  id: string;
  question: string;
  type: 'boolean' | 'integer' | 'multiple_choice';
  options?: any[];
  fieldName: string;
}

interface SurveyResponse {
  [key: string]: any;
}

@Component({
  selector: 'app-survey',
  imports: [CommonModule, FormsModule],
  templateUrl: './survey.html',
  styleUrl: './survey.scss'
})
export class SurveyComponent {
  currentStep = signal(0);
  responses = signal<SurveyResponse>({});
  isSubmitting = signal(false);
  predictionResult = signal<PredictionResponse | null>(null);
  
  constructor(
    private predictionService: PredictionService,
    private router: Router
  ) {}
  
  // Survey questions based on the actual ML model's features
  questions: SurveyQuestion[] = [
    {
      id: '1',
      question: 'Do you often stop watching Historical movies before finishing?',
      type: 'boolean',
      fieldName: 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical'
    },
    {
      id: '2',
      question: 'Do you pause movies when feeling bored or uninterested?',
      type: 'boolean',
      fieldName: 'why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested'
    },
    {
      id: '3',
      question: 'How many different genres do you usually stop watching before finishing?',
      type: 'integer',
      options: [0, 1, 2, 3, 4, 5],
      fieldName: 'total_genres_stopped'
    },
    {
      id: '4', 
      question: 'How many different reasons cause you to stop watching movies?',
      type: 'integer',
      options: [1, 2, 3, 4, 5, 6],
      fieldName: 'total_stopping_reasons'
    },
    {
      id: '5',
      question: 'Do you discover movies through trailers?',
      type: 'boolean',
      fieldName: 'why_do_you_usually_choose_to_watch_movies_trailer_or_promotional_material'
    },
    {
      id: '6',
      question: 'What percentage of movies do you typically complete? (0.0 to 1.0)',
      type: 'multiple_choice',
      options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
      fieldName: 'genre_completion_ratio'
    },
    {
      id: '7',
      question: 'Do you discover movies through awards or critical acclaim?',
      type: 'boolean',
      fieldName: 'why_do_you_usually_choose_to_watch_movies_awards_or_critical_acclaim'
    },
    {
      id: '8',
      question: 'Do you pause movies when you lose focus or get distracted?',
      type: 'boolean',
      fieldName: 'why_do_you_usually_pause_the_movie_lost_focus_or_distracted'
    },
    {
      id: '9',
      question: 'Do you stop watching movies due to distractions or interruptions?',
      type: 'boolean',
      fieldName: 'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_distractions_or_interruptions'
    },
    {
      id: '10',
      question: 'Do you stop watching movies due to technical issues (buffering, audio, etc.)?',
      type: 'boolean',
      fieldName: 'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_technical_issues_buffering_audio_etc.'
    },
    {
      id: '11',
      question: 'Rate your patience level when watching movies (0.0 to 1.0)',
      type: 'multiple_choice',
      options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
      fieldName: 'patience_score'
    },
    {
      id: '12',
      question: 'How many multitasking behaviors do you usually have while watching?',
      type: 'integer',
      options: [0, 1, 2, 3, 4, 5],
      fieldName: 'total_multitasking_behaviors'
    },
    {
      id: '13',
      question: 'Do you chat or text with others while watching movies?',
      type: 'boolean',
      fieldName: 'do_you_usually_do_other_things_while_watching_movies_i_chat_or_text_with_others'
    },
    {
      id: '14',
      question: 'Rate your attention span when watching movies (0.0 to 1.0)',
      type: 'multiple_choice',
      options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
      fieldName: 'attention_span_score'
    },
    {
      id: '15',
      question: 'Do you pause movies to discuss with others watching?',
      type: 'boolean',
      fieldName: 'why_do_you_usually_pause_the_movie_to_discuss_something_with_others_watching'
    },
    {
      id: '16',
      question: 'Rate your social influence when choosing movies (1-10)',
      type: 'integer',
      options: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      fieldName: 'social_influence_score'
    },
    {
      id: '17',
      question: 'Do you usually focus only on the movie (no multitasking)?',
      type: 'boolean',
      fieldName: 'do_you_usually_do_other_things_while_watching_movies_no_i_usually_focus_only_on_the_movie'
    },
    {
      id: '18',
      question: 'Do you often stop watching Romance movies before finishing?',
      type: 'boolean',
      fieldName: 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_romance'
    },
    {
      id: '19',
      question: 'Do you discover movies through reviews or ratings?',
      type: 'boolean',
      fieldName: 'how_do_you_usually_discover_movies_you_decide_to_watch_reviews_or_ratings'
    },
    {
      id: '20',
      question: 'Do you often stop watching Action movies before finishing?',
      type: 'boolean',
      fieldName: 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_action'
    },
    {
      id: '21',
      question: 'Do you enjoy watching Action movies?',
      type: 'boolean',
      fieldName: 'which_genres_do_you_enjoy_watching_the_most_action'
    },
    {
      id: '22',
      question: 'Do you usually watch movies at home via streaming platforms?',
      type: 'boolean',
      fieldName: 'where_do_you_usually_watch_movies_streaming_at_home_netflix_disney+_etc.'
    },
    {
      id: '23',
      question: 'Do you enjoy watching Romance movies?',
      type: 'boolean',
      fieldName: 'which_genres_do_you_enjoy_watching_the_most_romance'
    },
    {
      id: '24',
      question: 'Are you currently answering this on a weekend?',
      type: 'boolean',
      fieldName: 'is_weekend'
    }
  ];

  get currentQuestion() {
    return this.questions[this.currentStep()];
  }

  get progress() {
    return ((this.currentStep() + 1) / this.questions.length) * 100;
  }

  get isFirstStep() {
    return this.currentStep() === 0;
  }

  get isLastStep() {
    return this.currentStep() === this.questions.length - 1;
  }

  get canProceed() {
    const currentResponse = this.responses()[this.currentQuestion.fieldName];
    return currentResponse !== undefined && currentResponse !== null;
  }

  setResponse(fieldName: string, value: any) {
    this.responses.update(responses => ({
      ...responses,
      [fieldName]: value
    }));
  }

  nextStep() {
    if (this.canProceed && !this.isLastStep) {
      this.currentStep.update(step => step + 1);
    }
  }

  previousStep() {
    if (!this.isFirstStep) {
      this.currentStep.update(step => step - 1);
    }
  }

  async submitSurvey() {
    if (!this.canProceed) return;
    
    this.isSubmitting.set(true);
    
    try {
      // Add automatic weekend detection
      const surveyData = { ...this.responses() };
      surveyData['is_weekend'] = new Date().getDay() === 0 || new Date().getDay() === 6 ? 1 : 0;
      
      // Transform survey responses to API format
      const apiData = this.predictionService.transformSurveyToApiFormat(surveyData);
      
      console.log('Sending survey data to API:', apiData);
      
      // Save user survey data to session storage for use in movies page
      sessionStorage.setItem('userSurveyData', JSON.stringify(apiData));
      
      // Call real ML API
      this.predictionService.predictDropoff(apiData).subscribe({
        next: (response) => {
          console.log('Prediction response:', response);
          this.predictionResult.set(response);
          
          // Show success message with prediction
          const probability = Math.round(response.prediction.dropoff_probability * 100);
          alert(`Prediction complete! 
            Dropoff Risk: ${response.prediction.risk_level}
            Probability: ${probability}%
            
            Redirecting to view personalized movie recommendations...`);
          
          // Navigate to movies page with prediction data
          this.router.navigate(['/movies'], { 
            state: { predictionResult: response } 
          });
        },
        error: (error) => {
          console.error('API Error:', error);
          alert('Error connecting to prediction service. Please check if the API is running on http://localhost:8000');
        }
      });
      
    } catch (error) {
      console.error('Error submitting survey:', error);
      alert('Error processing survey. Please try again.');
    } finally {
      this.isSubmitting.set(false);
    }
  }

  getResponseValue(fieldName: string) {
    return this.responses()[fieldName];
  }
}
