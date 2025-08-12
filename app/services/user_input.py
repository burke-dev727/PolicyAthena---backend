# app/services/user_input.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: Service to store user input data directly in the user_input table
#          Handles data transformation from JSON format to database schema

from app.db.session import SessionLocal
from app.db.models import UserInput
from datetime import datetime

def user_input(profile_data: dict):
    db = SessionLocal()
    try:
        # Date Parsing Section
        # Convert string dates from JSON to Python date objects for database storage
        # Format expected: 'YYYY-MM-DD' (e.g., '2025-08-07')
        start_date = None
        end_date = None
        
        if profile_data.get('start_date'):
            try:
                start_date = datetime.strptime(profile_data['start_date'], '%Y-%m-%d').date()
            except:
                start_date = None
                
        if profile_data.get('end_date'):
            try:
                end_date = datetime.strptime(profile_data['end_date'], '%Y-%m-%d').date()
            except:
                end_date = None

        user_input_record = UserInput(
            # Insurance Information
            have_insurance=profile_data.get('have_insurance', False),
            insurance_provider=profile_data.get('insurance_provider', ''),
            policy_number=profile_data.get('policy_number', ''),
            start_date=start_date,                    
            end_date=end_date,                       
            source=profile_data.get('source', ''),
            
            # Coverage Preferences
            coverage_type=profile_data.get('coverage_type', ''),
            providers=profile_data.get('providers', ''),
            current_conditions=profile_data.get('current_conditions', ''),
            current_prescriptions=profile_data.get('current_perscriptions', ''),  # JSON: current_perscriptions -> DB: current_prescriptions
            coverage_level=profile_data.get('coverage_level', ''),
            monthly_budget=profile_data.get('monthly_budget', ''),
            
            # Eligibility Information
            is_us_citizen=profile_data.get('is_US_Citizen', False),   
            is_medicaid=profile_data.get('is_Mediaid', False),           
            is_medicare=profile_data.get('is_Medicare', False),          
            events=profile_data.get('events', ''),
            is_veteran=profile_data.get('is_Veteran', False),          
            is_student_eligible=profile_data.get('is_StudentEligible', False),  
            
            # Document References
            user_insurance_docs=profile_data.get('user_insurance_docs', ''),
            proof_of_income_docs=profile_data.get('proof_of_income_docs', '')
        )
        
        # Database Operations
        db.add(user_input_record)       
        db.commit()                     
        db.refresh(user_input_record)    
        
        return user_input_record.id      
        
    except Exception as e:
        db.rollback()                  
        raise e                         
    finally:
        db.close()                       