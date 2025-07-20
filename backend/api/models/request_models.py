# We'll add pydantic imports once it installs
# from pydantic import BaseModel, Field
# from typing import Optional

# For now, here's the structure we'll use:
"""
class UserSurveyData(BaseModel):
    # Main behavioral indicators
    boring_plot: int = Field(0, ge=0, le=1, description="Stops due to boring plot")
    historical_genre_stopped: int = Field(0, ge=0, le=1, description="Stops historical movies")
    feeling_bored_pause: int = Field(0, ge=0, le=1, description="Pauses when bored")
    
    # Behavioral counts and scores
    total_genres_stopped: int = Field(3, ge=0, description="Total genres stopped")
    total_stopping_reasons: int = Field(3, ge=0, description="Total stopping reasons")
    total_multitasking_behaviors: int = Field(2, ge=0, description="Multitasking behaviors")
    
    # Calculated scores from your feature engineering
    genre_completion_ratio: float = Field(0.5, ge=0.0, le=1.0, description="Genre completion ratio")
    patience_score: float = Field(0.5, ge=0.0, le=1.0, description="User patience score")
    attention_span_score: float = Field(0.5, ge=0.0, le=1.0, description="Attention span score")
    social_influence_score: int = Field(3, ge=0, description="Social influence score")
    
    # Discovery and viewing patterns
    discovers_via_reviews: int = Field(0, ge=0, le=1, description="Discovers via reviews")
    chooses_entertainment: int = Field(1, ge=0, le=1, description="Watches for entertainment")
    watches_streaming_home: int = Field(1, ge=0, le=1, description="Streams at home")
    scrolls_phone: int = Field(0, ge=0, le=1, description="Uses phone while watching")
    does_chores: int = Field(0, ge=0, le=1, description="Does chores while watching")
    
    # Contextual features
    is_weekend: int = Field(0, ge=0, le=1, description="Is weekend viewing")
    behavior_cluster: int = Field(1, ge=0, description="Behavioral cluster ID")
    
    class Config:
        schema_extra = {
            "example": {
                "boring_plot": 1,
                "historical_genre_stopped": 0,
                "feeling_bored_pause": 1,
                "total_genres_stopped": 3,
                "total_stopping_reasons": 4,
                "total_multitasking_behaviors": 2,
                "genre_completion_ratio": 0.6,
                "patience_score": 0.33,
                "attention_span_score": 0.5,
                "social_influence_score": 4,
                "discovers_via_reviews": 0,
                "chooses_entertainment": 1,
                "watches_streaming_home": 1,
                "scrolls_phone": 1,
                "does_chores": 0,
                "is_weekend": 1,
                "behavior_cluster": 2
            }
        }
"""

# Placeholder dictionary structure for now
EXAMPLE_USER_DATA = {
    "boring_plot": 1,
    "historical_genre_stopped": 0,
    "feeling_bored_pause": 1,
    "total_genres_stopped": 3,
    "total_stopping_reasons": 4,
    "total_multitasking_behaviors": 2,
    "genre_completion_ratio": 0.6,
    "patience_score": 0.33,
    "attention_span_score": 0.5,
    "social_influence_score": 4,
    "discovers_via_reviews": 0,
    "chooses_entertainment": 1,
    "watches_streaming_home": 1,
    "scrolls_phone": 1,
    "does_chores": 0,
    "is_weekend": 1,
    "behavior_cluster": 2
}
