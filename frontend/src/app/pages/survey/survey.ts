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
  
  // Survey questions based on your ML model's feature selection
  questions: SurveyQuestion[] = [
    {
      id: '1',
      question: 'Do you stop watching movies because of boring/uninteresting plot?',
      type: 'boolean',
      fieldName: 'boring_plot'
    },
    {
      id: '2', 
      question: 'How many different reasons cause you to stop watching movies?',
      type: 'integer',
      options: [1, 2, 3, 4, 5, 6],
      fieldName: 'total_stopping_reasons'
    },
    {
      id: '3',
      question: 'Do you often stop watching Historical movies before finishing?',
      type: 'boolean',
      fieldName: 'stop_historical'
    },
    {
      id: '4',
      question: 'Do you enjoy watching Action movies?',
      type: 'boolean',
      fieldName: 'enjoy_action'
    },
    {
      id: '5',
      question: 'Do you enjoy watching Romance movies?',
      type: 'boolean',
      fieldName: 'enjoy_romance'
    },
    {
      id: '6',
      question: 'Do you pause movies when feeling bored or uninterested?',
      type: 'boolean',
      fieldName: 'pause_when_bored'
    },
    {
      id: '7',
      question: 'Do you usually focus only on the movie (no multitasking)?',
      type: 'boolean',
      fieldName: 'focus_only'
    },
    {
      id: '8',
      question: 'Do you discover movies through trailers?',
      type: 'boolean',
      fieldName: 'discover_trailer'
    },
    {
      id: '9',
      question: 'Do you discover movies through reviews or ratings?',
      type: 'boolean',
      fieldName: 'discover_reviews'
    },
    {
      id: '10',
      question: 'Do you discover movies through streaming platform suggestions?',
      type: 'boolean',
      fieldName: 'discover_platform'
    },
    {
      id: '11',
      question: 'Do you discover movies through friend/family recommendations?',
      type: 'boolean',
      fieldName: 'discover_friends'
    },
    {
      id: '12',
      question: 'Do you usually watch movies at home via streaming platforms?',
      type: 'boolean',
      fieldName: 'watch_streaming'
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
      // Transform survey responses to API format
      const apiData = this.predictionService.transformSurveyToApiFormat(this.responses());
      
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
