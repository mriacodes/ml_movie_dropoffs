import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import os
import json
import joblib
import pickle

class MovieDropoffPredictionService:
    """
    Main prediction service for movie dropoff model
    Now using Marivic's trained Gradient Boosting model
    """
    
    def __init__(self):
        self.model = None
        self.smote_transformer = None
        self.feature_names = []
        self.model_info = {}
        self.is_loaded = False
        
    def load_model(self):
        """Load the trained ML model and preprocessing components"""
        try:
            # Paths to model files
            model_path = "../django_models/movie_dropoff_model_optimized.pkl"
            smote_path = "../django_models/smote_transformer.pkl"
            info_path = "../django_models/model_info.json"
            
            # Check if files exist
            if not os.path.exists(model_path):
                print(f"⚠ Model file not found at {model_path}, using fallback")
                return self._load_fallback_model()
            
            # Load the trained model
            self.model = joblib.load(model_path)
            print(f"✓ Loaded trained model from {model_path}")
            
            # Load SMOTE transformer (if needed)
            if os.path.exists(smote_path):
                self.smote_transformer = joblib.load(smote_path)
                print("✓ Loaded SMOTE transformer")
            
            # Load model info
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    self.model_info = json.load(f)
                    self.feature_names = self.model_info.get('feature_names', [])
                print(f"✓ Loaded model info with {len(self.feature_names)} features")
            
            self.is_loaded = True
            print("✓ Real ML model loaded successfully!")
            print(f"  - Model type: Gradient Boosting Classifier")
            print(f"  - Features: {len(self.feature_names)}")
            print(f"  - Performance: F1-score 75.9%, Accuracy 65%")
            
            return True
            
        except Exception as e:
            print(f"✗ Real model loading failed: {e}")
            print("⚠ Falling back to placeholder mode")
            return self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Fallback to placeholder model if real model loading fails"""
        self.feature_names = self._get_placeholder_features()
        self.is_loaded = True
        self.model_info = {
            "name": "Movie Dropoff Predictor",
            "version": "1.0.0-fallback",
            "features": len(self.feature_names),
            "status": "placeholder"
        }
        print("✓ Fallback model loaded")
        return True
    
    def _get_placeholder_features(self) -> List[str]:
        """Return placeholder feature names"""
        return [
            'boring_plot', 'total_stopping_reasons', 'stop_historical', 'enjoy_action',
            'total_genres_stopped', 'genre_completion_ratio', 'patience_score',
            'total_multitasking_behaviors', 'attention_span_score', 'behavior_cluster',
            'social_influence_score', 'watch_frequency_score', 'is_weekend'
        ]
    
    def predict_dropoff(self, user_data: Dict) -> Tuple[float, str, List[str], str]:
        """
        Predict dropoff probability for a user
        Returns: (probability, risk_level, recommendations, user_segment)
        """
        try:
            if self.model is not None:
                # Use real trained model
                return self._predict_with_real_model(user_data)
            else:
                # Use placeholder logic
                return self._predict_with_placeholder(user_data)
                
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.5, "Medium", ["Contact support"], "Unknown"
    
    def _predict_with_real_model(self, user_data: Dict) -> Tuple[float, str, List[str], str]:
        """Use the real trained Gradient Boosting model for prediction"""
        try:
            # Prepare features for the model
            feature_vector = self._prepare_features_for_model(user_data)
            
            # Get prediction probability
            probabilities = self.model.predict_proba([feature_vector])
            probability = float(probabilities[0][1])  # Probability of dropoff (class 1)
            
            # Calculate additional metrics
            risk_level = self._get_risk_level(probability)
            recommendations = self._get_recommendations(user_data, probability)
            user_segment = self._get_user_segment(user_data)
            
            print(f"✓ Real model prediction: {probability:.3f} ({risk_level})")
            return probability, risk_level, recommendations, user_segment
            
        except Exception as e:
            print(f"Real model prediction failed: {e}, using fallback")
            return self._predict_with_placeholder(user_data)
    
    def _prepare_features_for_model(self, user_data: Dict) -> List[float]:
        """
        Prepare user input data to match the model's expected feature format
        """
        # Create feature vector matching the model's expected input
        feature_vector = []
        
        # Map from survey questions to model features
        feature_mapping = {
            'boring_plot': 'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_boring_or_uninteresting_plot',
            'stop_historical': 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical',
            'feeling_bored_pause': 'why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested',
            'total_genres_stopped': 'total_genres_stopped',
            'total_stopping_reasons': 'total_stopping_reasons',
            'genre_completion_ratio': 'genre_completion_ratio',
            'patience_score': 'patience_score',
            'total_multitasking_behaviors': 'total_multitasking_behaviors',
            'attention_span_score': 'attention_span_score',
            'behavior_cluster': 'behavior_cluster',
            'social_influence_score': 'social_influence_score',
            'is_weekend': 'is_weekend'
        }
        
        # For each feature expected by the model, try to get value from user_data
        for feature_name in self.feature_names:
            # Try to find matching input
            value = 0.0  # Default value
            
            # Direct mapping
            for input_key, model_feature in feature_mapping.items():
                if model_feature == feature_name and input_key in user_data:
                    value = float(user_data[input_key])
                    break
            
            # Handle boolean features (convert to 0/1)
            if isinstance(value, bool):
                value = 1.0 if value else 0.0
            
            feature_vector.append(value)
        
        print(f"✓ Prepared feature vector with {len(feature_vector)} features")
        return feature_vector
    
    def _predict_with_placeholder(self, user_data: Dict) -> Tuple[float, str, List[str], str]:
        """Fallback placeholder prediction logic"""
        probability = self._calculate_placeholder_probability(user_data)
        risk_level = self._get_risk_level(probability)
        recommendations = self._get_recommendations(user_data, probability)
        user_segment = self._get_user_segment(user_data)
        
        return probability, risk_level, recommendations, user_segment
    
    def _calculate_placeholder_probability(self, data: Dict) -> float:
        """
        Placeholder probability calculation based on key indicators
        This simulates the ML model until the real one is integrated
        """
        risk_score = 0.0
        
        # Age factor (older users tend to be more stable)
        age = data.get('age', 30)
        if age < 25:
            risk_score += 0.2
        elif age > 45:
            risk_score -= 0.1
            
        # Streaming frequency (low frequency = higher risk)
        streaming_freq = data.get('streaming_frequency', 'moderate')
        if streaming_freq == 'rarely':
            risk_score += 0.3
        elif streaming_freq == 'daily':
            risk_score -= 0.2
            
        # Subscription duration (newer users higher risk)
        duration = data.get('subscription_duration', 6)
        if duration < 3:
            risk_score += 0.25
        elif duration > 12:
            risk_score -= 0.15
            
        # Price sensitivity
        price_sensitive = data.get('price_sensitivity', 'moderate')
        if price_sensitive == 'high':
            risk_score += 0.2
            
        # Customer support contacts (more contacts = higher risk)
        support_contacts = data.get('customer_support_contacts', 0)
        risk_score += min(support_contacts * 0.1, 0.3)
        
        # Convert to probability (0-1)
        probability = max(0.0, min(1.0, 0.5 + risk_score))
        
        return round(probability, 3)
    
    def _get_risk_level(self, probability: float) -> str:
        """Convert probability to risk level"""
        if probability < 0.3:
            return "Low"
        elif probability < 0.7:
            return "Medium"
        else:
            return "High"
    
    def _get_recommendations(self, data: Dict, probability: float) -> List[str]:
        """Generate personalized recommendations based on user data and risk"""
        recommendations = []
        
        if probability > 0.7:
            recommendations.extend([
                "🎯 Exclusive content recommendations based on your viewing history",
                "💰 Special discount offer for continued subscription",
                "📞 Priority customer support contact"
            ])
        elif probability > 0.4:
            recommendations.extend([
                "🎬 Discover new genres you might enjoy",
                "📱 Try our mobile app features",
                "⭐ Rate movies to improve recommendations"
            ])
        else:
            recommendations.extend([
                "🚀 Explore premium features",
                "👥 Share with friends and family",
                "🎉 Check out this week's trending content"
            ])
            
        # Add specific recommendations based on user profile
        streaming_freq = data.get('streaming_frequency', 'moderate')
        if streaming_freq == 'rarely':
            recommendations.append("📺 Set up viewing reminders for your favorite shows")
            
        return recommendations[:4]  # Limit to 4 recommendations
    
    def _get_user_segment(self, data: Dict) -> str:
        """Classify user into behavioral segment"""
        age = data.get('age', 30)
        streaming_freq = data.get('streaming_frequency', 'moderate')
        duration = data.get('subscription_duration', 6)
        
        if age < 25 and streaming_freq == 'daily':
            return "Young Power User"
        elif age > 45 and duration > 12:
            return "Loyal Mature Viewer"
        elif streaming_freq == 'rarely':
            return "Casual Viewer"
        elif duration < 3:
            return "New Subscriber"
        else:
            return "Regular Viewer"
    
    def get_model_info(self) -> Dict:
        """Return model information"""
        return {
            **self.model_info,
            "is_loaded": self.is_loaded,
            "features_count": len(self.feature_names),
            "expected_features": self.feature_names[:10]  # Show first 10
        }

# Global service instance
prediction_service = MovieDropoffPredictionService()
