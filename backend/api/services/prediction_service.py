import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import os
import json

class MovieDropoffPredictionService:
    """
    Main prediction service for movie dropoff model
    Uses placeholder logic until real ML model is integrated
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.is_loaded = False
        self.model_info = {
            "name": "Movie Dropoff Predictor",
            "version": "1.0.0",
            "features": 50,
            "status": "placeholder"
        }
        
    def load_model(self):
        """Load the trained ML model and preprocessing components"""
        try:
            # TODO: Load actual model when available
            # model_path = "../django_models/movie_dropoff_model.pkl"
            # self.model = joblib.load(model_path)
            
            # For now, simulate model loading
            self.feature_names = self._get_expected_features()
            self.is_loaded = True
            print("✓ Model loaded successfully (placeholder)")
            return True
            
        except Exception as e:
            print(f"✗ Model loading failed: {e}")
            return False
    
    def _get_expected_features(self) -> List[str]:
        """Return the expected feature names for the model"""
        # Based on your feature engineering work - 50 selected features
        return [
            'age_group', 'education_level', 'income_bracket', 'employment_status',
            'household_size', 'region', 'streaming_frequency', 'device_preference',
            'genre_preference_action', 'genre_preference_comedy', 'genre_preference_drama',
            'viewing_time_weekday', 'viewing_time_weekend', 'subscription_duration',
            'previous_cancellations', 'customer_support_contacts',
            'content_discovery_method', 'social_viewing_frequency',
            'price_sensitivity', 'feature_usage_score',
            # Add more features based on your feature engineering results
            # This would come from your final_feature_set.pkl
        ]
    
    def predict_dropoff(self, user_data: Dict) -> Tuple[float, str, List[str], str]:
        """
        Predict dropoff probability for a user
        Returns: (probability, risk_level, recommendations, user_segment)
        """
        try:
            # Placeholder prediction logic using behavioral heuristics
            probability = self._calculate_placeholder_probability(user_data)
            risk_level = self._get_risk_level(probability)
            recommendations = self._get_recommendations(user_data, probability)
            user_segment = self._get_user_segment(user_data)
            
            return probability, risk_level, recommendations, user_segment
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.5, "Medium", ["Contact support"], "Unknown"
    
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
