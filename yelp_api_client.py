"""
Yelp API Client for Lead Generator
Handles Yelp Fusion API interactions
"""

import requests
import os
import time
from typing import List, Dict, Optional
from config import YELP_API_KEY, DEFAULT_LIMIT, MAX_RESULTS, BUSINESS_CATEGORIES

class YelpAPIClient:
    def __init__(self):
        self.api_key = YELP_API_KEY
        self.base_url = "https://api.yelp.com/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
        self.rate_limit_delay = 0.1  # 100ms between requests
    
    def search_businesses(self, location: str, business_type: str = None, 
                         radius: int = 25000, max_results: int = 100) -> List[Dict]:
        """Search for businesses using Yelp Fusion API"""
        if not self.api_key:
            raise ValueError("Yelp API key is required")
        
        businesses = []
        offset = 0
        limit = min(DEFAULT_LIMIT, max_results)
        
        while len(businesses) < max_results:
            # Calculate how many results to fetch
            remaining = max_results - len(businesses)
            current_limit = min(limit, remaining)
            
            try:
                # Make API request
                response = self._make_search_request(
                    location, business_type, radius, current_limit, offset
                )
                
                if not response:
                    break
                
                # Process results
                for business in response.get('businesses', []):
                    if len(businesses) >= max_results:
                        break
                    
                    processed_business = self._process_business(business)
                    businesses.append(processed_business)
                
                # Check if we have more results
                if len(response.get('businesses', [])) < current_limit:
                    break
                
                offset += current_limit
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"Error fetching businesses: {e}")
                break
        
        return businesses[:max_results]
    
    def _make_search_request(self, location: str, business_type: str = None, 
                           radius: int = 25000, limit: int = 50, offset: int = 0) -> Dict:
        """Make a search request to Yelp API"""
        url = f"{self.base_url}/businesses/search"
        
        params = {
            'location': location,
            'radius': radius,
            'limit': limit,
            'offset': offset,
            'sort_by': 'best_match'
        }
        
        if business_type:
            params['categories'] = business_type
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def _process_business(self, business: Dict) -> Dict:
        """Process a business from Yelp API response"""
        location = business.get('location', {})
        coordinates = business.get('coordinates', {})
        
        return {
            'yelp_id': business.get('id'),
            'name': business.get('name'),
            'address': self._format_address(location),
            'city': location.get('city'),
            'state': location.get('state'),
            'zip_code': location.get('zip_code'),
            'phone': business.get('phone'),
            'website': business.get('url'),
            'business_type': self._get_primary_category(business.get('categories', [])),
            'rating': business.get('rating'),
            'review_count': business.get('review_count'),
            'price_level': business.get('price'),
            'yelp_url': business.get('url'),
            'latitude': coordinates.get('latitude'),
            'longitude': coordinates.get('longitude'),
            'image_url': business.get('image_url'),
            'is_closed': business.get('is_closed', False)
        }
    
    def _format_address(self, location: Dict) -> str:
        """Format address from location data"""
        address_parts = []
        
        for field in ['address1', 'address2', 'address3']:
            if location.get(field):
                address_parts.append(location[field])
        
        return ', '.join(address_parts)
    
    def _get_primary_category(self, categories: List[Dict]) -> str:
        """Get primary business category"""
        if not categories:
            return 'other'
        
        # Return the first category's alias
        return categories[0].get('alias', 'other')
    
    def get_business_details(self, business_id: str) -> Optional[Dict]:
        """Get detailed business information"""
        if not self.api_key:
            raise ValueError("Yelp API key is required")
        
        url = f"{self.base_url}/businesses/{business_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            business = response.json()
            return self._process_business(business)
        except requests.exceptions.RequestException as e:
            print(f"Failed to get business details: {e}")
            return None
    
    def search_businesses_by_coordinates(self, latitude: float, longitude: float, 
                                       business_type: str = None, radius: int = 25000, 
                                       max_results: int = 100) -> List[Dict]:
        """Search for businesses by coordinates"""
        if not self.api_key:
            raise ValueError("Yelp API key is required")
        
        businesses = []
        offset = 0
        limit = min(DEFAULT_LIMIT, max_results)
        
        while len(businesses) < max_results:
            remaining = max_results - len(businesses)
            current_limit = min(limit, remaining)
            
            try:
                url = f"{self.base_url}/businesses/search"
                params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'radius': radius,
                    'limit': current_limit,
                    'offset': offset,
                    'sort_by': 'best_match'
                }
                
                if business_type:
                    params['categories'] = business_type
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for business in data.get('businesses', []):
                    if len(businesses) >= max_results:
                        break
                    
                    processed_business = self._process_business(business)
                    businesses.append(processed_business)
                
                if len(data.get('businesses', [])) < current_limit:
                    break
                
                offset += current_limit
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"Error searching by coordinates: {e}")
                break
        
        return businesses[:max_results]
