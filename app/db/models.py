# app/db/models.py
# Created by Xinrui Hou
# Date: 2025-07-22
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Date, Text, ForeignKey, TIMESTAMP, text
import uuid

Base = declarative_base()

class PersonalInfo(Base):
    __tablename__ = "personal_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    ssn = Column(String(20))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(String(255))
    location = Column(String(100))
    zip_code = Column(String(20))

class CurrentInsurance(Base):
    __tablename__ = "current_insurance"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    has_insurance = Column(Boolean)
    provider_name = Column(String(255))
    policy_number = Column(String(100))
    coverage_start_date = Column(Date)
    coverage_end_date = Column(Date)
    source = Column(String(100))

class EmploymentInfo(Base):
    __tablename__ = "employment_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_employed = Column(Boolean)
    employer_name = Column(String(255))
    employer_offers_insurance = Column(Boolean)
    annual_income = Column(Integer)
    household_size = Column(Integer)

class CoverageNeeds(Base):
    __tablename__ = "coverage_needs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coverage_type = Column(String(50))
    coverage_level = Column(String(50))
    monthly_budget = Column(Integer)

class EligibilityInfo(Base):
    __tablename__ = "eligibility_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_us_citizen = Column(Boolean)
    eligible_for_medicaid = Column(Boolean)
    eligible_for_medicare = Column(Boolean)
    is_student = Column(Boolean)
    is_veteran = Column(Boolean)

class Documents(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    insurance_card_url = Column(Text)
    proof_of_income_url = Column(Text)

class PreferredProvider(Base):
    __tablename__ = "preferred_providers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coverage_needs_id = Column(String, ForeignKey('coverage_needs.id'))
    provider_name = Column(String(255))

class PreexistingCondition(Base):
    __tablename__ = "preexisting_conditions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coverage_needs_id = Column(String, ForeignKey('coverage_needs.id'))
    condition = Column(String(255))

class CurrentPrescription(Base):
    __tablename__ = "current_prescriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coverage_needs_id = Column(String, ForeignKey('coverage_needs.id'))
    prescription = Column(String(255))

class RecentLifeEvent(Base):
    __tablename__ = "recent_life_event"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    eligibility_info_id = Column(String, ForeignKey('eligibility_info.id'))
    event = Column(String(255))

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    personal_info_id = Column(String, ForeignKey('personal_info.id'))
    current_insurance_id = Column(String, ForeignKey('current_insurance.id'))
    employment_info_id = Column(String, ForeignKey('employment_info.id'))
    coverage_needs_id = Column(String, ForeignKey('coverage_needs.id'))
    eligibility_info_id = Column(String, ForeignKey('eligibility_info.id'))
    documents_id = Column(String, ForeignKey('documents.id'))
    created_at = Column(TIMESTAMP, server_default=text("timezone('utc', now())"))