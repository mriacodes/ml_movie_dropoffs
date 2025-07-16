import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE
import os
from django.conf import settings

class ModelRetrainingSystem:
    """
    System for collecting new user data and retraining the model
    """
    
    def __init__(self):
        self.models_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        self.data_dir = os.path.join(settings.BASE_DIR, 'ml_data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_user_feedback(self, user_responses, actual_behavior, movie_info=None):
        """
        Save user survey responses and actual movie completion behavior
        
        Args:
            user_responses (dict): Original survey responses
            actual_behavior (dict): Actual completion/dropoff data
                - movie_id: str
                - completed: bool
                - watch_time: float (minutes watched)
                - total_runtime: float (total movie length)
                - feedback_rating: int (1-5)
            movie_info (dict): Movie metadata (optional)
        """
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_responses': user_responses,
            'actual_behavior': actual_behavior,
            'movie_info': movie_info or {}
        }
        
        # Append to feedback file
        feedback_file = os.path.join(self.data_dir, 'user_feedback.jsonl')
        with open(feedback_file, 'a') as f:
            f.write(json.dumps(feedback_entry) + '\n')
    
    def load_feedback_data(self):
        """Load all collected user feedback data"""
        feedback_file = os.path.join(self.data_dir, 'user_feedback.jsonl')
        
        if not os.path.exists(feedback_file):
            return pd.DataFrame()
        
        feedback_data = []
        with open(feedback_file, 'r') as f:
            for line in f:
                feedback_data.append(json.loads(line.strip()))
        
        return pd.DataFrame(feedback_data)
    
    def prepare_retraining_data(self):
        """
        Convert feedback data into format suitable for model retraining
        
        Returns:
            tuple: (X_new, y_new) - Features and labels for retraining
        """
        feedback_df = self.load_feedback_data()
        
        if feedback_df.empty:
            return None, None
        
        # Extract features and labels
        features_list = []
        labels_list = []
        
        for _, row in feedback_df.iterrows():
            user_responses = row['user_responses']
            actual_behavior = row['actual_behavior']
            
            # Convert user responses to feature vector
            features = self.responses_to_features(user_responses)
            
            # Determine label based on actual behavior
            if 'completed' in actual_behavior:
                # Direct completion indicator
                label = 0 if actual_behavior['completed'] else 1
            else:
                # Use watch time ratio as proxy
                watch_ratio = actual_behavior.get('watch_time', 0) / actual_behavior.get('total_runtime', 1)
                label = 0 if watch_ratio >= 0.8 else 1  # 80% completion threshold
            
            features_list.append(features)
            labels_list.append(label)
        
        X_new = pd.DataFrame(features_list)
        y_new = pd.Series(labels_list)
        
        return X_new, y_new
    
    def responses_to_features(self, user_responses):
        """Convert user responses to feature vector matching training format"""
        # Load original feature names
        with open(os.path.join(self.models_dir, 'model_info.json'), 'r') as f:
            model_info = json.load(f)
        
        feature_names = model_info['feature_names']
        features = {name: 0 for name in feature_names}
        
        # Mapping logic (same as in prediction utils)
        feature_mapping = {
            'boring_plot': 'in_general_what_are_the_main_reasons_you_stop_watching_movies_before_finishing_boring_uninteresting_plot',
            'stop_historical': 'which_genres_do_you_find_yourself_stopping_more_often_before_finishing_historical',
            'pause_when_bored': 'why_do_you_usually_pause_the_movie_feeling_bored_or_uninterested',
            'focus_only': 'do_you_usually_do_other_things_while_watching_movies_no_i_usually_focus_only_on_the_movie',
            'discover_trailer': 'how_do_you_usually_discover_movies_you_decide_to_watch_trailer',
            'watch_for_entertainment': 'why_do_you_usually_choose_to_watch_movies_entertainment',
            'enjoy_action': 'which_genres_do_you_enjoy_watching_the_most_action',
            'enjoy_romance': 'which_genres_do_you_enjoy_watching_the_most_romance',
            'total_stopping_reasons': 'total_stopping_reasons',
            'patience_score': 'patience_score',
            'completion_ratio': 'genre_completion_ratio'
        }
        
        for user_field, model_feature in feature_mapping.items():
            if user_field in user_responses and model_feature in features:
                features[model_feature] = user_responses[user_field]
        
        return features
    
    def retrain_model(self, min_new_samples=50):
        """
        Retrain the model with new feedback data
        
        Args:
            min_new_samples (int): Minimum new samples required for retraining
            
        Returns:
            dict: Retraining results and performance metrics
        """
        # Load new data
        X_new, y_new = self.prepare_retraining_data()
        
        if X_new is None or len(X_new) < min_new_samples:
            return {
                'success': False,
                'reason': f'Insufficient new samples. Need {min_new_samples}, got {len(X_new) if X_new is not None else 0}'
            }
        
        # Load original training data if available
        original_data_file = os.path.join(self.data_dir, 'original_training_data.pkl')
        if os.path.exists(original_data_file):
            original_data = joblib.load(original_data_file)
            X_original = original_data['X']
            y_original = original_data['y']
            
            # Combine original and new data
            X_combined = pd.concat([X_original, X_new], ignore_index=True)
            y_combined = pd.concat([y_original, y_new], ignore_index=True)
        else:
            X_combined = X_new
            y_combined = y_new
        
        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_combined, y_combined, test_size=0.2, stratify=y_combined, random_state=42
        )
        
        # Apply SMOTE to training data
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        # Train new model (using same type as original)
        model = GradientBoostingClassifier(random_state=42, n_estimators=100)
        model.fit(X_train_balanced, y_train_balanced)
        
        # Evaluate performance
        y_val_pred = model.predict(X_val)
        
        metrics = {
            'accuracy': accuracy_score(y_val, y_val_pred),
            'f1_score': f1_score(y_val, y_val_pred),
            'precision': precision_score(y_val, y_val_pred),
            'recall': recall_score(y_val, y_val_pred)
        }
        
        # Save updated model if performance is acceptable
        if metrics['f1_score'] >= 0.7:  # Minimum acceptable F1 score
            # Backup current model
            current_model_path = os.path.join(self.models_dir, 'movie_dropoff_model.pkl')
            backup_path = os.path.join(self.models_dir, f'movie_dropoff_model_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pkl')
            if os.path.exists(current_model_path):
                os.rename(current_model_path, backup_path)
            
            # Save new model
            joblib.dump(model, current_model_path)
            
            # Update model info
            with open(os.path.join(self.models_dir, 'model_info.json'), 'r') as f:
                model_info = json.load(f)
            
            model_info['last_retrained'] = datetime.now().isoformat()
            model_info['retraining_samples'] = len(X_combined)
            model_info['performance_metrics'] = metrics
            
            with open(os.path.join(self.models_dir, 'model_info.json'), 'w') as f:
                json.dump(model_info, f, indent=2)
            
            return {
                'success': True,
                'metrics': metrics,
                'training_samples': len(X_combined),
                'new_samples': len(X_new)
            }
        else:
            return {
                'success': False,
                'reason': f'Model performance below threshold. F1: {metrics["f1_score"]:.3f}',
                'metrics': metrics
            }
    
    def schedule_retraining_check(self):
        """
        Check if retraining is needed based on data collection
        
        Returns:
            dict: Recommendation for retraining
        """
        feedback_df = self.load_feedback_data()
        
        if feedback_df.empty:
            return {'should_retrain': False, 'reason': 'No feedback data available'}
        
        # Check data volume
        new_samples = len(feedback_df)
        
        # Check data recency
        feedback_df['timestamp'] = pd.to_datetime(feedback_df['timestamp'])
        recent_data = feedback_df[feedback_df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(days=30)]
        
        recommendation = {
            'should_retrain': False,
            'total_samples': new_samples,
            'recent_samples': len(recent_data),
            'recommendation': ''
        }
        
        if new_samples >= 100 and len(recent_data) >= 20:
            recommendation['should_retrain'] = True
            recommendation['recommendation'] = 'Sufficient data for retraining'
        elif new_samples >= 50:
            recommendation['recommendation'] = 'Consider retraining soon'
        else:
            recommendation['recommendation'] = 'Continue collecting data'
        
        return recommendation

# Django management command example for retraining:
"""
# Create: management/commands/retrain_model.py

from django.core.management.base import BaseCommand
from yourapp.ml_utils import ModelRetrainingSystem

class Command(BaseCommand):
    help = 'Retrain the movie dropoff prediction model'
    
    def handle(self, *args, **options):
        retrainer = ModelRetrainingSystem()
        
        # Check if retraining is recommended
        check = retrainer.schedule_retraining_check()
        self.stdout.write(f"Retraining check: {check}")
        
        if check['should_retrain']:
            result = retrainer.retrain_model()
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(f'Model retrained successfully! F1: {result["metrics"]["f1_score"]:.3f}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Retraining failed: {result["reason"]}')
                )
        else:
            self.stdout.write('Retraining not recommended at this time')

# Usage: python manage.py retrain_model
"""
