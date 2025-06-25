from app.agents.input_interpreter import InputInterpreterAgent
from app.agents.profile_builder import ProfileBuilderAgent
from app.agents.plan_matcher import PlanMatcherAgent
from app.agents.scorer import ScoringAgent
from app.agents.explanation import ExplanationAgent

from app.agents.input_interpreter import InputInterpreterAgent
from app.agents.profile_builder import ProfileBuilderAgent
from app.agents.plan_matcher import PlanMatcherAgent
from app.agents.scorer import ScoringAgent
from app.agents.explanation import ExplanationAgent

class OrchestratorAgent:
    def __init__(self):
        self.input_agent = InputInterpreterAgent()
        self.profile_agent = ProfileBuilderAgent()

        mock_plans = [
            {"plan_id": "basic", "name": "Basic Plan"},
            {"plan_id": "premium", "name": "Premium Plan"},
            {"plan_id": "gold", "name": "Gold Plan"}
        ]
        self.matcher = PlanMatcherAgent(mock_plans)
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
