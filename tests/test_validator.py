import pytest
from app.core.validator import AccountValidator
from unittest.mock import patch

@pytest.fixture
def validator():
    return AccountValidator()

def test_single_validation(validator):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "is_valid": True,
            "reason": "Valid"
        }
        
        result = validator.validate_single(
            {"account_number": "123456", "bank_code": "01", "amount": 100.0},
            "http://mock-api"
        )
        
        assert result['valid'] == True
        assert 'anomaly' in result

def test_invalid_account(validator):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "is_valid": False,
            "reason": "Invalid account"
        }
        
        result = validator.validate_single(
            {"account_number": "999999", "bank_code": "01", "amount": 100.0},
            "http://mock-api"
        )
        
        assert result['valid'] == False
        assert result['reason'] == "Invalid account"