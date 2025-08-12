class InputInterpreterAgent:
    def run(self, raw_input: dict) -> dict:
        # Since we're storing directly in user_input table, just return the raw data
        # The service will handle date parsing and data type conversion
        return raw_input
