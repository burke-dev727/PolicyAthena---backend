# app/agents/plan_matcher.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: Plan matcher agent using OpenAI services for intelligent policy matching

import logging
from typing import Dict, List, Any
from app.services.openai import OpenAIServiceManager

logger = logging.getLogger(__name__)

class PlanMatcherAgent:
    """
    Plan matcher agent that uses OpenAI services to intelligently match
    user profiles with available insurance policies.
    
    This agent:
    - Analyzes user profile and requirements
    - Evaluates policy compatibility using AI
    - Ranks policies by match quality
    - Provides detailed matching insights
    """
    
    def __init__(self, openai_manager: OpenAIServiceManager = None):
        """
        Initialize the plan matcher agent.
        
        Args:
            openai_manager: OpenAI service manager instance
        """
        self.openai_manager = openai_manager or OpenAIServiceManager()
        self.analysis_service = self.openai_manager.policy_analysis
        
        logger.info("PlanMatcherAgent initialized with OpenAI services")
    
    async def run(self, profile: dict, available_plans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run plan matching analysis using OpenAI services.
        
        Args:
            profile: User profile and requirements
            available_plans: List of available insurance plans
            
        Returns:
            Dict containing matching results and analysis
        """
        try:
            logger.info(f"Starting plan matching for {len(available_plans)} plans")
            
            # Analyze each plan against the user profile
            matching_results = []
            
            for plan in available_plans:
                try:
                    # Use OpenAI service to analyze compatibility
                    analysis = await self.analysis_service.process(profile, plan)
                    
                    # Add plan information to results
                    matching_results.append({
                        "plan": plan,
                        "analysis": analysis,
                        "compatibility_score": analysis.get("compatibility_score", 0),
                        "recommendation": analysis.get("overall_recommendation", "Unable to determine"),
                        "key_factors": analysis.get("key_matching_factors", []),
                        "potential_issues": analysis.get("potential_issues", [])
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to analyze plan {plan.get('name', 'Unknown')}: {str(e)}")
                    # Add fallback result
                    matching_results.append({
                        "plan": plan,
                        "analysis": {"error": "Analysis failed"},
                        "compatibility_score": 0,
                        "recommendation": "Unable to analyze",
                        "key_factors": [],
                        "potential_issues": ["Analysis service unavailable"]
                    })
            
            # Sort results by compatibility score (highest first)
            matching_results.sort(key=lambda x: x["compatibility_score"], reverse=True)
            
            # Generate summary statistics
            summary = self._generate_matching_summary(matching_results)
            
            return {
                "status": "success",
                "total_plans_analyzed": len(available_plans),
                "matching_results": matching_results,
                "top_recommendations": matching_results[:3],  # Top 3 matches
                "summary": summary,
                "agent": "PlanMatcherAgent",
                "service_used": "OpenAI Policy Analysis"
            }
            
        except Exception as e:
            logger.error(f"Plan matching failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": "PlanMatcherAgent"
            }
    
    def _generate_matching_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for matching results."""
        if not results:
            return {"error": "No results to summarize"}
        
        # Extract scores for analysis
        scores = [r["compatibility_score"] for r in results]
        
        # Calculate statistics
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # Categorize recommendations
        excellent_matches = len([s for s in scores if s >= 80])
        good_matches = len([s for s in scores if 60 <= s < 80])
        poor_matches = len([s for s in scores if s < 60])
        
        return {
            "average_compatibility": round(avg_score, 2),
            "highest_score": max_score,
            "lowest_score": min_score,
            "score_distribution": {
                "excellent": excellent_matches,
                "good": good_matches,
                "poor": poor_matches
            },
            "recommendation_count": len([r for r in results if r["compatibility_score"] >= 70])
        }
    
    async def get_best_match(self, profile: dict, available_plans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get the single best matching plan for a user.
        
        Args:
            profile: User profile and requirements
            available_plans: List of available insurance plans
            
        Returns:
            Best matching plan with analysis
        """
        results = await self.run(profile, available_plans)
        
        if results["status"] == "success" and results["matching_results"]:
            best_match = results["matching_results"][0]  # Highest score
            return {
                "best_match": best_match,
                "confidence": best_match["analysis"].get("confidence_level", "Low"),
                "reasoning": best_match["key_factors"]
            }
        
        return {"error": "No suitable matches found"}
    
    async def filter_by_criteria(self, profile: dict, available_plans: List[Dict[str, Any]], 
                               min_score: int = 70) -> List[Dict[str, Any]]:
        """
        Filter plans by minimum compatibility score.
        
        Args:
            profile: User profile and requirements
            available_plans: List of available insurance plans
            min_score: Minimum compatibility score (0-100)
            
        Returns:
            List of plans meeting the minimum score
        """
        results = await self.run(profile, available_plans)
        
        if results["status"] == "success":
            filtered_plans = [
                r for r in results["matching_results"] 
                if r["compatibility_score"] >= min_score
            ]
            return filtered_plans
        
        return []
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent."""
        return {
            "agent_name": "PlanMatcherAgent",
            "version": "1.0.0",
            "capabilities": [
                "AI-powered policy compatibility analysis",
                "Multi-policy ranking and scoring",
                "Detailed matching insights",
                "Filtering by compatibility criteria"
            ],
            "openai_service": self.analysis_service.service_name if self.analysis_service else "Not available"
        }
