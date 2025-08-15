# app/db/crud.py
# Created by Xinrui Hou & James Zheng
# Date: 2025-07-22
# Updated: 2025-08-11
from .session import SessionLocal
from .models import (
    UserProfile, UserInput, PersonalInfo, CurrentInsurance, EmploymentInfo,
    CoverageNeeds, EligibilityInfo, Documents, PreferredProvider,
    PreexistingCondition, CurrentPrescription, RecentLifeEvent
)

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
    required_fields = ["have_insurance", "coverage_type", "coverage_level"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")
    return True

def save_userinput_data(data: dict):
    db = SessionLocal()
    validate_userinput_data(data)
    # UserInput Data
    try: 
         # Save CurrentInsurance
        insurance = CurrentInsurance(
            have_insurance=data.get("have_insurance") if data.get("have_insurance") else None,
            insurance_provider=data.get("insurance_provider", "") if data.get("insurance_provider") else None,
            policy_number=data.get("policy_number", "") if data.get("policy_number") else None,
            start_date=safe_date(data.get("start_date")),
            end_date=safe_date(data.get("end_date")),
            source=data.get("source", "") if data.get("source") else None
        )
        db.add(insurance)
        db.flush()

        # Save CoverageNeeds
        coverage = CoverageNeeds(
            coverage_type=data.get("coverage_type", "") if data.get("coverage_type") else None,
            coverage_level=data.get("coverage_level", "") if data.get("coverage_level") else None,
            monthly_budget=safe_int(data.get("monthly_budget"))
        )
        db.add(coverage)
        db.flush()

        # Save EligibilityInfo
        eligibility = EligibilityInfo(
            is_us_citizen=data.get("is_US_Citizen") if data.get("is_US_Citizen") else None,
            is_Mediaid=data.get("is_Mediaid") if data.get("is_Mediaid") else None,
            is_Medicare=data.get("is_Medicare") if data.get("is_Medicare") else None,
            is_veteran=data.get("is_Veteran") if data.get("is_Veteran") else None,
            is_student=data.get("is_StudentEligible") if data.get("is_StudentEligible") else None
        )
        db.add(eligibility)
        db.flush()

        # Save Documents
        documents = Documents(
            insurance_card_url=data.get("user_insurance_docs", "") if data.get("user_insurance_docs", "") else None,
            proof_of_income_url=data.get("proof_of_income_docs", "") if data.get("proof_of_income_docs", "") else None
        )
        db.add(documents)
        db.flush()

        # Save PreferredProviders
        providers_list = data.get("providers", [])
        if isinstance(providers_list, str):
            providers_list = [p.strip() for p in providers_list.split(",") if p.strip()]
        elif isinstance(providers_list, list):
            providers_list = [p for p in providers_list if p]
        for provider in providers_list:
            if provider:
                db.add(PreferredProvider(coverage_needs_id=coverage.id, provider_name=provider))

        # Save PreexistingConditions
        conditions_list = data.get("current_conditions", [])
        if isinstance(conditions_list, str):
            conditions_list = [c.strip() for c in conditions_list.split(",") if c.strip()]
        elif isinstance(conditions_list, list):
            conditions_list = [c for c in conditions_list if c]
        for condition in conditions_list:
            if condition:
                db.add(PreexistingCondition(coverage_needs_id=coverage.id, condition=condition))

        # Save CurrentPrescriptions
        prescriptions_list = data.get("current_prescriptions", [])
        if isinstance(prescriptions_list, str):
            prescriptions_list = [p.strip() for p in prescriptions_list.split(",") if p.strip()]
        elif isinstance(prescriptions_list, list):
            prescriptions_list = [p for p in prescriptions_list if p]
        for prescription in prescriptions_list:
            if prescription:
                db.add(CurrentPrescription(coverage_needs_id=coverage.id, prescription=prescription))

        # Save RecentLifeEvents
        events_list = data.get("events", [])
        if isinstance(events_list, str):
            events_list = [e.strip() for e in events_list.split(",") if e.strip()]
        elif isinstance(events_list, list):
            events_list = [e for e in events_list if e]
        for event in events_list:
            if event:
                db.add(RecentLifeEvent(eligibility_info_id=eligibility.id, event=event))

        # Save UserInput (linking all fields above)
        user_input = UserInput(
            current_insurance_id=insurance.id,
            coverage_needs_id=coverage.id,
            eligibility_info_id=eligibility.id,
            documents_id=documents.id
        )

        db.add(user_input)
        db.commit()
        db.refresh(user_input)
        return user_input.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def save_userprofile_data(data: dict):
    db = SessionLocal()
    # UserProfile Data
    try:
        # Save PersonalInfo
        personal = PersonalInfo(
            name=data.get("name", "") if data.get("name") else None,
            age=safe_int(data.get("age")),
            email=data.get("email", "") if data.get("email") else None,
            phone=data.get("phone", "") if data.get("phone") else None,
            address=data.get("address", "") if data.get("address") else None,
            location=data.get("location", "") if data.get("location") else None,
            zip_code=data.get("zipcode", "") if data.get("zipcode") else None,
            ssn=data.get("ssn", "") if data.get("ssn") else None
        )
        db.add(personal)
        db.flush()

        # Save EmploymentInfo
        employment = EmploymentInfo(
            is_employed=data.get("is_employed") if data.get("is_employed") else None,
            employer_name=data.get("employer_name", "") if data.get("employer_name") else None,
            employer_offers_insurance=data.get("is_employeroffers") if data.get("is_employeroffers") else None,
            annual_income=safe_int(data.get("annual_income")),
            household_size=safe_int(data.get("household_size"))
        )
        db.add(employment)
        db.flush()

        # Save UserProfile (linking personal and employment info)
        user_profile = UserProfile(
            personal_info_id=personal.id,
            employment_info_id=employment.id
        )
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        return user_profile.id
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()