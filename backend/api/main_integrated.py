from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Dict, Any
import json
from datetime import datetime

# Import our custom services and utilities
from services.prediction_service import prediction_service
from utils.data_utils import (
    validate_user_data, 
    preprocess_user_data, 
    format_response_data,
    log_prediction,
    health_check,
    get_model_metadata
)
from models.response_models import create_prediction_response, create_health_response

# We'll add these once pydantic installs
# from models.response_models import PredictionResponse, HealthResponse
# from models.request_models import UserSurveyData

app = FastAPI(
    title="Movie Dropoff Prediction API",
    description="ML API for predicting user subscription dropoff risk",
    version="1.0.0"
)

# CORS configuration for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the ML model and services on startup"""
    try:
        # Load the prediction service
        success = prediction_service.load_model()
        
        if success:
            print("✓ API started successfully")
            print("✓ ML dependencies loaded (pandas, numpy)")
            print("✓ Prediction service initialized")
            print("⚠ Running in PLACEHOLDER mode - waiting for real ML model")
        else:
            print("⚠ API started with limited functionality")
            
    except Exception as e:
        print(f"✗ Startup error: {e}")
        print("⚠ API running in fallback mode")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Movie Dropoff Prediction API",
        "description": "ML API for predicting user subscription dropoff risk",
        "version": "1.0.0",
        "status": "running",
        "mode": "placeholder",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model_info": "/model/info",
            "test": "/test-ml"
        }
    }

@app.get("/health")
async def api_health():
    """Health check endpoint"""
    try:
        health_data = health_check()
        return create_health_response(
            status=health_data["status"],
            message="API is running successfully"
        )
    except Exception as e:
        return create_health_response(
            status="error",
            message=f"Health check failed: {str(e)}"
        )

@app.post("/predict")
async def predict_dropoff(user_data: Dict[str, Any]):
    """
    Predict dropoff probability for a user
    
    Expected user_data format:
    {
        "age": 25,
        "streaming_frequency": "moderate",
        "subscription_duration": 6,
        "price_sensitivity": "low",
        "customer_support_contacts": 0,
        ...
    }
    """
    try:
        # Validate input data
        is_valid, errors = validate_user_data(user_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail={"errors": errors})
        
        # Preprocess the data
        processed_data = preprocess_user_data(user_data)
        
        # Get prediction
        probability, risk_level, recommendations, user_segment = prediction_service.predict_dropoff(processed_data)
        
        # Format response
        response = format_response_data(probability, risk_level, recommendations, user_segment)
        
        # Log the prediction (for monitoring)
        log_prediction(processed_data, response)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/model/info")
async def get_model_info():
    """Get information about the ML model"""
    try:
        model_info = prediction_service.get_model_info()
        metadata = get_model_metadata()
        
        return {
            **model_info,
            **metadata,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )

@app.get("/test-ml")
async def test_ml_dependencies():
    """Test ML dependencies and basic functionality"""
    try:
        # Test pandas and numpy
        df = pd.DataFrame({'test': [1, 2, 3]})
        arr = np.array([1, 2, 3])
        
        # Test prediction service
        test_user = {
            'age': 28,
            'streaming_frequency': 'moderate',
            'subscription_duration': 8,
            'price_sensitivity': 'low',
            'customer_support_contacts': 1
        }
        
        probability, risk_level, recommendations, segment = prediction_service.predict_dropoff(test_user)
        
        return {
            "status": "success",
            "message": "All ML dependencies working",
            "dependencies": {
                "pandas_version": pd.__version__,
                "numpy_version": np.__version__,
                "prediction_service": "operational"
            },
            "test_prediction": {
                "input": test_user,
                "probability": probability,
                "risk_level": risk_level,
                "user_segment": segment,
                "recommendations_count": len(recommendations)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"ML test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Additional utility endpoints
@app.get("/features")
async def get_expected_features():
    """Get list of expected features for the model"""
    try:
        features = prediction_service.feature_names
        return {
            "feature_count": len(features),
            "features": features,
            "description": "Expected input features for the model"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get features: {str(e)}"
        )

@app.get("/status")
async def get_api_status():
    """Detailed API status information"""
    try:
        return {
            "api_status": "running",
            "model_loaded": prediction_service.is_loaded,
            "mode": "placeholder",
            "ready_for_predictions": True,
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "api_status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Movie Dropoff Prediction API...")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
