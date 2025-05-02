from typing import Dict, Any, List
import requests
from concurrent.futures import ThreadPoolExecutor

class AccountValidator:
    def __init__(self, max_workers: int = 6):
        self.max_workers = max_workers
        self.session = requests.Session()  # Reuse HTTP connection
        self.session.headers.update({'Content-Type': 'application/json'})

    def validate_single(self, account_data: Dict[str, Any], api_url: str) -> Dict[str, Any]:
        """Validate a single account with complete error handling"""
        try:
            # Ensure required fields exist
            if not all(k in account_data for k in ['account_number', 'bank_code']):
                return {
                    'valid': False,
                    'reason': 'Missing required fields',
                    'anomaly': False
                }

            # Make API request
            response = self.session.post(
                api_url,
                json={
                    'account_number': str(account_data['account_number']),
                    'bank_code': str(account_data['bank_code']),
                    'amount': float(account_data.get('amount', 0))
                },
                timeout=5
            )

            # Process response
            response.raise_for_status()
            result = response.json()

            # Ensure response contains required fields
            return {
                'valid': bool(result.get('is_valid', False)),
                'reason': str(result.get('reason', 'Valid' if result.get('is_valid') else 'Invalid')),
                'anomaly': bool(result.get('anomaly', False))
            }

        except requests.exceptions.RequestException as e:
            return {
                'valid': False,
                'reason': f"API Error: {str(e)}",
                'anomaly': False
            }
        except Exception as e:
            return {
                'valid': False,
                'reason': f"Validation Error: {str(e)}",
                'anomaly': False
            }

    def validate_bulk(self, accounts: List[Dict[str, Any]], api_url: str) -> List[Dict[str, Any]]:
        """Process bulk validation with guaranteed response structure"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(
                lambda acc: self.validate_single(acc, api_url),
                accounts
            ))