import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api'; // Replace with your Django API base

  constructor(private http: HttpClient) {}

  getPredictedMovies(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/predicted-movies/`);
  }

  getUserData(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/user/`);
  }

  // Add other Django endpoints as needed
}
