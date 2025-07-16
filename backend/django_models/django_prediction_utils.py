import joblib
import pandas as pd
import numpy as np
import json
import os
from django.conf import settings

class MovieDropoffPredictor:
    """
    Utility class for predicting movie dropoff likelihood in Django application
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.model_info = None
        self.class_mappings = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and metadata"""
        models_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        
        # Load trained model
        model_path = os.path.join(models_dir, 'movie_dropoff_model.pkl')
        self.model = joblib.load(model_path)
        
        # Load model info
        info_path = os.path.join(models_dir, 'model_info.json')
        with open(info_path, 'r') as f:
            self.model_info = json.load(f)
        
        # Load class mappings
        mappings_path = os.path.join(models_dir, 'class_mappings.json')
        with open(mappings_path, 'r') as f:
            self.class_mappings = json.load(f)
        
        self.feature_names = self.model_info['feature_names']
    
    def preprocess_user_input(self, user_responses):
        """
        Convert user survey responses to model input format
        
        Args:
            user_responses (dict): User responses from Django form
            
        Returns:
            pandas.DataFrame: Preprocessed features ready for prediction
        """
        # Initialize feature vector with zeros
        features = pd.DataFrame(0, index=[0], columns=self.feature_names)
        
        # Map user responses to features
        feature_mapping = {
            'boring_plot': 'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_boring_uninteresting_plot',
            'stop_historical': 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical',
            'pause_when_bored': 'why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested',
            'focus_only': 'do_you_usually_do_other_things_while_watching_movies_no_i_usually_focus_only_on_the_movie',
            'discover_trailer': 'how_do_you_usually_discover_movies_you_decide_to_watch_trailer',
            'watch_for_entertainment': 'why_do_you_usually_choose_to_watch_movies_entertainment',
            'enjoy_action': 'which_genres_do_you_enjoy_watching_the_most_action',
            'enjoy_romance': 'which_genres_do_you_enjoy_watching_the_most_romance',
            'total_stopping_reasons': 'total_stopping_reasons',
            'patience_score': 'patience_score',
            'completion_ratio': 'genre_completion_ratio'
        }
        
        # Fill in the features based on user responses
        for user_field, model_feature in feature_mapping.items():
            if user_field in user_responses and model_feature in features.columns:
                features[model_feature] = user_responses[user_field]
        
        return features
    
    def predict_dropoff_probability(self, user_responses):
        """
        Predict dropoff probability for a user
        
        Args:
            user_responses (dict): User survey responses
            
        Returns:
            dict: Prediction results with probability and interpretation
        """
        # Preprocess input
        features = self.preprocess_user_input(user_responses)
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        # Format results
        result = {
            'will_drop_off': bool(prediction),
            'dropoff_probability': float(probability[1]),
            'completion_probability': float(probability[0]),
            'confidence': float(max(probability)),
            'interpretation': self.interpret_prediction(probability[1]),
            'recommended_action': self.get_recommendation(probability[1])
        }
        
        return result
    
    def interpret_prediction(self, dropoff_prob):
        """Provide human-readable interpretation of prediction"""
        if dropoff_prob >= 0.8:
            return "Very High Risk - Likely to drop off"
        elif dropoff_prob >= 0.6:
            return "High Risk - May drop off"
        elif dropoff_prob >= 0.4:
            return "Moderate Risk - Uncertain"
        elif dropoff_prob >= 0.2:
            return "Low Risk - Likely to complete"
        else:
            return "Very Low Risk - Very likely to complete"
    
    def get_recommendation(self, dropoff_prob):
        """Provide actionable recommendations based on prediction"""
        if dropoff_prob >= 0.7:
            return "Recommend shorter movies or highly-rated content in preferred genres"
        elif dropoff_prob >= 0.5:
            return "Show movie trailers and reviews before recommendation"
        elif dropoff_prob >= 0.3:
            return "Standard movie recommendations"
        else:
            return "User is likely to enjoy most recommended content"
    
    def batch_predict_movies(self, user_responses, movie_list):
        """
        Predict dropoff probability for multiple movies for a user
        
        Args:
            user_responses (dict): User survey responses
            movie_list (list): List of movie dictionaries with metadata
            
        Returns:
            list: Movies with dropoff predictions
        """
        base_prediction = self.predict_dropoff_probability(user_responses)
        
        results = []
        for movie in movie_list:
            # Adjust prediction based on movie characteristics
            adjusted_prob = self.adjust_for_movie_features(
                base_prediction['dropoff_probability'], 
                movie
            )
            
            movie_result = movie.copy()
            movie_result.update({
                'dropoff_probability': adjusted_prob,
                'completion_probability': 1 - adjusted_prob,
                'recommendation_score': 1 - adjusted_prob,
                'interpretation': self.interpret_prediction(adjusted_prob)
            })
            results.append(movie_result)
        
        # Sort by recommendation score (completion probability)
        results.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return results
    
    def adjust_for_movie_features(self, base_prob, movie):
        """
        Adjust dropoff probability based on specific movie characteristics
        
        Args:
            base_prob (float): Base dropoff probability from user profile
            movie (dict): Movie metadata (genre, rating, runtime, etc.)
            
        Returns:
            float: Adjusted dropoff probability
        """
        adjusted_prob = base_prob
        
        # Adjust based on movie runtime (longer movies = higher dropoff risk)
        if 'runtime' in movie:
            if movie['runtime'] > 150:  # Very long movies
                adjusted_prob += 0.1
            elif movie['runtime'] > 120:  # Long movies
                adjusted_prob += 0.05
            elif movie['runtime'] < 90:  # Short movies
                adjusted_prob -= 0.05
        
        # Adjust based on IMDB rating (higher rating = lower dropoff risk)
        if 'imdb_score' in movie:
            if movie['imdb_score'] >= 8.0:  # Excellent movies
                adjusted_prob -= 0.15
            elif movie['imdb_score'] >= 7.0:  # Good movies
                adjusted_prob -= 0.1
            elif movie['imdb_score'] < 6.0:  # Poor movies
                adjusted_prob += 0.1
        
        # Ensure probability stays within [0, 1]
        return max(0.0, min(1.0, adjusted_prob))

# Usage example for Django views:
"""
# In your Django views.py:
from .ml_utils import MovieDropoffPredictor

def predict_user_dropoff(request):
    if request.method == 'POST':
        predictor = MovieDropoffPredictor()
        user_responses = request.POST.dict()
        
        # Get prediction
        prediction = predictor.predict_dropoff_probability(user_responses)
        
        # Get user's preferred genres and fetch movies
        preferred_genres = request.POST.getlist('preferred_genres')
        movies = get_movies_by_genres(preferred_genres)  # Your function
        
        # Get movie-specific predictions
        movie_predictions = predictor.batch_predict_movies(user_responses, movies)
        
        context = {
            'user_prediction': prediction,
            'movie_recommendations': movie_predictions[:10],  # Top 10
            'model_info': predictor.model_info
        }
        
        return render(request, 'predictions.html', context)
"""
