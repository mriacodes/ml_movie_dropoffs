from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import json
import joblib
import os
from datetime import datetime

app = FastAPI(
    title="Movie Dropoff Prediction API",
    description="ML API for predicting movie watching dropoff behavior",
    version="1.0.0"
)

# CORS configuration for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== REAL ML MODEL PREDICTOR =====
class MovieDropoffPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.model_info = {}
        self.is_loaded = False
        self.fallback_mode = False
        
        # Try to load the real model
        self._load_real_model()
    
    def _load_real_model(self):
        """Load final trained model"""
        try:
            # Fix: Updated paths to match your actual structure
            model_path = "movie_dropoff_model_optimized.pkl"  # Model is in same folder
            info_path = "../django_models/model_info_optimized.json"  # Check if this exists
            
            if os.path.exists(model_path):
                # Load the trained model
                self.model = joblib.load(model_path)
                print("✅ Loaded optimized ML model successfully!")
                
                # Load model info if available
                if os.path.exists(info_path):
                    with open(info_path, 'r') as f:
                        self.model_info = json.load(f)
                    self.feature_names = self.model_info.get('features', [])
                    print(f"✅ Loaded {len(self.feature_names)} features from model info")
                else:
                    print("⚠ Model info not found, using basic feature set")
                    self.feature_names = self._get_basic_features()
                
                self.is_loaded = True
                self.fallback_mode = False
                
                print(f"🎯 Model Performance:")
                if 'performance_metrics' in self.model_info:
                    metrics = self.model_info['performance_metrics']
                    print(f"  - F1 Score: {metrics.get('f1_score', 'N/A')}")
                    print(f"  - Accuracy: {metrics.get('accuracy', 'N/A')}")
                    print(f"  - Precision: {metrics.get('precision', 'N/A')}")
                    print(f"  - Recall: {metrics.get('recall', 'N/A')}")
                
            else:
                print(f"❌ Model file not found at: {model_path}")
                self._load_fallback_model()
                
        except Exception as e:
            print(f"❌ Error loading real model: {e}")
            self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Load fallback rule-based model"""
        print("🔄 Loading fallback rule-based model...")
        self.fallback_mode = True
        self.is_loaded = True
        self.feature_names = self._get_basic_features()
        self.model_info = {
            "model_name": "Rule-based Fallback",
            "version": "1.0.0",
            "type": "fallback"
        }
    
    def _get_basic_features(self):
        """Basic feature set for fallback"""
        return [
            "boring_plot", "total_stopping_reasons", "stop_historical", 
            "enjoy_action", "genre_completion_ratio", "patience_score",
            "attention_span_score", "total_multitasking_behaviors",
            "social_influence_score", "is_weekend"
        ]
    
    def _prepare_features(self, user_data: dict) -> pd.DataFrame:
        """Prepare features for model prediction"""
        if self.fallback_mode:
            # For fallback, just use the basic features
            feature_dict = {}
            for feature in self.feature_names:
                feature_dict[feature] = user_data.get(feature, 0)
            return pd.DataFrame([feature_dict])
        
        else:
            # For real model, prepare all features
            # Create feature vector with all expected features
            feature_dict = {}
            
            # Fill in provided features
            for feature in self.feature_names:
                feature_dict[feature] = user_data.get(feature, 0)
            
            # Create DataFrame with proper feature order
            feature_df = pd.DataFrame([feature_dict])
            
            # Ensure all columns are present and in correct order
            feature_df = feature_df.reindex(columns=self.feature_names, fill_value=0)
            
            return feature_df
    
    def predict_dropoff(self, user_data: dict):
        """Predict dropoff probability using real or fallback model"""
        try:
            if self.fallback_mode:
                return self._fallback_prediction(user_data)
            else:
                return self._real_model_prediction(user_data)
                
        except Exception as e:
            print(f"⚠ Prediction error: {e}, falling back to rule-based")
            return self._fallback_prediction(user_data)
    
    def _real_model_prediction(self, user_data: dict):
        """Use the real trained model for prediction"""
        # Prepare features
        feature_df = self._prepare_features(user_data)
        
        # Get prediction probability
        probability = self.model.predict_proba(feature_df)[0][1]  # Probability of dropout
        
        # Determine risk level and recommendations
        risk_level, user_segment, recommendations = self._analyze_prediction(probability, user_data)
        
        return probability, risk_level, recommendations, user_segment
    
    def _fallback_prediction(self, user_data: dict):
        """Rule-based prediction fallback"""
        risk_score = 0.0
        
        # Analyze risk factors
        if user_data.get("boring_plot", 0) == 1:
            risk_score += 0.25
        if user_data.get("total_stopping_reasons", 0) > 3:
            risk_score += 0.20
        if user_data.get("stop_historical", 0) == 1:
            risk_score += 0.15
        if user_data.get("genre_completion_ratio", 0.5) < 0.4:
            risk_score += 0.15
        if user_data.get("patience_score", 0.5) < 0.3:
            risk_score += 0.10
        if user_data.get("attention_span_score", 0.5) < 0.3:
            risk_score += 0.10
        if user_data.get("total_multitasking_behaviors", 0) > 2:
            risk_score += 0.05
        
        # Convert to probability
        probability = min(max(risk_score, 0.05), 0.95)
        
        # Determine risk level and recommendations
        risk_level, user_segment, recommendations = self._analyze_prediction(probability, user_data)
        
        return probability, risk_level, recommendations, user_segment
    
    def _analyze_prediction(self, probability: float, user_data: dict):
        """Analyze prediction and generate recommendations"""
        if probability >= 0.7:
            risk_level = "High Risk"
            user_segment = "High Dropout Risk"
            recommendations = [
                "Consider shorter movies (under 90 minutes)",
                "Choose action or comedy genres for better engagement",
                "Watch during peak attention hours",
                "Minimize distractions during viewing"
            ]
        elif probability >= 0.4:
            risk_level = "Medium Risk"
            user_segment = "Moderate Dropout Risk"
            recommendations = [
                "Select movies with strong opening scenes",
                "Try genres you historically complete more",
                "Reduce multitasking during viewing",
                "Consider watching with others"
            ]
        else:
            risk_level = "Low Risk"
            user_segment = "Completion Oriented"
            recommendations = [
                "Continue with current viewing habits",
                "You show good completion patterns",
                "Consider exploring new genres"
            ]
        
        return risk_level, user_segment, recommendations

# Initialize predictor
predictor = MovieDropoffPredictor()

# ===== UTILITY FUNCTIONS =====
def validate_user_data(data: dict) -> tuple[bool, list]:
    """Validate input data"""
    errors = []
    required_fields = ["boring_plot", "total_stopping_reasons"]
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate data types and ranges
    for key, value in data.items():
        if key in ["boring_plot", "stop_historical", "enjoy_action", "is_weekend"]:
            if not isinstance(value, int) or value not in [0, 1]:
                errors.append(f"{key} must be 0 or 1")
        elif key in ["genre_completion_ratio", "patience_score", "attention_span_score"]:
            if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
                errors.append(f"{key} must be between 0.0 and 1.0")
    
    return len(errors) == 0, errors

def format_prediction_response(probability: float, risk_level: str, 
                             recommendations: List[str], user_segment: str) -> dict:
    """Format prediction response"""
    return {
        "dropoff_probability": round(probability, 3),
        "risk_level": risk_level,
        "user_segment": user_segment,
        "recommendations": recommendations[:4],  # Limit to 4
        "confidence_score": 0.85,
        "model_version": predictor.model_info.get('version', '1.0.0'),
        "model_type": "ML Model" if not predictor.fallback_mode else "Rule-based Fallback",
        "timestamp": datetime.now().isoformat()
    }

# ===== API ENDPOINTS =====
@app.on_event("startup")
async def startup_event():
    """Initialize the API on startup"""
    print("🎬 Movie Dropoff Prediction API Started")
    print(f"✅ Predictor loaded: {predictor.is_loaded}")
    print(f"🤖 Model type: {'Real ML Model' if not predictor.fallback_mode else 'Fallback Rule-based'}")
    print(f"📊 Features available: {len(predictor.feature_names)}")
    print("🚀 API ready for predictions!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Movie Dropoff Prediction API",
        "description": "Predict user movie watching dropoff behavior using ML",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": predictor.is_loaded,
        "model_type": "ML Model" if not predictor.fallback_mode else "Rule-based Fallback",
        "feature_count": len(predictor.feature_names),
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health",
            "model_info": "GET /model/info",
            "test": "GET /test",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational",
        "model_status": "loaded" if predictor.is_loaded else "not_loaded",
        "model_type": "ML Model" if not predictor.fallback_mode else "Rule-based Fallback",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict")
async def predict_dropoff(user_data: Dict[str, Any]):
    """
    Predict movie dropoff probability for a user using final trained model
    """
    try:
        # Validate input
        is_valid, errors = validate_user_data(user_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail={"errors": errors})
        
        # Get prediction
        probability, risk_level, recommendations, user_segment = predictor.predict_dropoff(user_data)
        
        # Format response
        response = format_prediction_response(probability, risk_level, recommendations, user_segment)
        
        return {
            "input_data": user_data,
            "prediction": response,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/test")
async def test_prediction():
    """Test endpoint with sample data"""
    test_data = {
        "boring_plot": 1,
        "total_stopping_reasons": 4,
        "stop_historical": 0,
        "enjoy_action": 1,
        "genre_completion_ratio": 0.6,
        "patience_score": 0.33,
        "attention_span_score": 0.5,
        "total_multitasking_behaviors": 2,
        "social_influence_score": 4,
        "is_weekend": 1
    }
    
    probability, risk_level, recommendations, user_segment = predictor.predict_dropoff(test_data)
    
    return {
        "test_data": test_data,
        "prediction": {
            "probability": round(probability, 3),
            "risk_level": risk_level,
            "user_segment": user_segment,
            "recommendations": recommendations,
            "model_type": "ML Model" if not predictor.fallback_mode else "Rule-based Fallback"
        },
        "status": "test_successful",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info")
async def get_model_info():
    """Get detailed model information"""
    return {
        "model_info": predictor.model_info,
        "feature_count": len(predictor.feature_names),
        "features": predictor.feature_names[:20],  # Show first 20 features
        "total_features": len(predictor.feature_names),
        "model_type": "ML Model" if not predictor.fallback_mode else "Rule-based Fallback",
        "status": "loaded" if predictor.is_loaded else "not_loaded",
        "fallback_mode": predictor.fallback_mode,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/movies")
async def get_movies(
    limit: int = 50, 
    genre: str = None, 
    min_rating: float = None,
    year_from: int = None,
    year_to: int = None
):
    """Get movie data from cleaned IMDB dataset"""
    try:
        # Load the cleaned IMDB data
        movies_path = "../movies_seeding/cleaned_imdb_data.csv"
        
        if not os.path.exists(movies_path):
            # Try alternative path
            movies_path = "../data_preprocessing/imdb_data.csv"
        
        if not os.path.exists(movies_path):
            raise HTTPException(status_code=404, detail="Movie data file not found")
        
        # Load and process movie data
        df = pd.read_csv(movies_path)
        
        # Apply filters
        if genre and genre.lower() != 'all':
            df = df[df['genres'].str.contains(genre, case=False, na=False)]
        
        if min_rating:
            df = df[df['imdb_score'] >= min_rating]
        
        if year_from:
            df = df[df['title_year'] >= year_from]
        
        if year_to:
            df = df[df['title_year'] <= year_to]
        
        # Sort by IMDB score and limit results
        df = df.sort_values('imdb_score', ascending=False).head(limit)
        
        # Convert to API format
        movies = []
        for _, row in df.iterrows():
            # Parse genres
            genres_str = str(row.get('genres', ''))
            genres = [g.strip() for g in genres_str.split(',') if g.strip()]
            
            movie = {
                "id": len(movies) + 1,
                "title": str(row.get('movie_title', 'Unknown')),
                "genre": genres,
                "year": int(row.get('title_year', 0)) if pd.notna(row.get('title_year')) else None,
                "director": str(row.get('director_name', 'Unknown')),
                "runtime": int(row.get('duration', 0)) if pd.notna(row.get('duration')) else None,
                "imdbRating": float(row.get('imdb_score', 0)) if pd.notna(row.get('imdb_score')) else None,
                "posterUrl": "🎬",  # Placeholder for now
                "description": f"A {row.get('main_genre', 'movie')} film from {row.get('title_year', 'unknown year')}",
                "mainGenre": str(row.get('main_genre', 'Unknown')),
                "contentRating": str(row.get('content_rating', 'Not Rated')) if pd.notna(row.get('content_rating')) else 'Not Rated',
                "starCast": str(row.get('star_cast', 'Unknown')) if pd.notna(row.get('star_cast')) else 'Unknown'
            }
            movies.append(movie)
        
        return {
            "movies": movies,
            "total": len(movies),
            "filters_applied": {
                "genre": genre,
                "min_rating": min_rating,
                "year_from": year_from,
                "year_to": year_to,
                "limit": limit
            }
        }
        
    except Exception as e:
        print(f"Error loading movies: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading movie data: {str(e)}")

@app.post("/movies/{movie_id}/predict")
async def predict_movie_completion(movie_id: int, user_data: dict):
    """Predict completion likelihood for a specific movie"""
    try:
        # Use the existing predictor method
        probability, risk_level, recommendations, user_segment = predictor.predict_dropoff(user_data)
        
        return {
            "movie_id": movie_id,
            "completion_likelihood": 1.0 - probability,  # Convert dropoff to completion
            "dropoff_probability": probability,
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.8,
            "factors": []
        }
        
    except Exception as e:
        print(f"Error predicting for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Movie Dropoff Prediction API with Real ML Model...")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
