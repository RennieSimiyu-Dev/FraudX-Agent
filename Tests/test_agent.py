"""
Comprehensive tests for the FraudX Agent system.
"""
import sys
import os
import pytest

# Add Backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Backend'))

from agent import fraud_agent
from decision import decide, get_risk_level
from verification import verify_user, is_valid_response
from analyst_queue import push_to_queue, get_queue, clear_queue, get_pending_count


class TestFraudAgent:
    """Tests for fraud detection agent."""
    
    def test_low_risk_transaction(self):
        """Test transaction with low fraud risk."""
        txn = {
            "amount": 50,
            "country": "KE",
            "device": "device_1",
            "merchant": "grocery"
        }
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"],
            "merchants": ["grocery", "fuel"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score < 30
        assert len(reasons) == 0
    
    def test_high_amount_risk(self):
        """Test transaction with unusually high amount."""
        txn = {
            "amount": 500,
            "country": "KE",
            "device": "device_1"
        }
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score >= 30
        assert any("high amount" in r.lower() for r in reasons)
    
    def test_new_country_risk(self):
        """Test transaction from new country."""
        txn = {
            "amount": 50,
            "country": "US",
            "device": "device_1"
        }
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score >= 25
        assert any("country" in r.lower() for r in reasons)
    
    def test_unknown_device_risk(self):
        """Test transaction from unknown device."""
        txn = {
            "amount": 50,
            "country": "KE",
            "device": "device_999"
        }
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score >= 20
        assert any("device" in r.lower() for r in reasons)
    
    def test_multiple_risk_factors(self):
        """Test transaction with multiple risk factors."""
        txn = {
            "amount": 500,
            "country": "US",
            "device": "device_999",
            "merchant": "unknown_merchant"
        }
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"],
            "merchants": ["grocery"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score >= 70
        assert len(reasons) >= 3
    
    def test_missing_transaction_field(self):
        """Test error handling for missing transaction field."""
        txn = {"amount": 50, "country": "KE"}  # Missing device
        profile = {
            "avg_amount": 40,
            "countries": ["KE"],
            "devices": ["device_1"]
        }
        
        with pytest.raises(ValueError, match="Missing required transaction field"):
            fraud_agent(txn, profile)
    
    def test_missing_profile_field(self):
        """Test error handling for missing profile field."""
        txn = {
            "amount": 50,
            "country": "KE",
            "device": "device_1"
        }
        profile = {"avg_amount": 40, "countries": ["KE"]}  # Missing devices
        
        with pytest.raises(ValueError, match="Missing required profile field"):
            fraud_agent(txn, profile)
    
    def test_score_capped_at_100(self):
        """Test that score is capped at 100."""
        txn = {
            "amount": 10000,
            "country": "XX",
            "device": "device_999",
            "merchant": "unknown"
        }
        profile = {
            "avg_amount": 10,
            "countries": ["KE"],
            "devices": ["device_1"],
            "merchants": ["grocery"]
        }
        
        score, reasons = fraud_agent(txn, profile)
        assert score <= 100


class TestDecision:
    """Tests for decision module."""
    
    def test_approve_decision(self):
        """Test approval for low risk scores."""
        assert decide(0) == "APPROVE"
        assert decide(15) == "APPROVE"
        assert decide(29) == "APPROVE"
    
    def test_verify_user_decision(self):
        """Test user verification for medium risk scores."""
        assert decide(30) == "VERIFY_USER"
        assert decide(50) == "VERIFY_USER"
        assert decide(69) == "VERIFY_USER"
    
    def test_analyst_queue_decision(self):
        """Test analyst queue for high risk scores."""
        assert decide(70) == "ANALYST_QUEUE"
        assert decide(85) == "ANALYST_QUEUE"
        assert decide(100) == "ANALYST_QUEUE"
    
    def test_invalid_score_type(self):
        """Test error handling for invalid score type."""
        with pytest.raises(ValueError, match="Score must be a number"):
            decide("invalid")
    
    def test_score_out_of_range(self):
        """Test error handling for out of range scores."""
        with pytest.raises(ValueError, match="Score must be between 0 and 100"):
            decide(-1)
        with pytest.raises(ValueError, match="Score must be between 0 and 100"):
            decide(101)
    
    def test_get_risk_level(self):
        """Test risk level descriptions."""
        assert get_risk_level(10) == "Low"
        assert get_risk_level(50) == "Medium"
        assert get_risk_level(90) == "High"


class TestVerification:
    """Tests for verification module."""
    
    def test_positive_responses(self):
        """Test various positive user responses."""
        positive = ["yes", "y", "YES", "approve", "confirm", "ok", "  yes  "]
        for response in positive:
            assert verify_user(response) == "APPROVED_BY_USER"
    
    def test_negative_responses(self):
        """Test various negative user responses."""
        negative = ["no", "n", "NO", "deny", "block", "reject", "  no  "]
        for response in negative:
            assert verify_user(response) == "BLOCKED"
    
    def test_invalid_responses(self):
        """Test invalid user responses."""
        invalid = ["maybe", "unknown", "123", ""]
        for response in invalid:
            assert verify_user(response) == "INVALID_RESPONSE"
    
    def test_non_string_response(self):
        """Test non-string response handling."""
        assert verify_user(123) == "INVALID_RESPONSE"
        assert verify_user(None) == "INVALID_RESPONSE"
    
    def test_is_valid_response(self):
        """Test response validation."""
        assert is_valid_response("yes") is True
        assert is_valid_response("no") is True
        assert is_valid_response("maybe") is False


class TestAnalystQueue:
    """Tests for analyst queue module."""
    
    def setup_method(self):
        """Clear queue before each test."""
        clear_queue()
    
    def test_push_to_queue(self):
        """Test adding transaction to queue."""
        txn = {"amount": 500, "country": "US", "device": "device_999"}
        score = 85
        reasons = ["High amount", "New country"]
        
        push_to_queue(txn, score, reasons)
        queue = get_queue()
        
        assert len(queue) == 1
        assert queue[0]["transaction"] == txn
        assert queue[0]["score"] == score
        assert queue[0]["reasons"] == reasons
        assert "timestamp" in queue[0]
        assert queue[0]["status"] == "pending"
    
    def test_get_queue(self):
        """Test retrieving queue."""
        txn1 = {"amount": 500, "country": "US", "device": "device_1"}
        txn2 = {"amount": 600, "country": "GB", "device": "device_2"}
        
        push_to_queue(txn1, 80, ["Reason 1"])
        push_to_queue(txn2, 90, ["Reason 2"])
        
        queue = get_queue()
        assert len(queue) == 2
    
    def test_get_pending_count(self):
        """Test counting pending transactions."""
        push_to_queue({"amount": 500}, 80, ["Reason"])
        push_to_queue({"amount": 600}, 90, ["Reason"])
        
        assert get_pending_count() == 2
    
    def test_clear_queue(self):
        """Test clearing the queue."""
        push_to_queue({"amount": 500}, 80, ["Reason"])
        clear_queue()
        
        assert len(get_queue()) == 0
        assert get_pending_count() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
