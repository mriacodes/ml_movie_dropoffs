# API Configuration settings
import os
from typing import Dict, Any

class APIConfig:
    """Configuration settings for the Movie Dropoff Prediction API"""
    
    # API Settings
    API_TITLE = "Movie Dropoff Prediction API"
    API_DESCRIPTION = "ML API for predicting user subscription dropoff risk"
    API_VERSION = "1.0.0"
    
    # Server Settings
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # CORS Settings
    ALLOWED_ORIGINS = [
        "http://localhost:4200",  # Angular development server
        "http://localhost:3000",  # Alternative frontend port
    ]
    
    # Model Settings
    MODEL_PATH = "../django_models/movie_dropoff_model_optimized.pkl"
    SMOTE_TRANSFORMER_PATH = "../django_models/smote_transformer.pkl"
    MODEL_INFO_PATH = "../django_models/model_info.json"
    
    # Feature Engineering Settings
    EXPECTED_FEATURES_COUNT = 50
    MIN_CONFIDENCE_THRESHOLD = 0.7
    
    # Data Validation Settings
    MIN_AGE = 13
    MAX_AGE = 100
    MIN_SUBSCRIPTION_DURATION = 0
    MAX_SUBSCRIPTION_DURATION = 120  # months
    
    VALID_STREAMING_FREQUENCIES = [
        'rarely', 'weekly', 'moderate', 'frequent', 'daily'
    ]
    
    VALID_PRICE_SENSITIVITIES = [
        'low', 'moderate', 'high'
    ]
    
    # Risk Level Thresholds
    LOW_RISK_THRESHOLD = 0.3
    HIGH_RISK_THRESHOLD = 0.7
    
    # Logging Settings
    LOG_PREDICTIONS = True
    LOG_LEVEL = "INFO"
    
    # Performance Settings
    MAX_CONCURRENT_PREDICTIONS = 100
    PREDICTION_TIMEOUT_SECONDS = 30
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return {
            "api": {
                "title": cls.API_TITLE,
                "description": cls.API_DESCRIPTION,
                "version": cls.API_VERSION,
                "host": cls.HOST,
                "port": cls.PORT,
                "debug": cls.DEBUG
            },
            "cors": {
                "allowed_origins": cls.ALLOWED_ORIGINS
            },
            "model": {
                "path": cls.MODEL_PATH,
                "smote_path": cls.SMOTE_TRANSFORMER_PATH,
                "info_path": cls.MODEL_INFO_PATH,
                "expected_features": cls.EXPECTED_FEATURES_COUNT
            },
            "validation": {
                "age_range": [cls.MIN_AGE, cls.MAX_AGE],
                "subscription_range": [cls.MIN_SUBSCRIPTION_DURATION, cls.MAX_SUBSCRIPTION_DURATION],
                "streaming_frequencies": cls.VALID_STREAMING_FREQUENCIES,
                "price_sensitivities": cls.VALID_PRICE_SENSITIVITIES
            },
            "thresholds": {
                "low_risk": cls.LOW_RISK_THRESHOLD,
                "high_risk": cls.HIGH_RISK_THRESHOLD,
                "min_confidence": cls.MIN_CONFIDENCE_THRESHOLD
            }
        }

# Environment-specific configurations
class DevelopmentConfig(APIConfig):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(APIConfig):
    """Production environment configuration"""
    DEBUG = False
    HOST = "0.0.0.0"
    LOG_LEVEL = "WARNING"
    ALLOWED_ORIGINS = ["https://yourdomain.com"]  # Update with actual domain

class TestingConfig(APIConfig):
    """Testing environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    LOG_PREDICTIONS = False

# Get configuration based on environment
def get_config():
    """Get configuration based on environment variable"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()

# Global config instance
config = get_config()
