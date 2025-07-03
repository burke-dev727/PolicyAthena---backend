# Author: James Zheng
# Updated: 6/3/2025
# Notes: User inputs their data here. 
# Plans: Make a while loop to check if the inputs are correct. Redirect the inputted data into input_route.py.
class InputInterpreterAgent:
    # Personal Info
    def get_user_name():
        return input("Enter your first and last name: ")
    def get_user_age():
        return int(input("Enter your age: "))
    def get_user_email():
        return input("Enter your email: ")
    def get_user_phone():
        return input("Enter your phone number: ")
    def get_user_home(): 
        return input("Enter your address and street: ") # FInd a way to put in both address and street and isolate it into two variables
    def get_user_location(): 
        return input("Enter your city and the state: ") # Two variables
    def get_user_zipcode():
        return input("Enter your zipcode: ")
    def get_user_ssn():
        return input("Enter your Social Security Number: ")
    
    # Current Insurance
    def is_user_insurance():
        return input("Do you have health insurance (Y/N): ")
    def get_user_provider():
        return input("Enter your provider's name: ")
    def get_user_policyNumber():
        return input("Enter your policy number: ")
    def get_user_coverageStart():
        return input("Enter your coverage start date: ")
    def get_user_coverageEnd():
        return input("Enter your coverage end date: ")
    def get_user_sources():
        return input("Enter your source: ")
    
    # Employment Info
    def is_user_employed():
        return input("Are you employed (Y/N): ")
    def get_user_employer():
        return input("Enter your emplyer's name: ")
    def is_employer_insurance():
        return input("Does your employer offers insurance (Y/N): ")
    def get_user_annualIncome():
        return int(input("Enter your average annual income: "))
    def get_user_householdSize():
        return int(input("How many people live with you: "))
    
    # Coverage Needs
    def get_user_coverageType():
        return input("Enter your coverage type (family or individual): ")
    def get_user_providers(): # Make into an list
        return input("Enter your preferred providers (doctors, hospitals, or clinics): ")
    def get_user_existingConditions(): # list
        return input("Do you have any preexisitng medical conditions: ")
    def get_user_currentPrescription(): # list
        return input("Enter your current perscriptions: ")
    def get_user_coverageLevel():
        return input("Enter your coverage level: ")
    def get_user_Monthlybudget():
        return int(input("Enter your monthyl budget: "))
    
    # Eligibility Info
    def is_user_UScitizen():
        return input("Are you a U.S. citizen (Y/N): ")
    def is_user_medicaid():
        return input("Are you eligible for medicaid (Y/N): ")
    def is_user_medicare():
        return input("Are you eligible for medicare (Y/N): ")
    def get_user_recentEvent(): # list and also find the event dates
        return input("Enter your recent life events and its dates: ")
    def is_user_student():
        return input("Are you a current student (Y/N): ")
    def is_user_veteran():
        return input("Are you a veteran (Y/N): ")
    
    # Documents
    def get_user_insurance():
        return input("Enter your insurance card's or policy document's url: ")
    def get_user_proofOfIncome():
        return input("Enter your proof of income, residency, or employment documents url: ")
    
    # Redirect User's data into variables
    name = get_user_name()
    age = get_user_age()
    email = get_user_email()
    phone = get_user_phone()
    #address = get_user_home()
    #street = get_user_home()
    #city = get_user_location()
    #state = get_user_location()
    zipcode = get_user_zipcode()
    ssn = get_user_ssn()

    # Place variabels into a list
    user_data = [name, age, zipcode] 
    
    def run(self, raw_input: dict) -> dict:
        return raw_input
