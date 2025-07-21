from config import config
import os
import json
import pandas as pd
import numpy as np
import joblib
import warnings
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

app = FastAPI(
    title="Movie Dropoff Prediction API",
    description="ML API for predicting movie watching dropoff behavior",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check route
@app.get("/ping")
def ping():
    return "pong"



class MovieDropoffPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.model_info = {}
        self.is_loaded = False
        self.fallback_mode = False
        
        self._load_real_model()
    
    def _load_real_model(self):
        """Load final trained model using config paths"""
        try:
            import sklearn
            print(f"Current scikit-learn version: {sklearn.__version__}")
            
            # Use absolute path resolution
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_file_dir, "..", "django_models", "movie_dropoff_model_optimized.pkl")
            model_path = os.path.normpath(model_path)
            
            print(f"Trying to load model from: {model_path}")
            print(f"Model file exists: {os.path.exists(model_path)}")
            print(f"Current working directory: {os.getcwd()}")
            
            if not os.path.exists(model_path):
                print("Model not found! Directory structure:")
                django_models_dir = os.path.join(current_file_dir, "..", "django_models")
                django_models_dir = os.path.normpath(django_models_dir)
                
                print(f"Looking in: {django_models_dir}")
                if os.path.exists(django_models_dir):
                    files = os.listdir(django_models_dir)
                    print(f"Files found: {files}")
                    
                    # Look for any .pkl files
                    pkl_files = [f for f in files if f.endswith('.pkl')]
                    if pkl_files:
                        print(f"Found pickle files: {pkl_files}")
                        # Try the first pickle file found
                        model_path = os.path.join(django_models_dir, pkl_files[0])
                        print(f"Trying alternate model: {model_path}")
                    else:
                        raise FileNotFoundError("No pickle files found in django_models directory")
                else:
                    print(f"django_models directory doesn't exist: {django_models_dir}")
                    raise FileNotFoundError(f"Directory not found: {django_models_dir}")
            
            # Suppress version warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                
                print("Attempting to load model...")
                self.model = joblib.load(model_path)
                print("Model loaded successfully!")
                
                # Get model info
                print(f"Model type: {type(self.model)}")
                print(f"Model classes: {getattr(self.model, 'classes_', 'Not available')}")
                
                # Try to get feature names
                if hasattr(self.model, 'feature_names_in_'):
                    self.feature_names = list(self.model.feature_names_in_)
                    print(f"Features from model: {len(self.feature_names)}")
                else:
                    print("Model doesn't have feature_names_in_, using fallback features")
                    self.feature_names = self._get_basic_features()
                
                # Test prediction
                test_data = pd.DataFrame([[0.5] * len(self.feature_names)], columns=self.feature_names)
                try:
                    if hasattr(self.model, 'predict_proba'):
                        test_pred = self.model.predict_proba(test_data)
                        print(f"Test prediction successful: {test_pred.shape}")
                    else:
                        test_pred = self.model.predict(test_data)
                        print(f"Test prediction successful: {test_pred}")
                    
                    self.is_loaded = True
                    self.fallback_mode = False
                    print("SUCCESS: Real ML model is loaded and functional!")
                    return
                    
                except Exception as pred_error:
                    print(f"Model prediction test failed: {pred_error}")
                    print("Model loaded but can't make predictions, using fallback")
                    raise pred_error
        
        except Exception as e:
            print(f"FAILED to load real model: {e}")
            print("Falling back to rule-based model")
            self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Load fallback rule-based model"""
        print("Loading fallback rule-based model...")
        self.fallback_mode = True
        self.is_loaded = True
        self.feature_names = self._get_basic_features()
        self.model_info = {
            "model_name": "Rule-based Fallback",
            "version": "1.0.0",
            "type": "fallback"
        }

    def _get_basic_features(self):
        """Get basic feature set for fallback"""
        return [
            'boring_plot', 'total_stopping_reasons', 'patience_score',
            'attention_span_score', 'genre_completion_ratio',
            'stop_historical', 'stop_action', 'stop_comedy',
            'pause_when_bored', 'viewer_age_group'
        ]
    
    def _prepare_features(self, user_data: dict) -> pd.DataFrame:
        """Prepare features for model prediction"""
        if self.fallback_mode:
            feature_dict = {}
            for feature in self.feature_names:
                feature_dict[feature] = user_data.get(feature, 0)
            return pd.DataFrame([feature_dict])
        
        else:
            feature_dict = {}
            
            for feature in self.feature_names:
                feature_dict[feature] = user_data.get(feature, 0)
            
            feature_df = pd.DataFrame([feature_dict])
            
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
            print(f"Prediction error: {e}, falling back to rule-based")
            return self._fallback_prediction(user_data)
    
    def _real_model_prediction(self, user_data: dict):
        """Use the real trained model for prediction"""
        feature_df = self._prepare_features(user_data)
        
        probability = self.model.predict_proba(feature_df)[0][1]  
        
        risk_level, user_segment, recommendations = self._analyze_prediction(probability, user_data)
        
        return probability, risk_level, recommendations, user_segment
    
    def _fallback_prediction(self, user_data: dict):
        """Rule-based prediction fallback"""
        risk_score = 0.0
        
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
        
        probability = min(max(risk_score, 0.05), 0.95)
        
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

predictor = MovieDropoffPredictor()

def validate_user_data(data: dict) -> tuple[bool, list]:
    """Validate input data"""
    errors = []
    required_fields = ["boring_plot", "total_stopping_reasons"]
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
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

@app.on_event("startup")
async def startup_event():
    """Initialize the API on startup"""
    print("Movie Dropoff Prediction API Started")
    print(f"Predictor loaded: {predictor.is_loaded}")
    print(f"Model type: {'Real ML Model' if not predictor.fallback_mode else 'Fallback Rule-based'}")
    print(f"Features available: {len(predictor.feature_names)}")
    print("API ready for predictions!")

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
        is_valid, errors = validate_user_data(user_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail={"errors": errors})
        
        probability, risk_level, recommendations, user_segment = predictor.predict_dropoff(user_data)
        
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
        "features": predictor.feature_names[:20],
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
        movies_path = "cleaned_imdb_data.csv"
        
        if not os.path.exists(movies_path):
            raise HTTPException(status_code=404, detail="Movie data file not found")
        
        df = pd.read_csv(movies_path)
        print(f"Loaded {len(df)} movies from dataset")
        
        print("Available columns:", list(df.columns))
        
        if genre and genre.lower() != 'all':
            if 'genres' in df.columns:
                df = df[df['genres'].str.contains(genre, case=False, na=False)]
            elif 'genre' in df.columns:
                df = df[df['genre'].str.contains(genre, case=False, na=False)]
        
        if min_rating:
           
            if 'imdb_score' in df.columns:
                df = df[df['imdb_score'] >= min_rating]
        
        if year_from:
            
            if 'release_year' in df.columns:
                df = df[df['release_year'] >= year_from]
            elif 'title_year' in df.columns:
                df = df[df['title_year'] >= year_from]
        
        if year_to:
            if 'release_year' in df.columns:
                df = df[df['release_year'] <= year_to]
            elif 'title_year' in df.columns:
                df = df[df['title_year'] <= year_to]
        
        # Sort and limit results
        if 'imdb_score' in df.columns:
            df = df.sort_values('imdb_score', ascending=False).head(limit)
        else:
            df = df.head(limit)
        
        # Convert to API format based on your CSV structure
        movies = []
        for idx, row in df.iterrows():
            movie = {
                "id": idx,
                "title": str(row.iloc[0]),
                "year": int(row.iloc[2]) if pd.notna(row.iloc[2]) else 2000,
                "imdbRating": float(row.iloc[1]) if pd.notna(row.iloc[1]) else 5.0,
                "genre": str(row.iloc[4]).split(',') if pd.notna(row.iloc[4]) else ["Unknown"],
                "director": str(row.iloc[5]) if pd.notna(row.iloc[5]) else "Unknown",
                "runtime": int(row.iloc[8]) if pd.notna(row.iloc[8]) and str(row.iloc[8]).replace('.','').isdigit() else 120,
                "contentRating": str(row.iloc[3]) if pd.notna(row.iloc[3]) else "Not Rated",
                "starCast": str(row.iloc[6]) if pd.notna(row.iloc[6]) else "Unknown Cast",
                "posterUrl": "movie-poster",
                "description": f"A {str(row.iloc[4]).split(',')[0] if pd.notna(row.iloc[4]) else 'movie'} film",
                "mainGenre": str(row.iloc[4]).split(',')[0] if pd.notna(row.iloc[4]) else "Unknown"
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
        probability, risk_level, recommendations, user_segment = predictor.predict_dropoff(user_data)
        
        return {
            "movie_id": movie_id,
            "completion_likelihood": 1.0 - probability,
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
    print("Starting Movie Dropoff Prediction API with Real ML Model...")
    print("API will be available at: http://localhost:8000")
    print("Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
