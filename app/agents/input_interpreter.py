import re
# Author: James Zheng
# Edited: 6/20/2025
# Updated 7/9/2025
# Notes: User inputs their data here and transmitts it back to input_route

# Personal Info
class PersonalInfo:
    # Get First and last name
    def get_user_name():
        while True:
            name = input("Enter your first and last name (e.g. 'Bob Joe'): ").strip()
            if name and all(a.isalpha() or a == " " for a in name):
                return name
            print("Invalid name. Please try again.")
        
    # Get age in integer
    def get_user_age():
        while True:
            age = input("Enter your age: ")
            if age.isdigit():
                return age
            else:
                print("Invalid age. Please enter with numbers and try again.")
    
    # Get email
    def get_user_email():
        while True:
            email = input("Enter your email: ")
            if email.isdigit():
                print("Invalid email. Please try again.")
            else:
                return email
    
    # Get phone number
    def get_user_phone():
        phone_check = re.compile(r'^(\d{10}|\d{3}-\d{3}-\d{4})$')
        while True:
            phone = input("Enter your phone number: ")
            if phone_check.match(phone) and phone.isdigit:
                return phone
            else:
                print("Invalid phone number. Please try again.")
    
    # Get address number and street name in that order, needs fixing for while loop
    def get_user_home(): 
        while True:
            # home_check = re.compile(r'^\d+\s+\w+(\s+\w+)+$')
            full_input = input("Enter your address (e.g., '123, Main Street'): ").strip()
            address_num, street_name = full_input.split(' ', 1) 
            return address_num, street_name
    
    # Get city and state name, needs fixing for while loop
    def get_user_location(): 
        while True:
            full_input = input("Enter your city and state (e.g., 'Plano, Texas'): ")
            city_name, state_name = full_input.split(' ', 1)
            return city_name, state_name
    
    # Gte zipcode
    def get_user_zipcode():
        while True:
            zipcode_check = re.compile(r'^(\d{5})')
            zipcode = input("Enter your zipcode (e.g. 50234): ")
            if zipcode_check.match(zipcode) and zipcode.isdigit:
                return zipcode
            else:
                print("Invalid zipcode. Please try again.")
    
    # Get Social Security Number
    def get_user_ssn():
        while True:
            ssn_check = re.compile(r'^(\d{9}|\d{3}-\d{2}-\d{4})$')
            ssn = input("Enter your Social Security Number: ")
            if ssn_check.match(ssn) and ssn.isdigit:
                return ssn
            else:
                print("Invalid Social Security Number. Pleas etry again.")
    
    # Direct input to variables
    name = get_user_name()
    age = get_user_age()
    email = get_user_email()
    phone = get_user_phone()
    address, street = get_user_home()
    city, state = get_user_location()
    zip_code = get_user_zipcode()
    ssn = get_user_ssn()

    # Put assigned variables into list
    list_personalInfo = [name, age, email, phone, address, street, city, state, zip_code, ssn] # 10

# Current Insurance
class CurrentInsurance:
    # Get if user has insurance or not
    def is_user_insurance():
        while True:
            insurance = input("Do you have health insurance (Y/N): ")
            if insurance == "Y".upper() or insurance == "N".upper:
                return insurance
            else:
                print("Invalid answer. Please try again.")
    
    # Get provider's name or the company that has insurance (IN PROGRESS)
    def get_user_provider():
        return input("Enter your provider's name: ")
    
    # Get the polciy number
    def get_user_policyNumber():
        return input("Enter your policy number: ")
    
    # Get the coverage start date
    def get_user_coverageStart():
        return input("Enter your coverage start date: ")
    
    # Get the coverage end date
    def get_user_coverageEnd():
        return input("Enter your coverage end date: ")
    
    # Get sources
    def get_user_sources():
        return input("Enter your source: ")
    
    # Direct input to variables
    has_insurance = is_user_insurance()
    provider_name = get_user_provider()
    policy_number = get_user_policyNumber()
    coverage_start = get_user_coverageStart()
    coverage_end = get_user_coverageEnd()
    source = get_user_sources()

    # Put assigned variables into list
    list_currentInsurance = [has_insurance, provider_name, policy_number, coverage_start, coverage_end, source] # 6

