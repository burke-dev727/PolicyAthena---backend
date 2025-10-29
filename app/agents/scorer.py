# app/agents/scorer.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: Scoring agent using OpenAI services for quantitative policy evaluation

import logging
from typing import Dict, List, Any
from app.services.openai import OpenAIServiceManager

logger = logging.getLogger(__name__)

class ScoringAgent:
    """
    Scoring agent that uses OpenAI services to provide quantitative
    evaluation of insurance policies.
    
    This agent:
    - Generates numerical scores for policies
    - Evaluates cost-benefit ratios
    - Assesses network and coverage quality
    - Provides weighted scoring with reasoning
    """
    
    def __init__(self, openai_manager: OpenAIServiceManager = None):
        """
        Initialize the scoring agent.
        
        Args:
            openai_manager: OpenAI service manager instance
        """
        self.openai_manager = openai_manager or OpenAIServiceManager()
        self.scoring_service = self.openai_manager.policy_scoring
        
        logger.info("ScoringAgent initialized with OpenAI services")
    
    async def run(self, matched_plans: List[Dict[str, Any]], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run scoring analysis on matched plans using OpenAI services.
        
        Args:
            matched_plans: List of plans from plan matcher
            user_profile: User profile and requirements
            
        Returns:
            Dict containing scoring results and rankings
        """
        try:
            logger.info(f"Starting scoring analysis for {len(matched_plans)} plans")
            
            # Score each plan
            scoring_results = []
            
            for plan_data in matched_plans:
                try:
                    plan = plan_data.get("plan", {})
                    analysis = plan_data.get("analysis", {})
                    
                    # Use OpenAI service to generate scoring
                    scoring = await self.scoring_service.process(user_profile, plan, analysis)
                    
                    # Combine plan, analysis, and scoring data
                    scoring_results.append({
                        "plan": plan,
                        "analysis": analysis,
                        "scoring": scoring,
                        "overall_score": scoring.get("overall_score", 0),
                        "weighted_score": scoring.get("weighted_score", 0),
                        "cost_score": scoring.get("cost_score", 0),
                        "coverage_score": scoring.get("coverage_score", 0),
                        "network_score": scoring.get("network_score", 0),
                        "preference_score": scoring.get("preference_score", 0)
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to score plan {plan.get('name', 'Unknown')}: {str(e)}")
                    # Add fallback scoring
                    scoring_results.append({
                        "plan": plan,
                        "analysis": analysis,
                        "scoring": {"error": "Scoring failed"},
                        "overall_score": 0,
                        "weighted_score": 0,
                        "cost_score": 0,
                        "coverage_score": 0,
                        "network_score": 0,
                        "preference_score": 0
                    })
            
            # Sort by weighted score (highest first)
            scoring_results.sort(key=lambda x: x["weighted_score"], reverse=True)
            
            # Generate scoring summary
            summary = self._generate_scoring_summary(scoring_results)
            
            # Categorize plans by score ranges
            categorized_plans = self._categorize_plans_by_score(scoring_results)
            
            return {
                "status": "success",
                "total_plans_scored": len(matched_plans),
                "scoring_results": scoring_results,
                "top_scored_plans": scoring_results[:3],  # Top 3 by score
                "summary": summary,
                "categorized_plans": categorized_plans,
                "agent": "ScoringAgent",
                "service_used": "OpenAI Policy Scoring"
            }
            
        except Exception as e:
            logger.error(f"Scoring analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": "ScoringAgent"
            }
    
    def _generate_scoring_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for scoring results."""
        if not results:
            return {"error": "No results to summarize"}
        
        # Extract scores for analysis
        overall_scores = [r["overall_score"] for r in results]
        weighted_scores = [r["weighted_score"] for r in results]
        cost_scores = [r["cost_score"] for r in results]
        coverage_scores = [r["coverage_score"] for r in results]
        network_scores = [r["network_score"] for r in results]
        
        return {
            "score_averages": {
                "overall": round(sum(overall_scores) / len(overall_scores), 2),
                "weighted": round(sum(weighted_scores) / len(weighted_scores), 2),
                "cost": round(sum(cost_scores) / len(cost_scores), 2),
                "coverage": round(sum(coverage_scores) / len(coverage_scores), 2),
                "network": round(sum(network_scores) / len(network_scores), 2)
            },
            "score_ranges": {
                "overall": {"min": min(overall_scores), "max": max(overall_scores)},
                "weighted": {"min": min(weighted_scores), "max": max(weighted_scores)}
            },
            "top_performers": {
                "highest_overall": max(overall_scores),
                "highest_weighted": max(weighted_scores),
                "best_cost": max(cost_scores),
                "best_coverage": max(coverage_scores),
                "best_network": max(network_scores)
            }
        }
    
    def _categorize_plans_by_score(self, results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize plans by their scoring performance."""
        categories = {
            "excellent": [],      # 90-100
            "very_good": [],      # 80-89
            "good": [],           # 70-79
            "fair": [],           # 60-69
            "poor": []            # Below 60
        }
        
        for result in results:
            score = result["weighted_score"]
            
            if score >= 90:
                categories["excellent"].append(result)
            elif score >= 80:
                categories["very_good"].append(result)
            elif score >= 70:
                categories["good"].append(result)
            elif score >= 60:
                categories["fair"].append(result)
            else:
                categories["poor"].append(result)
        
        return categories
    
    async def score_single_plan(self, user_profile: Dict[str, Any], plan: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a single plan.
        
        Args:
            user_profile: User profile and requirements
            plan: Plan details to score
            analysis: Analysis results for the plan
            
        Returns:
            Scoring results for the single plan
        """
        try:
            scoring = await self.scoring_service.process(user_profile, plan, analysis)
            
            return {
                "plan": plan,
                "analysis": analysis,
                "scoring": scoring,
                "overall_score": scoring.get("overall_score", 0),
                "weighted_score": scoring.get("weighted_score", 0),
                "detailed_scores": {
                    "cost": scoring.get("cost_score", 0),
                    "coverage": scoring.get("coverage_score", 0),
                    "network": scoring.get("network_score", 0),
                    "preference": scoring.get("preference_score", 0)
                },
                "reasoning": scoring.get("reasoning", {}),
                "improvement_suggestions": scoring.get("improvement_suggestions", [])
            }
            
        except Exception as e:
            logger.error(f"Single plan scoring failed: {str(e)}")
            return {
                "plan": plan,
                "error": str(e),
                "overall_score": 0,
                "weighted_score": 0
            }
    
    async def compare_plans(self, user_profile: Dict[str, Any], plans: List[Dict[str, Any]], 
                           analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple plans side by side.
        
        Args:
            user_profile: User profile and requirements
            plans: List of plans to compare
            analyses: List of analysis results for each plan
            
        Returns:
            Comparison results
        """
        try:
            comparison_results = []
            
            for i, (plan, analysis) in enumerate(zip(plans, analyses)):
                scoring = await self.scoring_service.process(user_profile, plan, analysis)
                comparison_results.append({
                    "plan_index": i,
                    "plan_name": plan.get("name", f"Plan {i+1}"),
                    "scores": {
                        "overall": scoring.get("overall_score", 0),
                        "weighted": scoring.get("weighted_score", 0),
                        "cost": scoring.get("cost_score", 0),
                        "coverage": scoring.get("coverage_score", 0),
                        "network": scoring.get("network_score", 0)
                    },
                    "analysis": analysis,
                    "scoring": scoring
                })
            
            # Sort by weighted score
            comparison_results.sort(key=lambda x: x["scores"]["weighted"], reverse=True)
            
            return {
                "status": "success",
                "comparison_results": comparison_results,
                "winner": comparison_results[0] if comparison_results else None,
                "total_plans": len(plans)
            }
            
        except Exception as e:
            logger.error(f"Plan comparison failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent."""
        return {
            "agent_name": "ScoringAgent",
            "version": "1.0.0",
            "capabilities": [
                "AI-powered quantitative scoring",
                "Multi-dimensional evaluation (cost, coverage, network, preference)",
                "Weighted scoring with configurable weights",
                "Plan comparison and ranking",
                "Detailed scoring reasoning"
            ],
            "openai_service": self.scoring_service.service_name if self.scoring_service else "Not available",
            "scoring_weights": self.scoring_service.scoring_weights if self.scoring_service else {}
        }
