# app/services/user_profile.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: Service to store user profile information in the user_profiles table
#          Handles basic personal information like name, contact details, and address

from app.db.session import SessionLocal
from app.db.models import UserProfile

def save_user_profile(profile_data: dict):
    """
    Create and store a new user profile in the database
    
    Args:
        profile_data (dict): User profile information containing:
            - first_name: User's first name
            - last_name: User's last name
            - age: User's age
            - email: User's email address
            - phone: User's phone number
            - address: User's street address
            - city: User's city
            - state: User's state
            - zip_code: User's zip code
            
    Returns:
        str: The UUID of the newly created user profile record
        
    Raises:
        Exception: If database operation fails
        
    Note:
        This service creates basic user profile records that can be linked
        to other user data like insurance preferences, employment info, etc.
    """
    db = SessionLocal()
    try:
        # Create UserProfile record with data from frontend
        # All fields are optional with empty string defaults for text fields
        user_profile = UserProfile(
            first_name=profile_data.get('first_name', ''),      # User's first name
            last_name=profile_data.get('last_name', ''),        # User's last name
            age=profile_data.get('age'),                        # User's age (can be None)
            email=profile_data.get('email', ''),                # User's email address
            phone=profile_data.get('phone', ''),                # User's phone number
            address=profile_data.get('address', ''),            # User's address (street name, address number)
            location=profile_data.get('location', ''),          # User's location (city, state)
            zip_code=profile_data.get('zip_code', ''),          # User's zipcode
            ssn=profile_data.get('ssn', ''),                    # User's social security number
            is_employed=profile_data.get('is_employed', ''),    # User's employment status
            employer_name=profile_data.get('employer_name', ''), # User's employer's name
            is_employeroffers=profile_data.get('is_employeroffers', ''), # User's employers offers yes/no
            annual_income=profile_data.get('annual_income', ''), # User's annual income
            household_size=profile_data.get('annual_income', '') # User's household size
        )
        
        # Database Operations
        db.add(user_profile)        # Add profile record to session
        db.commit()                 # Commit transaction to database
        db.refresh(user_profile)    # Refresh to get generated UUID
        
        return user_profile.id      # Return the new profile UUID
        
    except Exception as e:
        db.rollback()               # Rollback transaction on error
        raise e                     # Re-raise the exception for error handling
    finally:
        db.close()                  # Always close database connection 
