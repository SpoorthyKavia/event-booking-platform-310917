"""
Mock payment handler for bookings (stub).
"""

from uuid import uuid4

def process_mock_payment(user_id: int, amount: float):
    """
    Simulate payment gateway. Always returns success transaction.
    """
    # In production, integrate a payment processor
    return {
        "status": "success",
        "payment_reference": f"MOCK-{str(uuid4())[:8]}"
    }
