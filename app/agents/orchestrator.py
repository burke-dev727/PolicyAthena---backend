from app.agents.input_interpreter import InputInterpreterAgent
from app.agents.profile_builder import ProfileBuilderAgent
from app.agents.plan_matcher import PlanMatcherAgent
from app.agents.scorer import ScoringAgent
from app.agents.explanation import ExplanationAgent
#import json

class OrchestratorAgent:
    def __init__(self):
        self.input_agent = InputInterpreterAgent()
        self.profile_agent = ProfileBuilderAgent()
        self.matcher = PlanMatcherAgent()
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
