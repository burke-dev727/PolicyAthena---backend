# Created by Xinrui Hou
# Date: 2025-07-16
from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    age: int
    ssn: str
    email: str
    phone: str
    address: str

class CurrentInsurance(BaseModel):
    has_insurance: bool
    provider_name: str
    policy_number: str
    coverage_start_date: str
    coverage_end_date: str
    source: str

class EmploymentInfo(BaseModel):
    is_employed: bool
    employer_name: str
    employer_offers_insurance: bool
    annual_income: int
    household_size: int

class CoverageNeeds(BaseModel):
    coverage_type: str
    preferred_providers: List[str]
    preexisting_conditions: List[str]
    current_prescriptions: List[str]
    coverage_level: str
    monthly_budget: int

class EligibilityInfo(BaseModel):
    is_us_citizen: bool
    eligible_for_medicaid: bool
    eligible_for_medicare: bool
    recent_life_event: List[str]
    is_student: bool
    is_veteran: bool

class Documents(BaseModel):
    insurance_card_url: str
    proof_of_income_url: str

class UserProfileInput(BaseModel):
    personal_info: PersonalInfo
    current_insurance: CurrentInsurance
    employment_info: EmploymentInfo
    coverage_needs: CoverageNeeds
    eligibility_info: EligibilityInfo
    documents: Documents 