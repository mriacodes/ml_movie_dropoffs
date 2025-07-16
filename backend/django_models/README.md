# Django Models Directory

This directory contains all the exported machine learning model files and utilities needed to integrate the movie dropoff prediction system into a Django web application.

## Files Overview

### 📊 Model Files
- **`movie_dropoff_model.pkl`** (173 KB) - Trained Gradient Boosting classifier
  - Best performing model with 65% accuracy and 75.9% F1-score
  - Predicts likelihood of user dropping off before completing a movie

- **`smote_transformer.pkl`** (13 KB) - SMOTE balancing transformer
  - Used during training to handle class imbalance
  - May be needed for consistent preprocessing

### 📋 Configuration Files
- **`model_info.json`** (4 KB) - Model metadata and performance metrics
  - Feature names, model type, training date
  - Performance metrics: accuracy, F1-score, precision, recall, ROC-AUC
  - 3,768 feature columns used for prediction

- **`class_mappings.json`** (279 bytes) - Class label definitions
  - 0: "Will Complete Movie"
  - 1: "Will Drop Off"
  - Training data distribution information

- **`survey_questions.json`** (2 KB) - Survey form configuration
  - 12 questions for user profiling
  - Question types: boolean, integer, float, multiple_choice
  - Field mappings for Django form integration

### 🛠️ Django Utilities
- **`django_prediction_utils.py`** - Main prediction class
  - `MovieDropoffPredictor` class for real-time predictions
  - User input preprocessing and feature mapping
  - Batch predictions for multiple movies
  - Movie-specific probability adjustments

- **`django_retraining_utils.py`** - Continuous learning system
  - `ModelRetrainingSystem` class for model updates
  - User feedback collection and processing
  - Automated retraining with performance validation
  - Django management command templates

## Integration Steps

1. **Copy Files**: Move all files to your Django project's `ml_models/` directory
2. **Install Dependencies**: 
   ```
   pip install scikit-learn pandas numpy joblib imbalanced-learn
   ```
3. **Update Settings**: Add `ml_models/` path to Django settings
4. **Import Classes**: Use the utility classes in your Django views
5. **Create Forms**: Build survey forms using `survey_questions.json`
6. **Test Integration**: Verify predictions work with sample data

## Model Performance

- **Algorithm**: Gradient Boosting Classifier
- **Accuracy**: 65%
- **F1-Score**: 75.9%
- **Precision**: 68.8%
- **Recall**: 84.6%
- **ROC-AUC**: 62.6%

## User Flow

1. User completes survey (12 questions)
2. System processes responses using `MovieDropoffPredictor`
3. Based on genre preferences, fetch movies from IMDB
4. Calculate dropoff probability for each movie
5. Display movies with completion likelihood scores
6. Collect user feedback for continuous model improvement

## Business Value

- **Proactive Engagement**: Identify users likely to drop off
- **Personalized Recommendations**: Adjust suggestions based on completion probability
- **Reduced Churn**: Target interventions for high-risk users
- **Data-Driven Decisions**: Continuous learning from user behavior

## Next Steps

1. Set up Django project structure
2. Integrate IMDB movie database
3. Implement web interface
4. Deploy prediction system
5. Monitor and retrain model with new data

---
*Generated from movie dropoff prediction ML pipeline*
*Last Updated: July 16, 2025*
