import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';
import { SurveyComponent } from './pages/survey/survey';
import { MoviesComponent } from './pages/movies/movies';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', redirectTo: '', pathMatch: 'full' },
  { path: 'survey', component: SurveyComponent },
  { path: 'movies', component: MoviesComponent },
  { path: '**', redirectTo: '' } // Wildcard route for 404 pages
];
