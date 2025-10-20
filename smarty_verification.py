"""
Smarty Streets Address Verification Service
"""

import os
import requests
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SmartyStreetsVerifier:
    """Address verification using Smarty Streets API"""
    
    def __init__(self, auth_id: str, auth_token: str):
        """
        Initialize Smarty Streets verifier
        
        Args:
            auth_id: Smarty Streets Auth ID
            auth_token: Smarty Streets Auth Token
        """
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.base_url = "https://us-street.api.smartystreets.com/verify"
    
    def verify_address(self, street: str, city: str, state: str, zip_code: str) -> Dict:
        """
        Verify a single address using Smarty Streets
        
        Args:
            street: Street address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            
        Returns:
            Dictionary with verification results
        """
        try:
            params = {
                'auth-id': self.auth_id,
                'auth-token': self.auth_token,
                'street': street,
                'city': city,
                'state': state,
                'zipcode': zip_code
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            
            if not results:
                return {
                    'verified': False,
                    'status': 'invalid',
                    'confidence': 0.0,
                    'verified_address': None,
                    'verified_city': None,
                    'verified_state': None,
                    'verified_zip_code': None,
                    'error': 'No results returned'
                }
            
            # Get the first result
            result = results[0]
            
            # Check if address was verified
            if result.get('analysis', {}).get('dpv_match_code') in ['Y', 'S', 'D']:
                # Address is deliverable
                return {
                    'verified': True,
                    'status': 'verified',
                    'confidence': self._calculate_confidence(result),
                    'verified_address': result.get('delivery_line_1', ''),
                    'verified_city': result.get('components', {}).get('city_name', ''),
                    'verified_state': result.get('components', {}).get('state_abbreviation', ''),
                    'verified_zip_code': result.get('components', {}).get('zipcode', ''),
                    'error': None
                }
            else:
                # Address is not deliverable
                return {
                    'verified': False,
                    'status': 'invalid',
                    'confidence': 0.0,
                    'verified_address': None,
                    'verified_city': None,
                    'verified_state': None,
                    'verified_zip_code': None,
                    'error': result.get('analysis', {}).get('dpv_footnotes', 'Address not deliverable')
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Smarty Streets API error: {e}")
            return {
                'verified': False,
                'status': 'error',
                'confidence': 0.0,
                'verified_address': None,
                'verified_city': None,
                'verified_state': None,
                'verified_zip_code': None,
                'error': f'API Error: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error in address verification: {e}")
            return {
                'verified': False,
                'status': 'error',
                'confidence': 0.0,
                'verified_address': None,
                'verified_city': None,
                'verified_state': None,
                'verified_zip_code': None,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _calculate_confidence(self, result: Dict) -> float:
        """
        Calculate confidence score based on verification result
        
        Args:
            result: Smarty Streets API result
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        analysis = result.get('analysis', {})
        dpv_match = analysis.get('dpv_match_code', 'N')
        
        # Base confidence on DPV match code
        confidence_map = {
            'Y': 1.0,  # Confirmed deliverable
            'S': 0.9,  # Confirmed deliverable (secondary address)
            'D': 0.8,  # Confirmed deliverable (business)
            'N': 0.0,  # Not deliverable
        }
        
        base_confidence = confidence_map.get(dpv_match, 0.0)
        
        # Adjust based on other factors
        if analysis.get('dpv_vacant', False):
            base_confidence *= 0.7  # Reduce confidence for vacant addresses
        
        if analysis.get('dpv_cmra', False):
            base_confidence *= 0.9  # Slight reduction for commercial mail receiving agency
        
        return min(max(base_confidence, 0.0), 1.0)
    
    def batch_verify_addresses(self, addresses: list) -> list:
        """
        Verify multiple addresses in batch
        
        Args:
            addresses: List of address dictionaries with keys: street, city, state, zip_code
            
        Returns:
            List of verification results
        """
        results = []
        for address in addresses:
            result = self.verify_address(
                address.get('street', ''),
                address.get('city', ''),
                address.get('state', ''),
                address.get('zip_code', '')
            )
            results.append(result)
        
        return results

def get_smarty_verifier() -> Optional[SmartyStreetsVerifier]:
    """
    Get Smarty Streets verifier instance if credentials are available
    
    Returns:
        SmartyStreetsVerifier instance or None if credentials not available
    """
    auth_id = os.getenv('SMARTY_STREETS_AUTH_ID')
    auth_token = os.getenv('SMARTY_STREETS_AUTH_TOKEN')
    
    if not auth_id or not auth_token:
        logger.warning("Smarty Streets credentials not found in environment")
        return None
    
    return SmartyStreetsVerifier(auth_id, auth_token)
