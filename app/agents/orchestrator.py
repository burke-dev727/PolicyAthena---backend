from app.agents.input_interpreter import InputInterpreterAgent
from app.agents.plan_builder import PlanBuilderAgent
from app.agents.plan_matcher import PlanMatcherAgent
from app.agents.scorer import ScoringAgent
from app.agents.explanation import ExplanationAgent

import json
import os

# Sample hardcoded plan data
PLAN_DATA = [
    {
        "plan_id": "basic_1",
        "name": "Basic Plan",
        "features": ["feature_a", "feature_b"],
        "price": 10
    },
    {
        "plan_id": "premium_1",
        "name": "Premium Plan",
        "features": ["feature_a", "feature_b", "feature_c"],
        "price": 20
    }
]


class OrchestratorAgent:
    def __init__(self):
        self.input_agent = InputInterpreterAgent()
        self.plan_agent = PlanBuilderAgent()
        self.matcher = PlanMatcherAgent(PLAN_DATA)
        self.scorer = ScoringAgent()
        self.explainer = ExplanationAgent()

    def run(self, raw_input: dict):
        parsed = self.input_agent.run(raw_input)
        plan = self.plan_agent.run(parsed)
        matched = self.matcher.run(profile)
        scored = self.scorer.run(matched)
        explanation = self.explainer.run(scored[0], profile)
        return {
            "top_plan": scored[0],
            "alternatives": scored[1:3],
            "explanation": explanation
        }
