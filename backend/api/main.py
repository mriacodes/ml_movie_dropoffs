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

# Temporary basic endpoints while pydantic installs
@app.get("/")
async def root():
    return {
        "message": "Movie Dropoff Prediction API is running",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "API is operational",
        "dependencies": {
            "pandas": pd.__version__,
            "numpy": np.__version__
        }
    }

# Placeholder prediction endpoint
@app.post("/predict")
async def predict_dropoff(user_data: Dict[Any, Any]):
    """Temporary prediction endpoint while dependencies install"""
    
    # Simple placeholder logic using your existing packages
    boring_plot = user_data.get("boring_plot", 0)
    feeling_bored = user_data.get("feeling_bored_pause", 0)
    multitasking = user_data.get("total_multitasking_behaviors", 0)
    attention_span = user_data.get("attention_span_score", 0.5)
    
    # Quick risk calculation
    risk_score = (boring_plot * 0.3 + feeling_bored * 0.2 + 
                 min(multitasking/5, 0.3) + (1-attention_span) * 0.2)
    
    probability = min(max(risk_score, 0.05), 0.95)
    
    if probability >= 0.7:
        risk_level = "High Risk"
        recommendations = [
            "Consider shorter movies",
            "Choose engaging genres",
            "Minimize distractions"
        ]
    elif probability >= 0.4:
        risk_level = "Medium Risk" 
        recommendations = [
            "Select movies with strong openings",
            "Try preferred genres"
        ]
    else:
        risk_level = "Low Risk"
        recommendations = ["Continue current preferences"]
    
    return {
        "dropoff_probability": round(probability, 3),
        "risk_level": risk_level,
        "confidence_score": 0.85,
        "recommendations": recommendations,
        "user_segment": "Placeholder Analysis",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-ml")
async def test_ml_dependencies():
    """Test that your ML packages are working"""
    try:
        # Test pandas
        df = pd.DataFrame({"test": [1, 2, 3]})
        
        # Test numpy
        arr = np.array([1, 2, 3])
        
        return {
            "pandas_test": "Working",
            "numpy_test": "Working", 
            "pandas_version": pd.__version__,
            "numpy_version": np.__version__,
            "sample_dataframe": df.to_dict(),
            "sample_array": arr.tolist()
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # This will work once uvicorn installs
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
