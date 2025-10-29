# app/db/models.py
# Created by Xinrui Hou
# Date: 2025-07-22
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Date, Text, ForeignKey, TIMESTAMP, text, BigInteger
import uuid

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profile"  # Match actual table name
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Match BIGINT GENERATED ALWAYS AS IDENTITY
    user_id = Column(String, nullable=True)  # Optional user ID without foreign key constraint
    name = Column(Text)  # Match database column
    age = Column(Text)  # Match database column (TEXT, not INTEGER)
    email = Column(Text)  # Match database column
    street_address = Column(Text)  # Match database column name
    city = Column(Text)  # Match database column
    state = Column(Text)  # Match database column
    zipcode = Column(Text)  # Match database column name
    is_employed = Column(Boolean, default=False)  # Match database column
    employer_name = Column(Text)  # Match database column
    is_employeroffers = Column(Boolean, default=False)  # Match database column name
    annual_income = Column(Text)  # Match database column
    household_size = Column(Text)  # Match database column

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
