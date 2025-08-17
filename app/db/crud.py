# app/db/crud.py
# Created by Xinrui Hou & James Zheng
# Date: 2025-07-22
# Updated: 2025-08-15
# Description: CRUD operations for the database
# Notes: 
#   - Modified logic and error handling for CRUD operations
#   - Added validation for userinput and userprofile data
#   - Added safe_int and safe_date functions for data conversion
#   - Modified the data validation logic for userinput and userprofile data
#   - Removed a data validation check for personal and employment info since they are not required to exist
from .session import SessionLocal
from .models import (
    UserProfile, UserInput, PersonalInfo, CurrentInsurance, EmploymentInfo,
    CoverageNeeds, EligibilityInfo, Documents, PreferredProvider,
    PreexistingCondition, CurrentPrescription, RecentLifeEvent
)
import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Safe integer conversion with error handling
def safe_int(value):
    try:
        return int(value) if value else None
    except (ValueError, TypeError):
        return None

# Safe date conversion
def safe_date(value):
    try:
        if value:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        return None
    except (ValueError, TypeError):
        return None

# Validate user input data
def validate_userinput_data(data):
    # Check if at least one of the main sections has data
    has_insurance_data = any([
        data.get("have_insurance") is not None,
        data.get("insurance_provider"),
        data.get("policy_number"),
        data.get("start_date"),
        data.get("end_date"),
        data.get("source")
    ])
    
    has_coverage_data = any([
        data.get("coverage_type"),
        data.get("coverage_level"),
        data.get("monthly_budget"),
        data.get("providers"),
        data.get("current_conditions"),
        data.get("current_prescriptions")
    ])
    
    has_eligibility_data = any([
        data.get("is_US_Citizen") is not None,
        data.get("is_Mediaid") is not None,
        data.get("is_Medicare") is not None,
        data.get("is_Veteran") is not None,
        data.get("is_StudentEligible") is not None,
        data.get("events")
    ])
    
    if not any([has_insurance_data, has_coverage_data, has_eligibility_data]):
        raise ValueError("At least one section (insurance, coverage, or eligibility) must have data")
    
    return True

# Validate user profile data
def validate_userprofile_data(data):
    # Check if at least one of the main sections has data
    has_personal_data = any([
        data.get("name"),
        data.get("age"),
        data.get("email"),
        data.get("phone"),
        data.get("address"),
        data.get("location"),
        data.get("zipcode"),
        data.get("ssn")
    ])
    
    has_employment_data = any([
        data.get("is_employed") is not None,
        data.get("employer_name"),
        data.get("is_employeroffers") is not None,
        data.get("annual_income"),
        data.get("household_size")
    ])
    
    if not any([has_personal_data, has_employment_data]):
        raise ValueError("At least one section (personal or employment) must have data")
    
    return True

