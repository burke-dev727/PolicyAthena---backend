import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.input_interpreter import InputInterpreterAgent
# Author: James Zheng
# Edited: 6/20/2025
# Updated 7/30/2025
# Description: This module interprets user input for the PolicyAthena application.
# Notes: Will need to create more validations and seperate each field into different classes.

# Variable to display when the input is incorrect
error = "Invalid input."

class InputInterpreterAgent:
    def run(self, raw_input: dict) -> dict:
        # Extract insurance-related fields
        insurance = {
            "have_insurance": raw_input.get("have_insurance", False),
            "insurance_provider": raw_input.get("insurance_provider", ""),
            "policy_number": raw_input.get("policy_number", ""),
            "start_date": raw_input.get("start_date", ""),
            "end_date": raw_input.get("end_date", ""),
            "source": raw_input.get("source", "")
        }

        # Extract coverage fields
        coverage = {
            "coverage_type": raw_input.get("coverage_type", ""),
            "providers": raw_input.get("providers", ""),
            "current_conditions": raw_input.get("current_conditions", ""),
            "current_perscriptions": raw_input.get("current_perscriptions", ""),
            "coverage_level": raw_input.get("coverage_level", ""),
            "monthly_budget": raw_input.get("monthly_budget", "")
        }

        # Extract eligibility fields
        eligibility = {
            "is_US_Citizen": raw_input.get("is_US_Citizen", False),
            "is_Mediaid": raw_input.get("is_Mediaid", False),
            "is_Medicare": raw_input.get("is_Medicare", False),
            "events": raw_input.get("events", ""),
            "is_Veteran": raw_input.get("is_Veteran", False),
            "is_StudentEligible": raw_input.get("is_StudentEligible", False)
        }

        # Extract preferences fields (delete later or move it)
        preferences = {
            "user_insurance_docs": raw_input.get("user_insurance_docs", ""),
            "proof_of_income_docs": raw_input.get("proof_of_income_docs", "")
        }

        # Validation (make more)
        if insurance["have_insurance"] and not insurance["insurance_provider"]:
            raise ValueError("Insurance provider must be filled if you have insurance.")

        return {
           # "personal": personal,
           # "employment": employment,
            "insurance": insurance,
            "coverage": coverage,
            "eligibility": eligibility,
            "preferences": preferences
        }
