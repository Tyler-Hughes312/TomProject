#!/usr/bin/env python3
"""
Fast Business Finder - Optimized for Speed
==========================================

A streamlined tool that allows users to input distance, city, and industry
parameters and immediately receive an Excel document with business data.

Features:
- No AI verification (for maximum speed)
- Parallel processing of businesses
- Immediate Excel export
- Optimized API calls with caching
"""

import os
import sys
from typing import Optional
from business_finder import BusinessFinder, BusinessSearchParams
from category_helper import CategoryHelper
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_user_input() -> BusinessSearchParams:
    """
    Get user input for business search parameters.
    
    Returns:
        BusinessSearchParams object with user input
    """
    print("\n" + "="*60)
    print("🚀 FAST BUSINESS FINDER - OPTIMIZED FOR SPEED")
    print("="*60)
    
    # Get city
    while True:
        city = input("\n📍 Enter city (e.g., 'New York, NY' or 'Los Angeles, CA'): ").strip()
        if city:
            break
        print("❌ City is required. Please try again.")
    
    # Get industry
    print("\n🏢 Available industries (or enter your own):")
    category_helper = CategoryHelper()
    popular_categories = category_helper.get_popular_categories()
    
    # Show popular categories
    for i, category in enumerate(popular_categories[:10], 1):
        print(f"  {i:2d}. {category['title']}")
    
    while True:
        industry = input("\n🏢 Enter industry (e.g., 'restaurants', 'dentists', 'plumbers'): ").strip()
        if industry:
            # Validate category if it's in our list
            if category_helper.validate_category(industry):
                category_info = category_helper.get_category_by_alias(industry) or category_helper.get_category_by_title(industry)
                if category_info:
                    print(f"✅ Using category: {category_info['title']}")
            break
        print("❌ Industry is required. Please try again.")
    
    # Get distance
    while True:
        try:
            distance_input = input("\n📏 Enter search radius in miles (e.g., 5, 10, 25): ").strip()
            distance_miles = float(distance_input)
            if 0.1 <= distance_miles <= 100:
                break
            print("❌ Distance must be between 0.1 and 100 miles. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number for distance.")
    
    # Get number of results
    while True:
        try:
            max_results_input = input("\n📊 Enter maximum number of businesses to find (1-100, default 50): ").strip()
            if not max_results_input:
                max_results = 50
                break
            max_results = int(max_results_input)
            if 1 <= max_results <= 100:
                break
            print("❌ Number of businesses must be between 1 and 100. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    return BusinessSearchParams(
        city=city,
        industry=industry,
        distance_miles=distance_miles,
        max_results=max_results
    )


def main():
    """
    Main function to run the fast business finder.
    """
    try:
        # Check if API keys are available
        yelp_api_key = os.getenv('YELP_API_KEY')
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        if not yelp_api_key or not google_api_key:
            print("\n❌ ERROR: Missing API keys!")
            print("Please make sure you have:")
            print("  - YELP_API_KEY in your .env file")
            print("  - GOOGLE_API_KEY in your .env file")
            print("\nSee env_template.txt for setup instructions.")
            return
        
        # Get user input
        params = get_user_input()
        
        # Create business finder
        print(f"\n🔧 Initializing Business Finder...")
        finder = BusinessFinder(yelp_api_key=yelp_api_key, google_api_key=google_api_key)
        
        # Show search summary
        print(f"\n📋 Search Summary:")
        print(f"   City: {params.city}")
        print(f"   Industry: {params.industry}")
        print(f"   Radius: {params.distance_miles} miles")
        print(f"   Max Results: {params.max_results}")
        
        # Confirm with user
        confirm = input(f"\n🚀 Start search? (y/n, default y): ").strip().lower()
        if confirm in ['n', 'no']:
            print("❌ Search cancelled.")
            return
        
        print(f"\n🚀 Starting fast business search...")
        print("⏱️  This will be much faster than the previous version!")
        
        # Find and export businesses
        excel_file = finder.find_and_export_businesses(params)
        
        if excel_file:
            print(f"\n✅ SUCCESS! Excel file created: {excel_file}")
            print(f"📊 File contains business data with Yelp and Google cross-referencing")
            print(f"⚡ Processing completed with optimized speed")
            
            # Show performance stats
            stats = finder.get_api_usage_stats()
            print(f"\n📈 Performance Statistics:")
            print(f"   Google API calls: {stats['google_api_calls']}")
            print(f"   Cache hits: {stats['google_cache_hits']}")
            print(f"   Cache efficiency: {stats['google_cache_hits']/(stats['google_api_calls']+stats['google_cache_hits'])*100:.1f}%")
            
            # Ask if user wants to open the file
            open_file = input(f"\n📂 Open Excel file? (y/n, default y): ").strip().lower()
            if open_file not in ['n', 'no']:
                try:
                    os.system(f"open '{excel_file}'")  # macOS
                except:
                    try:
                        os.system(f"start '{excel_file}'")  # Windows
                    except:
                        print(f"Please open the file manually: {excel_file}")
        else:
            print("\n❌ No businesses found or error occurred.")
            print("Please check your search parameters and try again.")
    
    except KeyboardInterrupt:
        print("\n\n❌ Search interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Error in main: {e}", exc_info=True)


if __name__ == "__main__":
    main()