def save_userinput_data(data: dict):
    db = SessionLocal()
    logger.info("Starting UserInput data save operation...")
    validate_userinput_data(data)
    logger.info("UserInput data validation passed")
    
    # UserInput Data
    try: 
         # Save CurrentInsurance
        logger.info("Creating CurrentInsurance record...")
        insurance = CurrentInsurance(
            have_insurance=data.get("have_insurance") if data.get("have_insurance") is not None else None,
            insurance_provider=data.get("insurance_provider") if data.get("insurance_provider") else None,
            policy_number=data.get("policy_number") if data.get("policy_number") else None,
            start_date=safe_date(data.get("start_date")),
            end_date=safe_date(data.get("end_date")),
            source=data.get("source") if data.get("source") else None
        )
        db.add(insurance)
        db.flush()
        logger.info(f"CurrentInsurance created with ID: {insurance.id}")

        # Save CoverageNeeds
        logger.info("Creating CoverageNeeds record...")
        coverage = CoverageNeeds(
            coverage_type=data.get("coverage_type") if data.get("coverage_type") else None,
            coverage_level=data.get("coverage_level") if data.get("coverage_level") else None,
            monthly_budget=safe_int(data.get("monthly_budget"))
        )
        db.add(coverage)
        db.flush()
        logger.info(f"CoverageNeeds created with ID: {coverage.id}")

        # Save EligibilityInfo
        logger.info("Creating EligibilityInfo record...")
        eligibility = EligibilityInfo(
            is_us_citizen=data.get("is_US_Citizen") if data.get("is_US_Citizen") is not None else None,
            is_Mediaid=data.get("is_Mediaid") if data.get("is_Mediaid") is not None else None,
            is_Medicare=data.get("is_Medicare") if data.get("is_Medicare") is not None else None,
            is_veteran=data.get("is_Veteran") if data.get("is_Veteran") is not None else None,
            is_student=data.get("is_StudentEligible") if data.get("is_StudentEligible") is not None else None
        )
        db.add(eligibility)
        db.flush()
        logger.info(f"EligibilityInfo created with ID: {eligibility.id}")

        # Save Documents
        logger.info("Creating Documents record...")
        documents = Documents(
            insurance_card_url=data.get("user_insurance_docs") if data.get("user_insurance_docs") else None,
            proof_of_income_url=data.get("proof_of_income_docs") if data.get("proof_of_income_docs") else None
        )
        db.add(documents)
        db.flush()
        logger.info(f"Documents created with ID: {documents.id}")

        # Save PreferredProviders
        providers_list = data.get("providers", [])
        if isinstance(providers_list, str):
            providers_list = [p.strip() for p in providers_list.split(",") if p.strip()]
        elif isinstance(providers_list, list):
            providers_list = [p for p in providers_list if p]
        
        if providers_list:
            logger.info(f"Creating {len(providers_list)} PreferredProvider records...")
            for provider in providers_list:
                if provider:
                    db.add(PreferredProvider(coverage_needs_id=coverage.id, provider_name=provider))
            logger.info("PreferredProviders created")

        # Save PreexistingConditions
        conditions_list = data.get("current_conditions", [])
        if isinstance(conditions_list, str):
            conditions_list = [c.strip() for c in conditions_list.split(",") if c.strip()]
        elif isinstance(conditions_list, list):
            conditions_list = [c for c in conditions_list if c]
        
        if conditions_list:
            logger.info(f"Creating {len(conditions_list)} PreexistingCondition records...")
            for condition in conditions_list:
                if condition:
                    db.add(PreexistingCondition(coverage_needs_id=coverage.id, condition=condition))
            logger.info("PreexistingConditions created")

        # Save CurrentPrescriptions
        prescriptions_list = data.get("current_prescriptions", [])
        if isinstance(prescriptions_list, str):
            prescriptions_list = [p.strip() for p in prescriptions_list.split(",") if p.strip()]
        elif isinstance(prescriptions_list, list):
            prescriptions_list = [p for p in prescriptions_list if p]
        
        if prescriptions_list:
            logger.info(f"Creating {len(prescriptions_list)} CurrentPrescription records...")
            for prescription in prescriptions_list:
                if prescription:
                    db.add(CurrentPrescription(coverage_needs_id=coverage.id, prescription=prescription))
            logger.info("CurrentPrescriptions created")

        # Save RecentLifeEvents
        events_list = data.get("events", [])
        if isinstance(events_list, str):
            events_list = [e.strip() for e in events_list.split(",") if e.strip()]
        elif isinstance(events_list, list):
            events_list = [e for e in events_list if e]
        
        if events_list:
            logger.info(f"Creating {len(events_list)} RecentLifeEvent records...")
            for event in events_list:
                if event:
                    db.add(RecentLifeEvent(eligibility_info_id=eligibility.id, event=event))
            logger.info("RecentLifeEvents created")

        # Save UserInput (linking all fields above)
        logger.info("Creating UserInput record to link all data...")
        user_input = UserInput(
            current_insurance_id=insurance.id,
            coverage_needs_id=coverage.id,
            eligibility_info_id=eligibility.id,
            documents_id=documents.id
        )

        db.add(user_input)
        db.commit()
        db.refresh(user_input)
        logger.info(f"UserInput created successfully with ID: {user_input.id}")
        return user_input.id
    except Exception as e:
        logger.error(f"Error saving UserInput data: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

def save_userprofile_data(data: dict):
    db = SessionLocal()
    logger.info("Starting UserProfile data save operation...")
    validate_userprofile_data(data)
    logger.info("UserProfile data validation passed")
    
    # UserProfile Data
    try:
        # Save PersonalInfo
        logger.info("Creating PersonalInfo record...")
        personal = PersonalInfo(
            name=data.get("name") if data.get("name") else None,
            age=safe_int(data.get("age")),
            email=data.get("email") if data.get("email") else None,
            phone=data.get("phone") if data.get("phone") else None,
            address=data.get("address") if data.get("address") else None,
            location=data.get("location") if data.get("location") else None,
            zip_code=data.get("zipcode") if data.get("zipcode") else None,
            ssn=data.get("ssn") if data.get("ssn") else None
        )
        db.add(personal)
        db.flush()
        logger.info(f"PersonalInfo created with ID: {personal.id}")

        # Save EmploymentInfo
        logger.info("Creating EmploymentInfo record...")
        employment = EmploymentInfo(
            is_employed=data.get("is_employed") if data.get("is_employed") is not None else None,
            employer_name=data.get("employer_name") if data.get("employer_name") else None,
            employer_offers_insurance=data.get("is_employeroffers") if data.get("is_employeroffers") is not None else None,
            annual_income=safe_int(data.get("annual_income")),
            household_size=safe_int(data.get("household_size"))
        )
        db.add(employment)
        db.flush()
        logger.info(f"EmploymentInfo created with ID: {employment.id}")

        # Save UserProfile (linking personal and employment info)
        logger.info("Creating UserProfile record to link personal and employment info...")
        user_profile = UserProfile(
            personal_info_id=personal.id,
            employment_info_id=employment.id
        )
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        logger.info(f"UserProfile created successfully with ID: {user_profile.id}")
        return user_profile.id
    except Exception as e:
        logger.error(f"Error saving UserProfile data: {e}")
        db.rollback()
        raise e
    finally:
        db.close()