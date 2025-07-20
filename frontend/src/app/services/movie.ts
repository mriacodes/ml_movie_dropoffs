import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiKey = '9bedd8178358fe73088aaca74b58c6a8';
  private baseUrl = 'https://api.themoviedb.org/3';

  constructor(private http: HttpClient) {}

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
