#!/usr/bin/env python3
"""
Test script to verify the enhanced frontend notification system
This script simulates frontend submissions and shows what notifications users will see
"""

import requests
import json
import time

# Backend URL
BACKEND_URL = "http://localhost:8000/userInput/profile"

def test_userprofile_notification():
    """Test UserProfile submission and show expected frontend notification"""
    print("Testing UserProfile Notification System")
    print("=" * 60)
    
    userprofile_data = {
        "name": "Jane Smith",
        "age": "28",
        "email": "jane.smith@example.com",
        "phone": "555-987-6543",
        "address": "456 Oak Avenue",
        "location": "Los Angeles, CA",
        "zipcode": "90210",
        "ssn": "987-65-4321",
        "is_employed": True,
        "employer_name": "Tech Solutions Inc",
        "is_employeroffers": True,
        "annual_income": "85000",
        "household_size": "1",
        "source": "userprofile"
    }
    
    print("Submitting UserProfile data...")
    print(f"Data: {json.dumps(userprofile_data, indent=2)}")
    print()
    
    try:
        response = requests.post(BACKEND_URL, json=userprofile_data)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS! Frontend will show this notification:")
            print()
            
            if result.get("success"):
                success_message = f"""DATA SUBMITTED SUCCESSFULLY!

Backend Storage Status:
Database: Saved (ID: {result.get('db_id', 'N/A')})
File Storage: {'Saved' if result.get('file_saved') else 'Failed'}
Filename: {result.get('filename', 'N/A')}
Source: {result.get('source', 'N/A')}

Your profile data has been successfully stored in the backend database and file system."""
                
                print(success_message)
                print()
                print("Backend Response Details:")
                print(f"Database ID: {result.get('db_id')}")
                print(f"File Saved: {result.get('file_saved')}")
                print(f"Filename: {result.get('filename')}")
                print(f"Filepath: {result.get('filepath')}")
                print(f"Source: {result.get('source')}")
                
            else:
                print("ERROR! Frontend will show this notification:")
                print(f"SUBMISSION FAILED!\n\nError: {result.get('error', 'Unknown error')}")
                
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("NETWORK ERROR! Frontend will show this notification:")
        print("""NETWORK ERROR!

Unable to connect to the backend server.

Please ensure:
• Backend server is running on http://localhost:8000
• No firewall is blocking the connection
• Backend is accessible from your browser""")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print("\n" + "=" * 60)

def test_userinput_notification():
    """Test UserInput submission and show expected frontend notification"""
    print("Testing UserInput Notification System")
    print("=" * 60)
    
    userinput_data = {
        "have_insurance": True,
        "insurance_provider": "Blue Cross Blue Shield, Aetna",
        "policy_number": "POL789012",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "coverage_type": "Family",
        "providers": "Kaiser Permanente, United Healthcare",
        "current_conditions": "Asthma, Hypertension",
        "current_prescriptions": "Albuterol, Amlodipine",
        "coverage_level": "Silver",
        "monthly_budget": "$300-$500",
        "is_US_Citizen": True,
        "is_Mediaid": False,
        "is_Medicare": False,
        "events": "accident, 2024-06-15",
        "is_Veteran": False,
        "is_StudentEligible": False,
        "user_insurance_docs": "family_insurance_card.pdf",
        "proof_of_income_docs": "family_paystub.pdf",
        "source": "userinput"
    }
    
    print("Submitting UserInput data...")
    print(f"Data: {json.dumps(userinput_data, indent=2)}")
    print()
    
    try:
        response = requests.post(BACKEND_URL, json=userinput_data)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS! Frontend will show this notification:")
            print()
            
            if result.get("success"):
                success_message = f"""DATA SUBMITTED SUCCESSFULLY!

Backend Storage Status:
Database: Saved (ID: {result.get('db_id', 'N/A')})
File Storage: {'Saved' if result.get('file_saved') else 'Failed'}
Filename: {result.get('filename', 'N/A')}
Source: {result.get('source', 'N/A')}

🎯 Your data has been successfully stored in the backend database and file system."""
                
                print(success_message)
                print()
                print("Backend Response Details:")
                print(f"Database ID: {result.get('db_id')}")
                print(f"File Saved: {result.get('file_saved')}")
                print(f"Filename: {result.get('filename')}")
                print(f"Filepath: {result.get('filepath')}")
                print(f"Source: {result.get('source')}")
                
            else:
                print("ERROR! Frontend will show this notification:")
                print(f"SUBMISSION FAILED!\n\nError: {result.get('error', 'Unknown error')}")
                
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("NETWORK ERROR! Frontend will show this notification:")
        print("""NETWORK ERROR!

Unable to connect to the backend server.

Please ensure:
• Backend server is running on http://localhost:8000
• No firewall is blocking the connection
• Backend is accessible from your browser""")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print("\n" + "=" * 60)

def main():
    """Run all notification tests"""
    print("Frontend Notification System Test")
    print("This script shows what notifications users will see in the frontend")
    print()
    
    # Test UserProfile notifications
    test_userprofile_notification()
    
    # Wait between tests
    time.sleep(2)
    
    # Test UserInput notifications
    test_userinput_notification()
    
    print("\nTest Summary:")
    print("• Run this script to see expected frontend notifications")
    print("• Check backend logs for detailed operation information")
    print("• Use the frontend forms to test the actual notification system")
    print("• Verify data is stored in both database and file system")

if __name__ == "__main__":
    main()
