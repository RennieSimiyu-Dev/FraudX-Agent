"""
Standalone script to create a demo account with proper password hashing.
Uses bcrypt directly to avoid compatibility issues.
"""
import json
import os
import bcrypt
from datetime import datetime

# Path to analysts database
ANALYSTS_DB_PATH = os.path.join("data", "analysts.json")

def create_demo_account():
    """Create or update the demo analyst account."""
    
    # Create demo account data
    demo_password = "demo123"
    
    # Hash password using bcrypt directly
    password_bytes = demo_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    analyst_data = {
        "demo_analyst": {
            "analyst_id": "demo_analyst",
            "hashed_password": hashed_password,
            "full_name": "Demo Analyst",
            "email": "demo@fraudx.local",
            "review_desk": "Fraud Operations",
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
    }
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Load existing analysts if file exists
    if os.path.exists(ANALYSTS_DB_PATH):
        try:
            with open(ANALYSTS_DB_PATH, 'r') as f:
                existing_analysts = json.load(f)
            # Update with demo account
            existing_analysts.update(analyst_data)
            analyst_data = existing_analysts
        except:
            pass
    
    # Save to file
    with open(ANALYSTS_DB_PATH, 'w') as f:
        json.dump(analyst_data, f, indent=2)
    
    # Verify the password works
    stored_hash = analyst_data["demo_analyst"]["hashed_password"].encode('utf-8')
    verification = bcrypt.checkpw(password_bytes, stored_hash)
    
    print("="*60)
    print("✅ Demo Account Created Successfully!")
    print("="*60)
    print(f"Analyst ID: demo_analyst")
    print(f"Password: demo123")
    print(f"Full Name: Demo Analyst")
    print(f"Email: demo@fraudx.local")
    print(f"Review Desk: Fraud Operations")
    print("="*60)
    print(f"Password verification: {'✅ PASSED' if verification else '❌ FAILED'}")
    print(f"Account saved to: {ANALYSTS_DB_PATH}")
    print("\nYou can now:")
    print("1. Start the backend server: python Backend/main.py")
    print("2. Start the frontend: streamlit run Frontend/streamlit_app.py")
    print("3. Sign in with the credentials above")
    print("="*60)

if __name__ == "__main__":
    create_demo_account()

# Made with Bob
