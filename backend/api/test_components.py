#!/usr/bin/env python3
"""
Test script for Movie Dropoff Prediction API components
Run this to verify all components work before starting FastAPI
"""

import sys
import os

def test_imports():
    """Test that all our custom modules import correctly"""
    print("🧪 Testing imports...")
    try:
        from services.prediction_service import prediction_service
        print("✓ Prediction service imported")
        
        from utils.data_utils import validate_user_data, health_check, preprocess_user_data
        print("✓ Data utilities imported")
        
        from models.response_models import create_prediction_response, create_health_response
        print("✓ Response models imported")
        
        from config import config
        print("✓ Configuration imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_prediction_service():
    """Test the prediction service functionality"""
    print("\n🧪 Testing prediction service...")
    try:
        from services.prediction_service import prediction_service
        
        # Load model (placeholder)
        success = prediction_service.load_model()
        print(f"✓ Model loading: {success}")
        
        # Test prediction
        test_user = {
            'age': 28,
            'streaming_frequency': 'moderate',
            'subscription_duration': 8,
            'price_sensitivity': 'low',
            'customer_support_contacts': 1
        }
        
        probability, risk_level, recommendations, segment = prediction_service.predict_dropoff(test_user)
        
        print(f"✓ Test prediction successful:")
        print(f"  - Probability: {probability}")
        print(f"  - Risk Level: {risk_level}")
        print(f"  - User Segment: {segment}")
        print(f"  - Recommendations: {len(recommendations)} items")
        
        return True
    except Exception as e:
        print(f"✗ Prediction service test failed: {e}")
        return False

def test_data_utils():
    """Test data utilities"""
    print("\n🧪 Testing data utilities...")
    try:
        from utils.data_utils import validate_user_data, health_check, preprocess_user_data
        
        # Test validation
        test_data = {
            'age': 25,
            'streaming_frequency': 'moderate',
            'subscription_duration': 6
        }
        
        is_valid, errors = validate_user_data(test_data)
        print(f"✓ Data validation: {is_valid} (errors: {len(errors)})")
        
        # Test preprocessing
        processed = preprocess_user_data(test_data)
        print(f"✓ Data preprocessing: {len(processed)} fields processed")
        
        # Test health check
        health = health_check()
        print(f"✓ Health check: {health['status']}")
        
        return True
    except Exception as e:
        print(f"✗ Data utils test failed: {e}")
        return False

def test_basic_ml():
    """Test basic ML dependencies"""
    print("\n🧪 Testing ML dependencies...")
    try:
        import pandas as pd
        import numpy as np
        
        # Test pandas
        df = pd.DataFrame({'test': [1, 2, 3]})
        print(f"✓ Pandas {pd.__version__} working")
        
        # Test numpy
        arr = np.array([1, 2, 3])
        mean_val = np.mean(arr)
        print(f"✓ NumPy {np.__version__} working (test mean: {mean_val})")
        
        return True
    except Exception as e:
        print(f"✗ ML dependencies test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Movie Dropoff Prediction API - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Basic ML Dependencies", test_basic_ml),
        ("Module Imports", test_imports),
        ("Data Utilities", test_data_utils),
        ("Prediction Service", test_prediction_service)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🏁 Tests completed: {passed}/{len(results)} passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API components are ready.")
        print("💡 You can now start the FastAPI server once dependencies finish installing.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
