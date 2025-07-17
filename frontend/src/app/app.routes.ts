import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', redirectTo: '', pathMatch: 'full' },
  // Future routes will be added here
  // { path: 'survey', component: SurveyComponent },
  // { path: 'movies', component: MoviesComponent },
  { path: '**', redirectTo: '' } // Wildcard route for 404 pages
];
