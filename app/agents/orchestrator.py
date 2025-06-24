from agents.input_interpreter import InputInterpreterAgent
from agents.profile_builder import ProfileBuilderAgent
from agents.plan_matcher import PlanMatcherAgent
from agents.scorer import ScoringAgent
from agents.explanation import ExplanationAgent
import json

with open("data/plans.json") as f:
    PLAN_DATA = json.load(f)

class OrchestratorAgent:
    def __init__(self):
        self.input_agent = InputInterpreterAgent()
        self.profile_agent = ProfileBuilderAgent()
        self.matcher = PlanMatcherAgent(PLAN_DATA)
        self.scorer = ScoringAgent()
        self.explainer = ExplanationAgent()

    def run(self, raw_input: dict):
        parsed = self.input_agent.run(raw_input)
        profile = self.profile_agent.run(parsed)
        matched = self.matcher.run(profile)
        scored = self.scorer.run(matched)
        explanation = self.explainer.run(scored[0], profile)
        return {
            "top_plan": scored[0],
            "alternatives": scored[1:3],
            "explanation": explanation
        }
