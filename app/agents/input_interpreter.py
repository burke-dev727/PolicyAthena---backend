# Author: James Zheng
# Updated: 6/3/2025
# Notes: User inputs their data here. 
# Plans: Make a while loop to check if the inputs are correct. Redirect the inputted data into input_route.py.
class InputInterpreterAgent:
    # User's inputs
    def get_user_name():
            return input("Enter your name: ")
    def get_user_age():
         return int(input("Enter your age: "))
    def get_user_zipcode():
            return input("Enter your zipcode: ")
    
    # Redirect User's data into variables
    name = get_user_name()
    age = get_user_age()
    zipcode = get_user_zipcode()
    # Place variabels into a list
    user_data = [name, age, zipcode] 
    
    def run(self, raw_input: dict) -> dict:
        return raw_input
