# app/routers/input_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for handling user input data and user profile creation
#          Provides REST API interface for frontend to submit user information

from fastapi import APIRouter
from app.agents.input_interpreter import InputInterpreterAgent
from app.services.user_input import user_input
from app.services.user_profile import save_user_profile
router = APIRouter(prefix="/userInput", tags=["userInput"])

@router.post("/userInput")
async def process_user_profile(data: dict):
    """
    Process and store user input data (insurance preferences, conditions, etc.)
    
    Endpoint: POST /userInput/userInput
    
    This endpoint accepts the flat JSON structure from userinput_answers_data.json
    and stores it directly in the user_input table. The data includes:
    - Insurance preferences and current coverage
    - Health conditions and prescriptions
    - Eligibility information
    - Coverage preferences and budget
    
    Args:
        data (dict): Raw JSON data from frontend containing user input
        
    Returns:
        dict: Response with status message, profile ID, and parsed data
        
    Example Request Body:
        {
            "have_insurance": false,
            "insurance_provider": "Blue Shield",
            "coverage_type": "Individual",
            "current_conditions": "diabetes, infection, cancer",
            ...
        }
    """
    try:
        interpreter = InputInterpreterAgent()
        parsed_profile = interpreter.run(data)
        profile_id = user_input(parsed_profile)
        return {
            "message": "Profile received and stored.",
            "profile_id": profile_id,
            "parsed_profile": parsed_profile
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}

@router.post("/userProfile")
async def create_user_profile(profile_data: dict):
    """
    Create a new user profile with basic personal information
    
    Endpoint: POST /userInput/userProfile
    
    This endpoint creates basic user profile records containing:
    - Personal identification (name, age)
    - Contact information (email, phone)
    - Address details (street, city, state, zip)
    
    Args:
        profile_data (dict): User profile information from frontend
        
    Returns:
        dict: Response with status message, profile ID, and submitted data
        
    Example Request Body:
        {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "email": "john.doe@example.com",
            "phone": "555-123-4567",
            "address": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip_code": "12345"
        }
    """
    try:
        profile_id = save_user_profile(profile_data)
        
        # Return success response with the new profile ID
        return {
            "message": "User profile created successfully.",
            "profile_id": profile_id,
            "profile_data": profile_data
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}
