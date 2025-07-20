import { Component } from '@angular/core';
import { MovieService } from './movie.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-movie-page',
  templateUrl: './movie-page.html',
  styleUrls: ['./movie-page.scss'],
  imports: [CommonModule],
  
})
export class MoviePage {
  selectedMovie: any = null;
  movies: any[] = [];

  constructor(private movieService: MovieService) {}

  ngOnInit() {
    this.fetchMovies();
  }

  fetchMovies() {
    const genreId = '28'; // Action
    this.movieService.getMoviesByGenre(genreId).subscribe((res) => {
      this.movies = res.results;
    });
  }

  selectMovie(movie: any) {
    this.selectedMovie = {
      title: movie.title,
      image: `https://image.tmdb.org/t/p/w500${movie.poster_path}`,
      date: movie.release_date,
      duration: 'N/A',
      language: movie.original_language,
      tags: [] // optionally map TMDb genres
    };
  }

  closeModal() {
    this.selectedMovie = null;
  }
  // selectedMovie: any = null;
  
  //   selectMovie(title: string, image: string, date: string, duration: string, language: string, tags: string[]) {
  //     this.selectedMovie = { title, image, date, duration, language, tags };
  //   }
  
  //   closeModal() {
  //     this.selectedMovie = null;
  //   }

}
