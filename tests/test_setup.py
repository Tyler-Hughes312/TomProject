"""
Test setup for Lead Generator
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from leadgen import app
        print("✅ Flask app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Flask app: {e}")
        return False
    
    try:
        from business_finder import BusinessFinder
        print("✅ BusinessFinder imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import BusinessFinder: {e}")
        return False
    
    try:
        from category_helper import CategoryHelper
        print("✅ CategoryHelper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CategoryHelper: {e}")
        return False
    
    return True

def test_api_keys():
    """Test that API keys are configured"""
    yelp_key = os.getenv('YELP_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if yelp_key:
        print("✅ YELP_API_KEY is configured")
    else:
        print("⚠️ YELP_API_KEY is not configured")
    
    if google_key:
        print("✅ GOOGLE_API_KEY is configured")
    else:
        print("⚠️ GOOGLE_API_KEY is not configured")
    
    return bool(yelp_key and google_key)

def test_flask_app():
    """Test that Flask app can be created"""
    try:
        from leadgen import app
        with app.app_context():
            print("✅ Flask app context created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create Flask app context: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Lead Generator setup...")
    print()
    
    all_tests_passed = True
    
    # Test imports
    print("Testing imports...")
    if not test_imports():
        all_tests_passed = False
    print()
    
    # Test API keys
    print("Testing API keys...")
    if not test_api_keys():
        all_tests_passed = False
    print()
    
    # Test Flask app
    print("Testing Flask app...")
    if not test_flask_app():
        all_tests_passed = False
    print()
    
    if all_tests_passed:
        print("🎉 All tests passed! Lead Generator is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
