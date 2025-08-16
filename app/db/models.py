# app/db/models.py
# Created by Xinrui Hou
# Date: 2025-07-22
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Date, Text, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy import func
import uuid

Base = declarative_base()


class PersonalInfo(Base):
    __tablename__ = "personal_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100))
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
    have_insurance = Column(Boolean, default=False, nullable=False)
    insurance_provider = Column(String(255))
    policy_number = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    source = Column(String(100))

class EmploymentInfo(Base):
    __tablename__ = "employment_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_employed = Column(Boolean, default=False, nullable=False)
    employer_name = Column(String(255))
    employer_offers_insurance = Column(Boolean, default=False, nullable=False)
    annual_income = Column(Integer)
    household_size = Column(Integer)

class CoverageNeeds(Base):
    __tablename__ = "coverage_needs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    coverage_type = Column(String(50))
    coverage_level = Column(String(50))
    monthly_budget = Column(Integer)
    preferred_providers = relationship("PreferredProvider", backref="coverage_needs")
    preexisting_conditions = relationship("PreexistingCondition", backref="coverage_needs")
    current_prescriptions = relationship("CurrentPrescription", backref="coverage_needs")

class EligibilityInfo(Base):
    __tablename__ = "eligibility_info"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    is_us_citizen = Column(Boolean, default=False, nullable=False)
    is_Mediaid = Column(Boolean, default=False, nullable=False)
    is_Medicare = Column(Boolean, default=False, nullable=False)
    is_student = Column(Boolean, default=False, nullable=False)
    is_veteran = Column(Boolean, default=False, nullable=False)

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
    __tablename__ = "recent_life_events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    eligibility_info_id = Column(String, ForeignKey('eligibility_info.id'))
    event = Column(String(255))

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    personal_info_id = Column(String, ForeignKey('personal_info.id')) 
    employment_info_id = Column(String, ForeignKey('employment_info.id'))
    personal_info = relationship("PersonalInfo")
    employment_info = relationship("EmploymentInfo")
    

class UserInput(Base):
    __tablename__ = "user_inputs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    current_insurance_id = Column(String, ForeignKey('current_insurance.id'))
    coverage_needs_id = Column(String, ForeignKey('coverage_needs.id'))
    eligibility_info_id = Column(String, ForeignKey('eligibility_info.id'))
    documents_id = Column(String, ForeignKey('documents.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Add relationships
    current_insurance = relationship("CurrentInsurance")
    coverage_needs = relationship("CoverageNeeds")
    eligibility_info = relationship("EligibilityInfo")
    documents = relationship("Documents")
