class PlanMatcherAgent:
    def __init__(self):
        self.mock_plans = [
            {"id": 1, "name": "Basic Plan"},
            {"id": 2, "name": "Premium Plan"},
            {"id": 3, "name": "Gold Plan"}
        ]

    def run(self, profile: dict):
        return self.mock_plans
