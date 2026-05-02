"""
Analyst queue module for managing transactions requiring manual review.
"""
from typing import Dict, List, Any
from datetime import datetime
from threading import Lock


# Thread-safe queue for analyst review
_queue: List[Dict[str, Any]] = []
_queue_lock = Lock()


def push_to_queue(txn: Dict[str, Any], score: int, reasons: List[str]) -> None:
    """
    Add a transaction to the analyst review queue.
    
    Args:
        txn: Transaction data
        score: Fraud risk score
        reasons: List of risk factors
    """
    with _queue_lock:
        queue_item = {
            "transaction": txn,
            "score": score,
            "reasons": reasons,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        _queue.append(queue_item)


def get_queue() -> List[Dict[str, Any]]:
    """
    Get all transactions in the analyst review queue.
    
    Returns:
        List of transactions awaiting review
    """
    with _queue_lock:
        return _queue.copy()


def get_pending_count() -> int:
    """
    Get count of pending transactions in queue.
    
    Returns:
        Number of pending transactions
    """
    with _queue_lock:
        return sum(1 for item in _queue if item.get("status") == "pending")


def clear_queue() -> None:
    """Clear all transactions from the queue."""
    with _queue_lock:
        _queue.clear()


def update_status(index: int, status: str) -> bool:
    """
    Update the status of a transaction in the queue.
    
    Args:
        index: Index of the transaction in the queue
        status: New status (e.g., "reviewed", "approved", "rejected")
    
    Returns:
        True if update was successful, False otherwise
    """
    with _queue_lock:
        if 0 <= index < len(_queue):
            _queue[index]["status"] = status
            _queue[index]["reviewed_at"] = datetime.utcnow().isoformat()
            return True
        return False

# Made with Bob
