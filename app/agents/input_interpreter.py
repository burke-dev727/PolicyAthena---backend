# Author: James Zheng
# Updated: 6/3/2025
# Notes: User inputs their data here. 
# Plans: Make a while loop to check if the inputs are correct. Redirect the inputted data into input_route.py. May also put all three variables into an array.
class InputInterpreterAgent:
    # User's inputs
    def get_user_name():
            return input("Enter your name: ")
    def get_user_age():
         return int(input("Enter your age: "))
    def get_user_zipcode():
            return input("Enter your zipcode: ")
    
    # Redirect User's data into variables
    user_name = get_user_name()
    user_age = get_user_age()
    user_zipcode = get_user_zipcode()
    # from input_interpreter.py import user_name, user_age, user_zipcode
    
    def run(self, raw_input: dict) -> dict:
        return raw_input
