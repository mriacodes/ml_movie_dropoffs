#!/usr/bin/env python3
"""
Quick test server to validate API functionality
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

app = FastAPI(title="Movie Dropoff API - Test Server")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple placeholder prediction function
def simple_predict(user_data):
    """Simple rule-based prediction for testing"""
    risk_score = 0
    
    # Add risk factors
    if user_data.get("boring_plot", 0) == 1:
        risk_score += 0.2
    if user_data.get("total_stopping_reasons", 0) > 3:
        risk_score += 0.15
    if user_data.get("genre_completion_ratio", 0.5) < 0.5:
        risk_score += 0.1
    if user_data.get("is_weekend", 0) == 1:
        risk_score += 0.05
    
    # Convert to probability
    probability = min(max(risk_score, 0.05), 0.95)
    
    # Determine risk level
    if probability > 0.7:
        risk_level = "High Risk"
        recommendations = ["Watch shorter movies", "Choose engaging genres"]
    elif probability > 0.4:
        risk_level = "Medium Risk" 
        recommendations = ["Select movies with good openings", "Reduce distractions"]
    else:
        risk_level = "Low Risk"
        recommendations = ["Continue current habits", "Explore new genres"]
    
    user_segment = f"Risk Level: {risk_level}"
    
    return probability, risk_level, recommendations, user_segment

@app.get("/")
async def root():
    return {
        "message": "Movie Dropoff Prediction API Test Server",
        "status": "running",
        "endpoints": ["/health", "/predict", "/test"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "API is operational",
        "version": "1.0.0-test"
    }

@app.post("/predict")
async def predict(user_data: dict):
    """Simple prediction endpoint"""
    try:
        # Simple validation
        required_fields = ["boring_plot", "total_stopping_reasons"]
        missing = [field for field in required_fields if field not in user_data]
        if missing:
            return {"error": f"Missing fields: {missing}", "status": "failed"}
        
        # Predict
        prob, risk, recs, segment = simple_predict(user_data)
        
        return {
            "dropoff_probability": round(prob, 3),
            "risk_level": risk,
            "user_segment": segment,
            "recommendations": recs,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@app.get("/test")
async def test_prediction():
    """Test endpoint with sample data"""
    test_data = {
        "boring_plot": 1,
        "total_stopping_reasons": 4,
        "stop_historical": 0,
        "enjoy_action": 1,
        "genre_completion_ratio": 0.6,
        "is_weekend": 1
    }
    
    prob, risk, recs, segment = simple_predict(test_data)
    
    return {
        "test_data": test_data,
        "prediction": {
            "probability": round(prob, 3),
            "risk_level": risk,
            "user_segment": segment,
            "recommendations": recs
        },
        "status": "test_successful"
    }

if __name__ == "__main__":
    import uvicorn
    print("🎯 Starting Movie Dropoff API Test Server...")
    print("📡 Server will be at: http://localhost:8000")
    print("📖 Endpoints: /health, /predict, /test")
    uvicorn.run(app, host="127.0.0.1", port=8000)
