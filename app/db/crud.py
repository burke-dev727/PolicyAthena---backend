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

def save_userinput_data(data: dict):
    db = SessionLocal()
    # UserInput Data
    try: 
         # Save CurrentInsurance
        insurance = CurrentInsurance(
            has_insurance=data.get("have_insurance") if data.get("have_insurance") else None,
            insurance_provider=data.get("insurance_provider", "") if data.get("insurance_provider") else None,
            policy_number=data.get("policy_number", "") if data.get("policy_number") else None,
            start_date=data.get("start_date") if data.get("start_date") else None,
            end_date=data.get("end_date") if data.get("end_date") else None,
            source=data.get("source", "") if data.get("source") else None
        )
        db.add(insurance)
        db.flush()

        # Save CoverageNeeds
        coverage = CoverageNeeds(
            coverage_type=data.get("coverage_type", "") if data.get("coverage_type") else None,
            coverage_level=data.get("coverage_level", "") if data.get("coverage_level") else None,
            monthly_budget=int(data.get("monthly_budget")) if data.get("monthly_budget") else None
        )
        db.add(coverage)
        db.flush()

        # Save EligibilityInfo
        eligibility = EligibilityInfo(
            is_us_citizen=data.get("is_US_Citizen") if data.get("is_US_Citizen") else None,
            eligible_for_medicaid=data.get("is_Medicaid") if data.get("is_Medicaid") else None,
            eligible_for_medicare=data.get("is_Medicare") if data.get("is_Medicare") else None,
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

        # Save PreferredProviders, PreexistingConditions, CurrentPrescriptions, RecentLifeEvents
        for provider in data.get("providers", "").split(","):
            if provider.strip():
                db.add(PreferredProvider(coverage_needs_id=coverage.id, provider_name=provider.strip()))
            else:
                db.add(PreferredProvider(coverage_needs_id=coverage.id, provider_name=None))
        for cond in data.get("current_conditions", "").split(","):
            if cond.strip():
                db.add(PreexistingCondition(coverage_needs_id=coverage.id, condition=cond.strip()))
            else:
                db.add(PreexistingCondition(coverage_needs_id=coverage.id, condition=None))
        for rx in data.get("current_prescriptions", "").split(","):
            if rx.strip():
                db.add(CurrentPrescription(coverage_needs_id=coverage.id, prescription=rx.strip()))
            else:
                db.add(CurrentPrescription(coverage_needs_id=coverage.id, prescription=None))
        for event in data.get("events", "").split(","):
            if event.strip():
                db.add(RecentLifeEvent(eligibility_info_id=eligibility.id, event=event.strip()))
            else:
                db.add(RecentLifeEvent(eligibility_info_id=eligibility.id, event=None))

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
            age=int(data.get("age")) if data.get("age") else None,
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
            annual_income=int(data.get("annual_income")) if data.get("annual_income") else None,
            household_size=int(data.get("household_size")) if data.get("household_size") else None
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