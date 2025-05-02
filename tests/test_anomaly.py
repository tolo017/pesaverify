import pytest
import pandas as pd
import numpy as np
from app.ai.anomaly import AnomalyDetector

@pytest.fixture
def detector():
    return AnomalyDetector()

@pytest.fixture
def training_data():
    return pd.DataFrame({
        'account_number': ['123456', '234567', '345678'],
        'amount': [100.0, 150.0, 200.0]
    })

def test_anomaly_detection(detector, training_data):
    # Train the model
    detector.train(training_data)
    
    # Test normal transaction
    normal_tx = {'account_number': '234567', 'amount': 160.0}
    assert not detector.detect(normal_tx)
    
    # Test anomalous transaction
    anomaly_tx = {'account_number': '999999', 'amount': 10000.0}
    assert detector.detect(anomaly_tx)