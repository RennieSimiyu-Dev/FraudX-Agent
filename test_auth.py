"""
Quick test script to verify authentication setup and create a working demo account.
"""
import sys
import os

# Add Backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

from auth import get_password_hash, verify_password, register_analyst, authenticate_analyst

# Test password hashing
print("Testing password hashing...")
test_password = "demo123"
hashed = get_password_hash(test_password)
print(f"Password: {test_password}")
print(f"Hashed: {hashed}")
print(f"Verification: {verify_password(test_password, hashed)}")

print("\n" + "="*50)
print("Creating/Updating demo_analyst account...")
print("="*50)

try:
    # Try to register demo_analyst (will fail if exists)
    analyst = register_analyst(
        analyst_id="demo_analyst",
        password="demo123",
        full_name="Demo Analyst",
        email="demo@fraudx.local",
        review_desk="Fraud Operations"
    )
    print("✅ Demo account created successfully!")
    print(f"Analyst ID: {analyst['analyst_id']}")
    print(f"Full Name: {analyst['full_name']}")
except Exception as e:
    print(f"ℹ️  Demo account already exists or error: {e}")

print("\n" + "="*50)
print("Testing authentication...")
print("="*50)

# Test authentication
result = authenticate_analyst("demo_analyst", "demo123")
if result:
    print("✅ Authentication successful!")
    print(f"Analyst: {result['full_name']}")
    print(f"Email: {result['email']}")
    print(f"Desk: {result['review_desk']}")
else:
    print("❌ Authentication failed!")

print("\n" + "="*50)
print("Demo Account Credentials:")
print("="*50)
print("Analyst ID: demo_analyst")
print("Password: demo123")
print("="*50)

# Made with Bob