# Employment Info
class EmploymentInfo:
    # If user is employed or not
    def is_user_employed():
        return input("Are you employed (Y/N): ")
    
    # Get user's employer, such as a perosn or company
    def get_user_employer():
        return input("Enter your emplyer's name: ")
    
    # If user's employer offers insurance
    def is_employer_insurance():
        return input("Does your employer offers insurance (Y/N): ")
    
    # Get annual income of user
    def get_user_annualIncome():
        return int(input("Enter your average annual income: "))
    
    # Get household size of user
    def get_user_householdSize():
        return int(input("How many people live with you: "))
    
    # Direct input to variables
    is_employed = is_user_employed()
    employer_name = get_user_employer()
    employer_offers = is_employer_insurance()
    annual_income = get_user_annualIncome()
    household_size = get_user_householdSize()

    # Put assigned variables into list
    list_employmentInfo = [is_employed, employer_name, employer_offers, annual_income, household_size] # 5

# Coverage Needs
class CoverageNeeds:
    # Get the coverage type of either indiviudal or family
    def get_user_coverageType():
        return input("Enter your coverage type (family or individual): ")
    
    # Get user's providers seperated by comma
    def get_user_providers():
        i = input("Enter your preferred providers seperated by commas (e.g. doctors,hospitals,clinics): ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    # Get user's medical conditions in any amount seperated by commas
    def get_user_existingConditions(): 
        i = input("Do you have any preexisitng medical conditions, and if so, seperate answers by commas (e.g. asthma,hemoroids): ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    # Get current prescription in any amount seperated by commas
    def get_user_currentPrescription():
        i = input("Enter your current perscriptions and seperate them by commas if neccessary: ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    # Get one of the four coverage level, from Bronze, Silver, Gold, or Platinum
    def get_user_coverageLevel():
        return input("Enter your coverage level: ")
    
    # Get user's monthly budget
    def get_user_Monthlybudget():
        return int(input("Enter your monthly budget: "))
    
    # Direct input to variables
    coverage_type = get_user_coverageType()
    providers_list = get_user_providers()
    existing_condtitions_list = get_user_existingConditions()
    current_perscription_list = get_user_currentPrescription()
    coverage_level = get_user_coverageLevel()
    monthly_budget = get_user_Monthlybudget()

    # Place new variables into list
    list_coverageNeeds = [coverage_type, providers_list, existing_condtitions_list, current_perscription_list, coverage_level, monthly_budget] # 6

# Eligibility Info
class EligibilityInfo:
    # if user is a US citizen
    def is_user_UScitizen():
        return input("Are you a U.S. citizen (Y/N): ")
    
    # if user has medicaid
    def is_user_medicaid():
        return input("Are you eligible for medicaid (Y/N): ")
    
    # if user has medicare
    def is_user_medicare():
        return input("Are you eligible for medicare (Y/N): ")
    
    # Get user's recent events into a 2D list
    def get_user_recentEvent():
        items = []
        print("Enter your recent life events and its dates (e.g. 'Wedding,07-06-2025'). Type 'exit' when finished: ")
        while True:
            repeat = input("Enter other recent life events and its dates: ")
            if repeat.lower() == "exit":
                break
            try:
                name_event, date_event = repeat.split(',')
                items.append([name_event.strip(), date_event.strip()])
            except ValueError:
                print("Invalid format. Please enter data as: 'EventName,Dates'")
        return items
    
    # if user is a student
    def is_user_student():
        return input("Are you a current student (Y/N): ")
    
    # if user is a veteran
    def is_user_veteran():
        return input("Are you a veteran (Y/N): ")
    
    # Input data assign into new variables
    is_UScitizen = is_user_UScitizen()
    is_medicaid = is_user_medicaid()
    is_medicare = is_user_medicare()
    recentEvents_2DList = get_user_recentEvent()
    is_student = is_user_student()
    is_veteran = is_user_veteran()

    # Puts new varibales into list
    list_eligibilityInfo = [is_UScitizen, is_medicaid, is_medicare, recentEvents_2DList, is_student, is_veteran] # 6

# Documents Input
class Documents:
    # Get user's insurance through a url link
    def get_user_insurance():
        return input("Enter your insurance card's or policy document's url: ")
    
    # Get user's proof of income (with a residency, income, or employment documents) by posting a url link.
    def get_user_proofOfIncome():
        return input("Enter your proof of income, residency, or employment documents url: ")
    
    # Assigns new variables for each input data
    user_insurance = get_user_insurance()
    user_proofOfIncome = get_user_proofOfIncome()
    
    # Places docuemnt data into list
    list_documents = [user_insurance, user_proofOfIncome] # 2

class InputInterpreterAgent:
    def run(self, raw_input: dict) -> dict:
        return raw_input
