import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule, DecimalPipe } from '@angular/common';
import { PredictionService } from '../../services/prediction.service';

@Component({
  selector: 'app-home',
  imports: [RouterLink, CommonModule, DecimalPipe],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class HomeComponent implements OnInit {
  apiStatus = signal<'checking' | 'connected' | 'disconnected'>('checking');
  modelInfo = signal<any>(null);

  constructor(private predictionService: PredictionService) {}

  ngOnInit() {
    this.checkApiStatus();
  }

  checkApiStatus() {
    this.apiStatus.set('checking');
    
    this.predictionService.testConnection().subscribe({
      next: (response) => {
        console.log('API Connected:', response);
        this.apiStatus.set('connected');
        
        // Get model info
        this.predictionService.getModelInfo().subscribe({
          next: (modelInfo) => {
            this.modelInfo.set(modelInfo);
          },
          error: (error) => console.log('Model info error:', error)
        });
      },
      error: (error) => {
        console.error('API Connection Failed:', error);
        this.apiStatus.set('disconnected');
      }
    });
  }
}
