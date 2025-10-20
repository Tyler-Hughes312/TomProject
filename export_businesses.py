#!/usr/bin/env python3
"""
Simple Business Export Script
Export business data to Excel with customizable parameters.
"""

from business_finder import BusinessFinder, BusinessSearchParams
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_businesses_to_excel(city: str, industry: str, distance_miles: float, max_results: int, 
                              custom_filename: str = None):
    """
    Export businesses to Excel with specified parameters.
    
    Args:
        city: City to search in
        industry: Industry/category to search for
        distance_miles: Search radius in miles
        max_results: Maximum number of results
        custom_filename: Optional custom filename for the Excel file
    """
    
    try:
        # Initialize the business finder
        print(f"🚀 Initializing Business Finder...")
        finder = BusinessFinder.from_env()
        print("✅ Business Finder initialized successfully!")
        
        # Create search parameters
        params = BusinessSearchParams(
            city=city,
            industry=industry,
            distance_miles=distance_miles,
            max_results=max_results
        )
        
        # Display search parameters
        print(f"\n🔍 Search Parameters:")
        print(f"   📍 City: {params.city}")
        print(f"   🏢 Industry: {params.industry}")
        print(f"   📏 Radius: {params.distance_miles} miles")
        print(f"   📊 Max Results: {params.max_results}")
        
        # Search for businesses
        print(f"\n🔍 Searching for businesses...")
        businesses = finder.get_businesses_sync(params)
        
        if not businesses:
            print("❌ No businesses found matching your criteria.")
            return
        
        # Export to Excel
        print(f"\n📊 Found {len(businesses)} businesses. Exporting to Excel...")
        excel_file = finder.export_to_excel(businesses, params, custom_filename)
        
        # Show results
        print(f"\n✅ Excel file created successfully!")
        print(f"📁 File: {excel_file}")
        print(f"📊 Businesses exported: {len(businesses)}")
        
        # Show API usage
        stats = finder.get_api_usage_stats()
        print(f"🔌 API Usage: {stats['google_api_calls']} Google calls, {stats['google_cache_hits']} cache hits")
        
        # Show summary
        high_confidence = sum(1 for b in businesses if b.verification_metadata.get('confidence_level') == 'high')
        medium_confidence = sum(1 for b in businesses if b.verification_metadata.get('confidence_level') == 'medium')
        
        print(f"\n📈 Summary:")
        print(f"   • High confidence: {high_confidence}")
        print(f"   • Medium confidence: {medium_confidence}")
        print(f"   • Low confidence: {len(businesses) - high_confidence - medium_confidence}")
        
        print(f"\n🎉 Export complete! Open {excel_file} to view your data.")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please check your .env file and API keys.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        logger.exception("Error occurred during export")


def main():
    """Main function with example usage."""
    
    print("="*60)
    print("BUSINESS DATA EXPORT TOOL")
    print("="*60)
    
    # Example usage - you can modify these parameters
    print("\n📋 Example: Exporting restaurants in San Francisco")
    
    # You can modify these parameters as needed
    city = "San Francisco"
    industry = "restaurants"  # Try: "coffee", "pizza", "dentists", "auto", etc.
    distance_miles = 3.0      # Search radius in miles
    max_results = 15          # Maximum number of businesses to find
    
    # Optional: Custom filename (leave as None for auto-generated name)
    custom_filename = None    # e.g., "my_restaurants.xlsx"
    
    # Export the data
    export_businesses_to_excel(
        city=city,
        industry=industry,
        distance_miles=distance_miles,
        max_results=max_results,
        custom_filename=custom_filename
    )
    
    print("\n" + "="*60)
    print("CUSTOMIZATION TIPS")
    print("="*60)
    print("To customize your search, modify the parameters in this script:")
    print("• city: Change to any city name")
    print("• industry: Use any Yelp category (restaurants, coffee, pizza, etc.)")
    print("• distance_miles: Adjust search radius")
    print("• max_results: Change number of businesses to find")
    print("• custom_filename: Set to create a specific filename")


if __name__ == "__main__":
    main()
