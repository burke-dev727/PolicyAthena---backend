# app/services/user_profile.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Updated: Modified to match actual database schema and UI JSON structure
# Purpose: Service to store user profile information in the user_profile table
#          Handles basic personal information, employment, and financial details

from app.db.session import SessionLocal
from app.db.models import UserProfile

def save_user_profile(profile_data: dict, user_id: str = None):
    """
    Create and store a new user profile in the database
    
    Args:
        profile_data (dict): User profile information from UI containing:
            - name: User's full name
            - age: User's age (as string)
            - email: User's email address
            - phone: User's phone number (not stored in DB but in JSON)
            - address: User's street address
            - location: User's city/state (will be split into city/state)
            - zipcode: User's zip code
            - is_employed: Whether user is employed
            - employer_name: Name of employer
            - is_employeroffers: Whether employer offers insurance
            - annual_income: Annual income amount
            - household_size: Number of people in household
        user_id (str, optional): UUID reference to auth.users table
            
    Returns:
        int: The BIGINT ID of the newly created user profile record
        
    Raises:
        Exception: If database operation fails
        
    Note:
        This service creates user profile records matching the actual database schema.
        Some UI fields (phone) are not stored in the database but are preserved
        in the profile_data for reference.
    """
    db = SessionLocal()
    try:
        # Parse location into city and state
        location = profile_data.get('location', '')
        city = ''
        state = ''
        
        if location:
            # Simple parsing - assume format is "City, State" or just "City"
            if ',' in location:
                parts = location.split(',')
                city = parts[0].strip()
                state = parts[1].strip() if len(parts) > 1 else ''
            else:
                city = location.strip()
        
        # Create UserProfile record with data from frontend
        # Mapping UI JSON fields to database columns
        user_profile = UserProfile(
            user_id=user_id if user_id else None,                # Optional user ID (can be None)
            name=profile_data.get('name', ''),                  # User's full name
            age=profile_data.get('age', ''),                    # User's age (as TEXT)
            email=profile_data.get('email', ''),                # User's email address
            street_address=profile_data.get('address', ''),      # User's street address
            city=city,                                          # Parsed city from location
            state=state,                                        # Parsed state from location
            zipcode=profile_data.get('zipcode', ''),            # User's zip code
            is_employed=profile_data.get('is_employed', False), # Employment status
            employer_name=profile_data.get('employer_name', ''), # Employer name
            is_employeroffers=profile_data.get('is_employeroffers', False), # Employer insurance offer
            annual_income=profile_data.get('annual_income', ''), # Annual income
            household_size=profile_data.get('household_size', '') # Household size
        )
        
        # Database Operations
        db.add(user_profile)        # Add profile record to session
        db.commit()                 # Commit transaction to database
        db.refresh(user_profile)    # Refresh to get generated BIGINT ID
        
        return user_profile.id      # Return the new profile BIGINT ID
        
    except Exception as e:
        db.rollback()               # Rollback transaction on error
        raise e                     # Re-raise the exception for error handling
    finally:
        db.close()                  # Always close database connection 