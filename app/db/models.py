# app/db/models.py
# Created by Xinrui Hou
# Date: 2025-07-22
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Date, Text, ForeignKey, TIMESTAMP, text, BigInteger
import uuid

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Basic profile fields
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    # Additional profile fields can be added here
    created_at = Column(TIMESTAMP, server_default=text("timezone('utc', now())"))

class UserInput(Base):
    __tablename__ = "user_input"
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Match BIGINT GENERATED ALWAYS AS IDENTITY
    have_insurance = Column(Boolean, nullable=False, default=False)
    insurance_provider = Column(Text)
    policy_number = Column(Text, default='')
    start_date = Column(Date)
    end_date = Column(Date)
    source = Column(Text)
    coverage_type = Column(Text)
    providers = Column(Text)
    current_conditions = Column(Text)
    current_prescriptions = Column(Text)  # Match database column name
    coverage_level = Column(Text)
    monthly_budget = Column(Text)
    is_us_citizen = Column(Boolean, nullable=False, default=False)  # Match database column name
    is_medicaid = Column(Boolean, nullable=False, default=False)  # Match database column name
    is_medicare = Column(Boolean, nullable=False, default=False)  # Match database column name
    events = Column(Text, default='')
    is_veteran = Column(Boolean, nullable=False, default=False)  # Match database column name
    is_student_eligible = Column(Boolean, nullable=False, default=False)  # Match database column name
    user_insurance_docs = Column(Text, default='')
    proof_of_income_docs = Column(Text, default='')
