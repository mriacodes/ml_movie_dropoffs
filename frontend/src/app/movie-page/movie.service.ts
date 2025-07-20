import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MovieService {
  private apiKey = '9bedd8178358fe73088aaca74b58c6a8';
  private apiUrl = 'https://api.themoviedb.org/3/discover/movie';

  constructor(private http: HttpClient) {}

  getMoviesByGenre(genreId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}?api_key=${this.apiKey}&with_genres=${genreId}`);
  }
}
