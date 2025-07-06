# Author: James Zheng
# Updated: 6/3/2025
# Notes: User inputs their data here and transmitts it back to input_route
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
        full_input = input("Enter your address (e.g., '123, Main Street'): ")
        address_num, street_name = full_input.split(' ', 1) 
        return address_num, street_name
    
    def get_user_location(): 
        full_input = input("Enter your city and state (e.g., 'Plano, Texas'): ")
        city_name, state_name = full_input.split(' ', 1)
        return city_name, state_name
    
    def get_user_zipcode():
        return input("Enter your zipcode: ")
    
    def get_user_ssn():
        return input("Enter your Social Security Number: ")
    
    name = get_user_name()
    age = get_user_age()
    email = get_user_email()
    phone = get_user_phone()
    address, street = get_user_home()
    city, state = get_user_location()
    zip_code = get_user_zipcode()
    ssn = get_user_ssn()
    

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
    
    has_insurance = is_user_insurance()
    provider_name = get_user_provider()
    policy_number = get_user_policyNumber()
    coverage_start = get_user_coverageStart()
    coverage_end = get_user_coverageEnd()
    source = get_user_sources()
    

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
    
    is_employed = is_user_employed()
    employer_name = get_user_employer()
    employer_offers = is_employer_insurance()
    annual_income = get_user_annualIncome()
    household_size = get_user_householdSize()
    

    # Coverage Needs
    def get_user_coverageType():
        return input("Enter your coverage type (family or individual): ")
    
    def get_user_providers():
        i = input("Enter your preferred providers seperated by commas (e.g. doctors,hospitals,clinics): ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    def get_user_existingConditions(): 
        i = input("Do you have any preexisitng medical conditions, and if so, seperate answers by commas (e.g. asthma,hemoroids): ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    def get_user_currentPrescription():
        i = input("Enter your current perscriptions and seperate them by commas if neccessary: ")
        list = [s.strip() for s in i.split(",")]
        return list
    
    def get_user_coverageLevel():
        return input("Enter your coverage level: ")
    
    def get_user_Monthlybudget():
        return int(input("Enter your monthly budget: "))
    
    coverage_type = get_user_coverageType()
    providers_list = get_user_providers()
    existing_condtitions_list = get_user_existingConditions()
    current_perscription_list = get_user_currentPrescription()
    coverage_level = get_user_coverageLevel()
    monthly_budget = get_user_Monthlybudget()
    

    # Eligibility Info
    def is_user_UScitizen():
        return input("Are you a U.S. citizen (Y/N): ")
    
    def is_user_medicaid():
        return input("Are you eligible for medicaid (Y/N): ")
    
    def is_user_medicare():
        return input("Are you eligible for medicare (Y/N): ")
    
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
    
    def is_user_student():
        return input("Are you a current student (Y/N): ")
    
    def is_user_veteran():
        return input("Are you a veteran (Y/N): ")
    
    is_UScitizen = is_user_UScitizen()
    is_medicaid = is_user_medicaid()
    is_medicare = is_user_medicare()
    recentEvents_2DList = get_user_recentEvent()
    is_student = is_user_student()
    is_veteran = is_user_veteran()
    

    # Documents
    def get_user_insurance():
        return input("Enter your insurance card's or policy document's url: ")
    
    def get_user_proofOfIncome():
        return input("Enter your proof of income, residency, or employment documents url: ")
    
    user_insurance = get_user_insurance()
    user_proofOfIncome = get_user_proofOfIncome()
    
    # Place variabels into a list
    user_personalInfo = [] 
    user_currentInsurance = []
    user_employmentInfo = []
    user_coverageNeeds = []
    user_eligibilityInfo = []
    user_documents = []

    def run(self, raw_input: dict) -> dict:
        return raw_input