from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.01, random_state=42)
    
    def train(self, historical_data: pd.DataFrame):
        """Train model on historical transaction data"""
        features = self._extract_features(historical_data)
        self.model.fit(features)
    
    def detect(self, transaction: Dict[str, Any]) -> bool:
        """Returns True if anomaly detected"""
        features = self._extract_features(pd.DataFrame([transaction]))
        return self.model.predict(features)[0] == -1
    
    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Feature engineering for fraud detection"""
        return np.array([
            np.log1p(df["amount"]),
            df["account_number"].astype(str).str.len()
        ]).T