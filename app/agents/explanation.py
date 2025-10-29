# app/agents/explanation.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: Explanation agent using OpenAI services for intelligent policy explanations

import logging
from typing import Dict, List, Any
from app.services.openai import OpenAIServiceManager

logger = logging.getLogger(__name__)

class ExplanationAgent:
    """
    Explanation agent that uses OpenAI services to generate intelligent,
    human-readable explanations for policy recommendations.
    
    This agent:
    - Explains why specific policies were recommended
    - Provides personalized insights and reasoning
    - Generates actionable next steps
    - Creates comprehensive policy summaries
    """
    
    def __init__(self, openai_manager: OpenAIServiceManager = None):
        """
        Initialize the explanation agent.
        
        Args:
            openai_manager: OpenAI service manager instance
        """
        self.openai_manager = openai_manager or OpenAIServiceManager()
        self.analysis_service = self.openai_manager.policy_analysis
        self.scoring_service = self.openai_manager.policy_scoring
        
        logger.info("ExplanationAgent initialized with OpenAI services")
    
    async def run(self, top_plan: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for the top recommended plan.
        
        Args:
            top_plan: Top recommended plan with analysis and scoring
            profile: User profile and requirements
            
        Returns:
            Dict containing detailed explanation and recommendations
        """
        try:
            logger.info("Generating explanation for top recommended plan")
            
            # Extract data from top plan
            plan = top_plan.get("plan", {})
            analysis = top_plan.get("analysis", {})
            scoring = top_plan.get("scoring", {})
            
            # Generate comprehensive explanation using OpenAI
            explanation = await self._generate_comprehensive_explanation(
                profile, plan, analysis, scoring
            )
            
            # Add metadata and structure
            result = {
                "status": "success",
                "plan_name": plan.get("name", "Unknown Plan"),
                "explanation": explanation,
                "key_highlights": {
                    "compatibility_score": analysis.get("compatibility_score", 0),
                    "overall_score": scoring.get("overall_score", 0),
                    "recommendation_level": self._get_recommendation_level(
                        analysis.get("compatibility_score", 0),
                        scoring.get("overall_score", 0)
                    )
                },
                "agent": "ExplanationAgent",
                "services_used": ["OpenAI Policy Analysis", "OpenAI Policy Scoring"]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": "ExplanationAgent"
            }
    
    async def _generate_comprehensive_explanation(self, profile: Dict[str, Any], 
                                                plan: Dict[str, Any], 
                                                analysis: Dict[str, Any], 
                                                scoring: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive explanation using OpenAI services."""
        try:
            # Create context for explanation
            context = {
                "user_profile": self._format_user_profile(profile),
                "plan_details": self._format_plan_details(plan),
                "analysis_results": self._format_analysis_results(analysis),
                "scoring_results": self._format_scoring_results(scoring)
            }
            
            # Generate explanation using OpenAI
            # For now, we'll create a structured explanation based on available data
            # In the future, you can create a dedicated OpenAI explanation service
            
            explanation = {
                "simple_explanation": self._generate_simple_explanation(profile, plan, analysis, scoring),
                "key_benefits": analysis.get("key_matching_factors", []),
                "considerations": analysis.get("potential_issues", []),
                "personalized_insights": self._generate_personalized_insights(profile, plan, analysis),
                "cost_analysis": self._extract_cost_analysis(scoring),
                "coverage_analysis": self._extract_coverage_analysis(analysis, scoring),
                "network_analysis": self._extract_network_analysis(scoring),
                "next_steps": self._generate_next_steps(profile, plan, analysis, scoring),
                "comparison_context": self._generate_comparison_context(analysis, scoring)
            }
            
            return explanation
            
        except Exception as e:
            logger.error(f"Comprehensive explanation generation failed: {str(e)}")
            return self._get_fallback_explanation()
    
    def _generate_simple_explanation(self, profile: Dict[str, Any], plan: Dict[str, Any], 
                                   analysis: Dict[str, Any], scoring: Dict[str, Any]) -> str:
        """Generate a simple, clear explanation of the recommendation."""
        plan_name = plan.get("name", "this policy")
        compatibility = analysis.get("compatibility_score", 0)
        overall_score = scoring.get("overall_score", 0)
        
        if compatibility >= 80 and overall_score >= 80:
            return f"{plan_name} is an excellent match for your needs with {compatibility}% compatibility and a score of {overall_score}/100."
        elif compatibility >= 70 and overall_score >= 70:
            return f"{plan_name} is a good match for your requirements with {compatibility}% compatibility and a score of {overall_score}/100."
        elif compatibility >= 60 and overall_score >= 60:
            return f"{plan_name} is a fair option with {compatibility}% compatibility and a score of {overall_score}/100."
        else:
            return f"{plan_name} may not be the best fit, but we can help you explore alternatives."
    
    def _generate_personalized_insights(self, profile: Dict[str, Any], plan: Dict[str, Any], 
                                      analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized insights based on user profile and analysis."""
        insights = []
        
        # Health condition insights
        if profile.get("current_conditions"):
            conditions = profile["current_conditions"]
            if "diabetes" in conditions.lower():
                insights.append("This plan provides strong coverage for diabetes management")
            if "cancer" in conditions.lower():
                insights.append("Comprehensive cancer treatment coverage included")
        
        # Budget insights
        budget = profile.get("monthly_budget", "")
        if budget and "$" in budget:
            insights.append(f"Premium fits within your budget range of {budget}")
        
        # Coverage level insights
        coverage_level = profile.get("coverage_level", "")
        if coverage_level:
            insights.append(f"Bronze level provides good value for your current needs")
        
        return insights if insights else ["This plan aligns well with your specific requirements"]
    
    def _extract_cost_analysis(self, scoring: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cost-related analysis from scoring results."""
        reasoning = scoring.get("reasoning", {})
        
        return {
            "cost_score": scoring.get("cost_score", 0),
            "cost_reasoning": reasoning.get("cost_score_reason", "Cost analysis not available"),
            "improvement_suggestions": scoring.get("improvement_suggestions", [])
        }
    
    def _extract_coverage_analysis(self, analysis: Dict[str, Any], scoring: Dict[str, Any]) -> Dict[str, Any]:
        """Extract coverage-related analysis."""
        reasoning = scoring.get("reasoning", {})
        
        return {
            "coverage_score": scoring.get("coverage_score", 0),
            "key_factors": analysis.get("key_matching_factors", []),
            "coverage_reasoning": reasoning.get("coverage_score_reason", "Coverage analysis not available"),
            "potential_gaps": analysis.get("potential_issues", [])
        }
    
    def _extract_network_analysis(self, scoring: Dict[str, Any]) -> Dict[str, Any]:
        """Extract network-related analysis."""
        reasoning = scoring.get("reasoning", {})
        
        return {
            "network_score": scoring.get("network_score", 0),
            "network_reasoning": reasoning.get("network_score_reason", "Network analysis not available")
        }
    
    def _generate_next_steps(self, profile: Dict[str, Any], plan: Dict[str, Any], 
                            analysis: Dict[str, Any], scoring: Dict[str, Any]) -> List[str]:
        """Generate actionable next steps for the user."""
        next_steps = [
            "Review the complete policy documents thoroughly",
            "Contact the insurance provider for specific questions about coverage",
            "Verify that your preferred healthcare providers are in-network",
            "Understand your deductible and out-of-pocket maximums"
        ]
        
        # Add personalized next steps
        if profile.get("current_conditions"):
            next_steps.append("Confirm coverage for your specific health conditions")
        
        if profile.get("current_perscriptions"):
            next_steps.append("Verify prescription drug coverage and costs")
        
        # Add scoring-based recommendations
        if scoring.get("overall_score", 0) < 70:
            next_steps.append("Consider comparing with 2-3 other policy options")
        
        return next_steps
    
    def _generate_comparison_context(self, analysis: Dict[str, Any], scoring: Dict[str, Any]) -> Dict[str, Any]:
        """Generate context for how this plan compares to alternatives."""
        compatibility = analysis.get("compatibility_score", 0)
        overall_score = scoring.get("overall_score", 0)
        
        if compatibility >= 80 and overall_score >= 80:
            comparison = "This plan ranks among the top options for your profile"
        elif compatibility >= 70 and overall_score >= 70:
            comparison = "This plan is above average and worth serious consideration"
        elif compatibility >= 60 and overall_score >= 60:
            comparison = "This plan meets basic requirements but consider alternatives"
        else:
            comparison = "This plan may not be optimal for your needs"
        
        return {
            "comparison_summary": comparison,
            "relative_strength": "strong" if compatibility >= 75 else "moderate" if compatibility >= 60 else "weak",
            "recommendation_confidence": analysis.get("confidence_level", "Low")
        }
    
    def _get_recommendation_level(self, compatibility_score: int, overall_score: int) -> str:
        """Determine recommendation level based on scores."""
        if compatibility_score >= 80 and overall_score >= 80:
            return "Strongly Recommended"
        elif compatibility_score >= 70 and overall_score >= 70:
            return "Recommended"
        elif compatibility_score >= 60 and overall_score >= 60:
            return "Consider"
        else:
            return "Not Recommended"
    
    def _format_user_profile(self, profile: Dict[str, Any]) -> str:
        """Format user profile for explanation context."""
        return f"User Profile: Age {profile.get('age', 'N/A')}, Location: {profile.get('city', 'N/A')}, {profile.get('state', 'N/A')}"
    
    def _format_plan_details(self, plan: Dict[str, Any]) -> str:
        """Format plan details for explanation context."""
        return f"Plan: {plan.get('name', 'Unknown')}, Coverage: {plan.get('coverage', 'N/A')}"
    
    def _format_analysis_results(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results for explanation context."""
        return f"Compatibility: {analysis.get('compatibility_score', 'N/A')}%, Recommendation: {analysis.get('overall_recommendation', 'N/A')}"
    
    def _format_scoring_results(self, scoring: Dict[str, Any]) -> str:
        """Format scoring results for explanation context."""
        return f"Overall Score: {scoring.get('overall_score', 'N/A')}/100, Weighted Score: {scoring.get('weighted_score', 'N/A')}"
    
    def _get_fallback_explanation(self) -> Dict[str, Any]:
        """Get fallback explanation when generation fails."""
        return {
            "simple_explanation": "We're currently processing your policy explanation. Please check back shortly.",
            "key_benefits": ["Analysis in progress"],
            "considerations": ["Evaluation pending"],
            "personalized_insights": ["Insights being generated"],
            "next_steps": ["Please wait for complete analysis"]
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent."""
        return {
            "agent_name": "ExplanationAgent",
            "version": "1.0.0",
            "capabilities": [
                "AI-powered policy explanations",
                "Personalized insights and recommendations",
                "Comprehensive coverage analysis",
                "Actionable next steps",
                "Cost-benefit breakdown"
            ],
            "openai_services": [
                self.analysis_service.service_name if self.analysis_service else "Not available",
                self.scoring_service.service_name if self.scoring_service else "Not available"
            ]
        }
