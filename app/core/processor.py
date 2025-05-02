import pandas as pd
from typing import List, Dict
from .validator import AccountValidator

class BulkProcessor:
    def __init__(self, max_workers: int = 10):
        self.validator = AccountValidator(max_workers)
    
    def process_file(self, file_path: str, bank_api_url: str) -> Dict:
        """Process bulk account file"""
        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_json(file_path)
        accounts = df.to_dict('records')
        results = self.validator.validate_bulk(accounts, bank_api_url)
        
        valid = [r for r in results if r['valid']]
        invalid = [r for r in results if not r['valid']]
        
        return {
            "valid_accounts": valid,
            "invalid_accounts": invalid,
            "summary_stats": {
                "total": len(results),
                "valid_count": len(valid),
                "invalid_count": len(invalid)
            }
        }