# Request models structure - now with pydantic support
from pydantic import BaseModel, Field
from typing import Optional

class UserSurveyData(BaseModel):
    """User survey data based on the actual survey questions"""
    
    # Main behavioral indicators (matching survey_questions.json)
    boring_plot: int = Field(0, ge=0, le=1, description="Stops due to boring plot")
    total_stopping_reasons: int = Field(3, ge=1, le=6, description="Total stopping reasons")
    stop_historical: int = Field(0, ge=0, le=1, description="Stops historical movies")
    enjoy_action: int = Field(1, ge=0, le=1, description="Enjoys action movies")
    
    # Behavioral scores and patterns
    total_genres_stopped: int = Field(2, ge=0, le=10, description="Total genres stopped")
    genre_completion_ratio: float = Field(0.6, ge=0.0, le=1.0, description="Genre completion ratio")
    patience_score: float = Field(0.5, ge=0.0, le=1.0, description="User patience score")
    attention_span_score: float = Field(0.5, ge=0.0, le=1.0, description="Attention span score")
    
    # Multitasking and social behavior
    total_multitasking_behaviors: int = Field(2, ge=0, le=5, description="Multitasking behaviors")
    social_influence_score: int = Field(3, ge=0, le=10, description="Social influence score")
    behavior_cluster: int = Field(1, ge=0, le=5, description="Behavioral cluster ID")
    
    # Contextual features
    is_weekend: int = Field(0, ge=0, le=1, description="Is weekend viewing")
    watch_frequency_score: Optional[float] = Field(3.0, ge=1.0, le=5.0, description="Watch frequency")
    
    # Additional survey fields
    feeling_bored_pause: Optional[int] = Field(0, ge=0, le=1, description="Pauses when bored")
    discovers_via_reviews: Optional[int] = Field(0, ge=0, le=1, description="Discovers via reviews")
    chooses_entertainment: Optional[int] = Field(1, ge=0, le=1, description="Watches for entertainment")
    watches_streaming_home: Optional[int] = Field(1, ge=0, le=1, description="Streams at home")
    scrolls_phone: Optional[int] = Field(0, ge=0, le=1, description="Uses phone while watching")
    does_chores: Optional[int] = Field(0, ge=0, le=1, description="Does chores while watching")
    
    class Config:
        schema_extra = {
            "example": {
                "boring_plot": 1,
                "total_stopping_reasons": 4,
                "stop_historical": 0,
                "enjoy_action": 1,
                "total_genres_stopped": 3,
                "genre_completion_ratio": 0.6,
                "patience_score": 0.33,
                "attention_span_score": 0.5,
                "total_multitasking_behaviors": 2,
                "social_influence_score": 4,
                "behavior_cluster": 2,
                "is_weekend": 1,
                "watch_frequency_score": 3.5,
                "feeling_bored_pause": 1,
                "discovers_via_reviews": 0,
                "chooses_entertainment": 1,
                "watches_streaming_home": 1,
                "scrolls_phone": 1,
                "does_chores": 0
            }
        }

# Quick test data for API testing
EXAMPLE_USER_DATA = {
    "boring_plot": 1,
    "total_stopping_reasons": 4,
    "stop_historical": 0,
    "enjoy_action": 1,
    "total_genres_stopped": 3,
    "genre_completion_ratio": 0.6,
    "patience_score": 0.33,
    "attention_span_score": 0.5,
    "total_multitasking_behaviors": 2,
    "social_influence_score": 4,
    "behavior_cluster": 2,
    "is_weekend": 1
}
