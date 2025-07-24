# app/services/user_profile_service.py

from app.db.session import SessionLocal
from app.db.models import (
    PersonalInfo, CurrentInsurance, EmploymentInfo, CoverageNeeds,
    EligibilityInfo, Documents, UserProfile,
    PreferredProvider, PreexistingCondition, CurrentPrescription, RecentLifeEvent
)

def user_input(profile_data: dict):
    db = SessionLocal()
    try:
        # 1. Save each section
        personal_info = PersonalInfo(**profile_data['personal_info'])
        db.add(personal_info)
        db.flush()  # get id

        current_insurance = CurrentInsurance(**profile_data['current_insurance'])
        db.add(current_insurance)
        db.flush()

        employment_info = EmploymentInfo(**profile_data['employment_info'])
        db.add(employment_info)
        db.flush()

        coverage_needs = CoverageNeeds(
            coverage_type=profile_data['coverage_needs']['coverage_type'],
            coverage_level=profile_data['coverage_needs']['coverage_level'],
            monthly_budget=profile_data['coverage_needs']['monthly_budget']
        )
        db.add(coverage_needs)
        db.flush()

        # Save arrays for coverage_needs
        for provider in profile_data['coverage_needs']['preferred_providers']:
            db.add(PreferredProvider(coverage_needs_id=coverage_needs.id, provider_name=provider))
        for cond in profile_data['coverage_needs']['preexisting_conditions']:
            db.add(PreexistingCondition(coverage_needs_id=coverage_needs.id, condition=cond))
        for rx in profile_data['coverage_needs']['current_prescriptions']:
            db.add(CurrentPrescription(coverage_needs_id=coverage_needs.id, prescription=rx))

        eligibility_info = EligibilityInfo(
            is_us_citizen=profile_data['eligibility_info']['is_us_citizen'],
            eligible_for_medicaid=profile_data['eligibility_info']['eligible_for_medicaid'],
            eligible_for_medicare=profile_data['eligibility_info']['eligible_for_medicare'],
            is_student=profile_data['eligibility_info']['is_student'],
            is_veteran=profile_data['eligibility_info']['is_veteran']
        )
        db.add(eligibility_info)
        db.flush()

        # Save recent_life_event
        for event in profile_data['eligibility_info']['recent_life_event']:
            db.add(RecentLifeEvent(eligibility_info_id=eligibility_info.id, event=event))

        documents = Documents(**profile_data['documents'])
        db.add(documents)
        db.flush()

        # 2. Save main user_profiles row
        user_profile = UserProfile(
            personal_info_id=personal_info.id,
            current_insurance_id=current_insurance.id,
            employment_info_id=employment_info.id,
            coverage_needs_id=coverage_needs.id,
            eligibility_info_id=eligibility_info.id,
            documents_id=documents.id
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