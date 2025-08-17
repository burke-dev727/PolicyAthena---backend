#!/usr/bin/env python3
"""
Test script to verify data flow from frontend to backend
This script simulates the data that would be sent from the frontend
"""

import requests
import json
import time

# Backend URL
BACKEND_URL = "http://localhost:8000/userInput/profile"

def test_userprofile_data():
    """Test UserProfile data submission"""
    print("Testing UserProfile data submission...")
    
    userprofile_data = {
        "name": "John Doe",
        "age": "30",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "address": "123 Main St",
        "location": "New York, NY",
        "zipcode": "10001",
        "ssn": "123-45-6789",
        "is_employed": True,
        "employer_name": "Tech Corp",
        "is_employeroffers": True,
        "annual_income": "75000",
        "household_size": "2",
        "source": "userprofile"
    }
    
    try:
        response = requests.post(BACKEND_URL, json=userprofile_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_userinput_data():
    """Test UserInput data submission"""
    print("\nTesting UserInput data submission...")
    
    userinput_data = {
        "have_insurance": True,
        "insurance_provider": "Blue Cross Blue Shield, Aetna",
        "policy_number": "POL123456",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "coverage_type": "Individual",
        "providers": "Kaiser Permanente, Cigna",
        "current_conditions": "Hypertension, Diabetes",
        "current_prescriptions": "Lisinopril, Metformin",
        "coverage_level": "Gold",
        "monthly_budget": "300-500",
        "is_US_Citizen": True,
        "is_Mediaid": False,
        "is_Medicare": False,
        "events": "surgery, 2023-12-01",
        "is_Veteran": False,
        "is_StudentEligible": False,
        "user_insurance_docs": "insurance_card.pdf",
        "proof_of_income_docs": "paystub.pdf",
        "source": "userinput"
    }
    
    try:
        response = requests.post(BACKEND_URL, json=userinput_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting data flow tests...")
    print("=" * 50)
    
    # Test UserProfile
    userprofile_success = test_userprofile_data()
    
    # Wait a bit between requests
    time.sleep(1)
    
    # Test UserInput
    userinput_success = test_userinput_data()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"UserProfile: {'PASS' if userprofile_success else 'FAIL'}")
    print(f"UserInput: {'PASS' if userinput_success else 'FAIL'}")
    
    if userprofile_success and userinput_success:
        print("\n✅ All tests passed! Data flow is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the backend logs for details.")

if __name__ == "__main__":
    main()

