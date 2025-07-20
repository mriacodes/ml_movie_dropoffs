import pandas as pd
import numpy as np
from typing import Dict, Any, List
import json
from datetime import datetime

def validate_user_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate incoming user survey data
    Returns: (is_valid, error_messages)
    """
    errors = []
    required_fields = ['age', 'streaming_frequency', 'subscription_duration']
    
    # Check required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Validate age
    age = data.get('age')
    if age is not None:
        try:
            age_val = int(age)
            if age_val < 13 or age_val > 100:
                errors.append("Age must be between 13 and 100")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number")
    
    # Validate streaming frequency
    streaming_freq = data.get('streaming_frequency')
    valid_frequencies = ['rarely', 'weekly', 'moderate', 'frequent', 'daily']
    if streaming_freq and streaming_freq not in valid_frequencies:
        errors.append(f"streaming_frequency must be one of: {valid_frequencies}")
    
    # Validate subscription duration
    duration = data.get('subscription_duration')
    if duration is not None:
        try:
            duration_val = int(duration)
            if duration_val < 0 or duration_val > 120:  # Max 10 years
                errors.append("subscription_duration must be between 0 and 120 months")
        except (ValueError, TypeError):
            errors.append("subscription_duration must be a valid number")
    
    return len(errors) == 0, errors

def preprocess_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess user data to match model expectations
    """
    processed_data = data.copy()
    
    # Convert age to age group (if needed by model)
    age = data.get('age')
    if age is not None:
        if age < 25:
            processed_data['age_group'] = 'young'
        elif age < 45:
            processed_data['age_group'] = 'middle'
        else:
            processed_data['age_group'] = 'mature'
    
    # Ensure numeric fields are properly typed
    numeric_fields = ['age', 'subscription_duration', 'household_size', 'customer_support_contacts']
    for field in numeric_fields:
        if field in processed_data and processed_data[field] is not None:
            try:
                processed_data[field] = float(processed_data[field])
            except (ValueError, TypeError):
                processed_data[field] = 0
    
    return processed_data

def format_response_data(probability: float, risk_level: str, 
                        recommendations: List[str], user_segment: str) -> Dict[str, Any]:
    """
    Format prediction response data
    """
    return {
        "dropoff_probability": round(probability, 3),
        "risk_level": risk_level,
        "confidence_score": 0.85,  # Placeholder confidence
        "recommendations": recommendations,
        "user_segment": user_segment,
        "timestamp": datetime.now().isoformat(),
        "model_version": "1.0.0-placeholder"
    }

def log_prediction(user_data: Dict, prediction_result: Dict) -> None:
    """
    Log prediction for monitoring and analysis
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_features": {k: v for k, v in user_data.items() if k != 'personal_info'},
        "prediction": {
            "probability": prediction_result.get("dropoff_probability"),
            "risk_level": prediction_result.get("risk_level"),
            "user_segment": prediction_result.get("user_segment")
        }
    }
    
    # In production, this would go to a proper logging system
    print(f"PREDICTION LOG: {json.dumps(log_entry, indent=2)}")

def get_feature_importance() -> Dict[str, float]:
    """
    Return feature importance scores (placeholder)
    In production, this would come from the trained model
    """
    return {
        "streaming_frequency": 0.15,
        "subscription_duration": 0.12,
        "age": 0.10,
        "price_sensitivity": 0.09,
        "customer_support_contacts": 0.08,
        "genre_preferences": 0.07,
        "device_preference": 0.06,
        "viewing_time_patterns": 0.05
    }

def health_check() -> Dict[str, Any]:
    """
    Perform health check of the service
    """
    try:
        # Check if we can import required packages
        import pandas as pd
        import numpy as np
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "dependencies": {
                "pandas": pd.__version__,
                "numpy": np.__version__,
                "python": "3.x"
            },
            "model_status": "placeholder_active",
            "api_version": "1.0.0"
        }
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def get_model_metadata() -> Dict[str, Any]:
    """
    Return model metadata and configuration
    """
    return {
        "model_name": "Movie Dropoff Predictor",
        "model_type": "Binary Classification",
        "framework": "scikit-learn (placeholder)",
        "features_count": 50,
        "training_samples": 78,
        "expected_accuracy": "> 70% F1-score",
        "last_updated": "2024-12-20",
        "status": "placeholder_mode"
    }
