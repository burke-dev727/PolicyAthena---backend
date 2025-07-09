class PersonalInfo:
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

    user_personalInfo = [name, age, email, phone, address, street, city, state, zip_code, ssn]
    
