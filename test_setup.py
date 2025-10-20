#!/usr/bin/env python3
"""
Test script to verify Lead Generator setup
"""

import os
import sys
from business_finder import BusinessFinder, BusinessSearchParams
from category_helper import CategoryHelper

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing imports...")
    try:
        from business_finder import BusinessFinder, BusinessSearchParams
        from category_helper import CategoryHelper
        from config import YELP_API_KEY, GOOGLE_API_KEY
        print("✅ All imports successful!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_category_helper():
    """Test category helper functionality"""
    print("\n🧪 Testing Category Helper...")
    try:
        helper = CategoryHelper()
        popular = helper.get_popular_categories()
        print(f"✅ Found {len(popular)} popular categories")
        
        # Test search
        results = helper.search_categories("restaurant", limit=3)
        print(f"✅ Found {len(results)} restaurant categories")
        
        return True
    except Exception as e:
        print(f"❌ Category helper error: {e}")
        return False

def test_business_finder():
    """Test business finder initialization"""
    print("\n🧪 Testing Business Finder...")
    try:
        # Check for API keys
        yelp_key = os.getenv('YELP_API_KEY')
        google_key = os.getenv('GOOGLE_API_KEY')
        
        if not yelp_key:
            print("⚠️  YELP_API_KEY not found in environment")
        if not google_key:
            print("⚠️  GOOGLE_API_KEY not found in environment")
        
        if yelp_key and google_key:
            finder = BusinessFinder(yelp_api_key=yelp_key, google_api_key=google_key)
            print("✅ Business Finder initialized successfully!")
            return True
        else:
            print("⚠️  Skipping Business Finder test - API keys not available")
            return True
    except Exception as e:
        print(f"❌ Business Finder error: {e}")
        return False

def test_search_params():
    """Test BusinessSearchParams dataclass"""
    print("\n🧪 Testing BusinessSearchParams...")
    try:
        params = BusinessSearchParams(
            city="San Francisco",
            industry="restaurants",
            distance_miles=5.0,
            max_results=10
        )
        print(f"✅ Created search params: {params.city}, {params.industry}")
        return True
    except Exception as e:
        print(f"❌ BusinessSearchParams error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Lead Generator Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_category_helper,
        test_business_finder,
        test_search_params
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Lead Generator is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set up your API keys in .env file")
        print("2. Run: python main.py")
        print("3. Or run: python export_businesses.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
