import re
# Author: James Zheng
# Edited: 6/20/2025
# Updated 7/13/2025
# Notes: User inputs their data here and transmitts it back to input_route

# Variable to display when the input is incorrect
error = "Invalid input. Please try Again."

# Personal Info
class PersonalInfo:
    # Get First and last name
    def get_user_name():
        while True:
            name = input("Enter your first and last name (e.g. 'Bob Joe'): ").strip()
            if name and all(a.isalpha() or a == " " for a in name):
                return name
            print(error)
        
    # Get age in integer
    def get_user_age():
        while True:
            age = input("Enter your age (e.g. 21): ")
            if age.isdigit():
                return age
            else:
                print(error)
    
    # Get email
    def get_user_email():
        while True:
            email = input("Enter your email (e.g. thisguy@gmail.com): ")
            if email.isdigit():
                print(error)
            else:
                return email
            
    # Get phone number
    def get_user_phone():
        phone_check = re.compile(r'^(\d{10}|\d{3}-\d{3}-\d{4})$')
        while True:
            phone = input("Enter your phone number (e.g. 123-456-7890): ")
            if phone_check.match(phone) and phone.isdigit:
                return phone
            else:
                print(error)
    
    # Get address number and street name in that order
    def get_user_home(): 
        home_check = re.compile(r'^\s*(\d+)\s*,\s*(.+\S)\s*$')
        while True:
            full_input = input("Enter your address (e.g., '123, Main Street'): ").strip()
            if home_check.match(full_input.strip()):
                address_num, street_name = full_input.split(' ', 1) 
                return address_num, street_name
            else:
                print(error)
    
    # Get city and state name
    def get_user_location(): 
        location_check = re.compile(r'^\s*(.+\S)\s*,\s*(.+\S)\s*$')
        while True:
            full_input = input("Enter your city and state (e.g., 'Plano, Texas'): ")
            try:
                int(full_input)
                print(error)
                continue
            except ValueError:
                pass

            if location_check.match(full_input.strip()):
                city_name, state_name = full_input.split(' ', 1)
                return city_name, state_name
            else:
                print(error)
    
    # Gte zipcode
    def get_user_zipcode():
        while True:
            zipcode_check = re.compile(r'^(\d{5})')
            zipcode = input("Enter your zipcode (e.g. 50234): ")
            if zipcode_check.match(zipcode) and zipcode.isdigit:
                return zipcode
            else:
                print(error)
    
    # Get Social Security Number
    def get_user_ssn():
        while True:
            ssn_check = re.compile(r'^(\d{9}|\d{3}-\d{2}-\d{4})$')
            ssn = input("Enter your Social Security Number (e.g. 453-33-9384): ")
            if ssn_check.match(ssn) and ssn.isdigit:
                return ssn
            else:
                print(error)
    
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
            if insurance.lower() == "y" or insurance.lower() == "n":
                return insurance
            else:
                print(error)
    
    # Get provider's name or the company that has insurance
    def get_user_provider():
        while True:
            provider = input("Enter your provider's name: ")
            if provider.strip():
                return provider
            else:
                print(error)

    
    # Get the polciy number
    def get_user_policyNumber():
        while True:
            policy = input("Enter your policy number: ")
            if policy != "":
                return policy
            else:
                print(error)
    
    # Get the coverage start date 
    def get_user_coverageStart():
        print("Now tell us if your current or last coverage start and end. If not, please type in 'none':")
        while True:
            date_check = re.compile(r'^(\d{8}|\d{4}-\d{2}-\d{2})$')
            date = input("Enter your coverage start date (e.g. YYYY-MM-DD): ").strip()
            clean_date = date.replace("-", "")
            if date.lower() == "none":
                return date
            if date_check.match(date) and clean_date.isdigit():
                return date
            else:
                print(error)
    
    # Get the coverage end date
    def get_user_coverageEnd():
        while True:
            date_check = re.compile(r'^(\d{8}|\d{4}-\d{2}-\d{2})$')
            date = input("Enter your coverage end date, or type in 'none' if you don't have coverage (e.g. YYYY-MM-DD): ").strip()
            clean_date = date.replace("-", "")
            if date.lower() == "none":
                return date
            if date_check.match(date) and clean_date.isdigit():
                return date
            else:
                print(error)
    
    # Get source
    def get_user_sources():
        while True:
            source = input("Enter whether you obatined a plan through work, a private insurer, or a government program (e.g., Medicare, Medicaid, Marketplace)?: ")
            return source 
    
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
        while True:
            answer = input("Are you employed (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # Get user's employer, such as a perosn or company (TEST)
    def get_user_employer():
        while True:
            employer = input("Enter your employer's name: ")
            if employer == "":
                print(error)
            else:
                return employer
    
    # If user's employer offers insurance
    def is_employer_insurance():
        while True:
            answer = input("Does your employer offers insurance (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # Get annual income of user
    def get_user_annualIncome():
        while True:
            income = input("Enter your average annual income: ")
            if income.isdigit():
                return income
            else:
                print(error)
    
    # Get household size of user
    def get_user_householdSize():
        while True:
            household = input("How many people live with you: ")
            if household.isdigit():
                return household
            else:
                print(error)
    
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
    # Get the coverage type of either indiviudal or family (TEST)
    def get_user_coverageType():
        while True:
            type = input("Enter your coverage type (family or individual): ")
            if type.lower() == "family" or type.lower() == "individual":
                return type
            else:
                print(error)
    
    # Get user's providers until user exits (TEST)
    def get_user_providers():
        list = []
        while True:
            i = input("Enter your preferred providers and type 'exit' when you are done (e.g. doctors, hospitals, or clinics): ")
            if i.lower() == "exit":
                return list
            if i == " ":
                print(error)

            list.append([i.strip()])
    
    # Get user's medical conditions in any amount until user exits (TEST)
    def get_user_existingConditions(): 
        list = []
        while True:
            i = input("Enter your current medical conditions and type 'exit' when you are done (e.g. asthma, heart problems, etc.): ")
            if i.lower() == "exit":
                return list
            if i == " ":
                print(error)

            list.append([i.strip()])
    
    # Get current prescription in any amount until user types i nexit to finish (TEST)
    def get_user_currentPrescription():
        list = []
        while True:
            i = input("Enter your current perscriptions and type 'exit' when you are done (e.g. ): ")
            if i.lower() == "exit":
                return list
            if i == " ":
                print(error)

            list.append([i.strip()])
    
    # Get one of the four coverage level, from Bronze, Silver, Gold, or Platinum
    def get_user_coverageLevel():
        while True:
            level = input("Enter your coverage level (Bronze, Silver, Gold, and Platinum): ")
            if level.lower() == "bronze" or level.lower() == "silver" or level.lower() == "gold" or level.lower() == "platinum":
                return level
            else:
                print(error)
    
    # Get user's monthly budget
    def get_user_Monthlybudget():
        while True:
            budget = input("Enter your monthly budget: ")
            if budget.isdigit():
                return budget
            else:
                print(error)
    
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
        while True:
            answer = input("Are you a U.S. citizen (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # if user has medicaid
    def is_user_medicaid():
        while True:
            answer = input("Are you eligible for medicaid (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # if user has medicare
    def is_user_medicare():
        while True:
            answer = input("Are you eligible for medicare (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # Get user's recent events into a 2D list
    def get_user_recentEvent():
        items = []
        print("Enter your recent life events and its dates (e.g. 'Wedding,YYYY-MM-DD'). Type 'exit' when finished: ")
        while True:
            repeat = input("Enter other recent life events and its dates: ")
            if repeat.lower() == "exit":
                break
            try:
                name_event, date_event = repeat.split(',')
                items.append([name_event.strip(), date_event.strip()])
            except ValueError:
                print("Invalid format. Please enter data as 'EventName,YYYY-MM-DD'.")
        return items
    
    # if user is a student
    def is_user_student():
        while True:
            answer = input("Are you a current student (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
    # if user is a veteran
    def is_user_veteran():
        while True:
            answer = input("Are you a veteran (Y/N): ")
            if answer.lower() == "y" or answer.lower() == "n":
                return answer
            else:
                print(error)
    
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
        while True:
            insurance = input("Enter your insurance card's or policy document link (must contain .url): ")
            if ".url" in insurance:
                return insurance
            else:
                print(error)
    
    # Get user's proof of income (with a residency, income, or employment documents) by posting a url link.
    def get_user_proofOfIncome():
        while True:
            proof = input("Enter your proof of income, residency, or employment documents (must contain .url): ")
            if ".url" in proof:
                return proof
            else:
                print(error)
    
    # Assigns new variables for each input data
    user_insurance = get_user_insurance()
    user_proofOfIncome = get_user_proofOfIncome()
    
    # Places docuemnt data into list
    list_documents = [user_insurance, user_proofOfIncome] # 2

# Test
print(PersonalInfo.list_personalInfo)
print(CurrentInsurance.list_currentInsurance)
print(EmploymentInfo.list_employmentInfo)
print(CoverageNeeds.list_coverageNeeds)
print(EligibilityInfo.list_eligibilityInfo)
print(Documents.list_documents)

class InputInterpreterAgent:
    def run(self, raw_input: dict) -> dict:
        return raw_input