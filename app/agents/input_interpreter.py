from input.user_inputs import PersonalInfo, CurrentInsurance, EmploymentInfo, CoverageNeeds, EligibilityInfo, Documents
# Edited: James Zheng
# Created: 6/20/2025
# Updated 7/9/2025
# Notes: User inputs their data here and transmitts it back to input_route
class InputInterpreterAgent:

    def run(self, raw_input: dict) -> dict:
        return raw_input