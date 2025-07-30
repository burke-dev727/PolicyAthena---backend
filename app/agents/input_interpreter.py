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
        # Placeholder: In the future, add preprocessing, validation, or transformation here
        required_fields = ["name", "age", "email", "phone", "address", "location", "zipcode", "ssn"]
        for field in required_fields:
            if not raw_input.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Check name is a valid string
        try: 
            name = raw_input.get("name", "")
            if not re.match(r"^[a-zA-Z\s]+$", name):
                raise ValueError("Name must contain only letters and spaces")
        except Exception:
            raise ValueError("Name must be a valid string")
        
        # Check age is a positive integer
        try:
            age = int(raw_input.get("age", 0))
            if age <= 0:
                raise ValueError("Age must be a positive integer")
        except Exception:
            raise ValueError("Age must be a valid integer")

        # Add more validation as needed...
        return raw_input