import pandas as pd
from typing import List, Dict
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_validation_report(valid_accounts: List[Dict], invalid_accounts: List[Dict]) -> str:
        """Generate a comprehensive validation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_report_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename) as writer:
            pd.DataFrame(valid_accounts).to_excel(writer, sheet_name="Valid Accounts", index=False)
            pd.DataFrame(invalid_accounts).to_excel(writer, sheet_name="Invalid Accounts", index=False)
        
        return filename

    @staticmethod
    def generate_summary_stats(results: List[Dict]) -> Dict:
        """Generate summary statistics"""
        stats = {
            "total": len(results),
            "valid": sum(1 for r in results if r.get("valid", False)),
            "invalid": sum(1 for r in results if not r.get("valid", True)),
            "anomalies": sum(1 for r in results if r.get("anomaly", False))
        }
        stats["valid_pct"] = f"{(stats['valid']/stats['total'])*100:.2f}%"
        return stats