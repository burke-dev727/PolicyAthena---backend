# app/routers/orchestrator_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for orchestrating the complete policy analysis workflow

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from app.agents.plan_matcher import PlanMatcherAgent
from app.agents.scorer import ScoringAgent
from app.agents.explanation import ExplanationAgent
from app.services.openai import OpenAIServiceManager
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])

class CompleteWorkflowRequest(BaseModel):
    """Request for complete policy analysis workflow."""
    user_profile: Dict[str, Any]
    available_plans: List[Dict[str, Any]]

class CompleteWorkflowResponse(BaseModel):
    """Response from complete workflow."""
    status: str
    workflow_steps: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    summary: Dict[str, Any]

@router.post("/complete-workflow", response_model=CompleteWorkflowResponse)
async def run_complete_workflow(request: CompleteWorkflowRequest):
    """
    Run the complete policy analysis workflow.
    
    This endpoint orchestrates all three agents:
    1. Plan Matcher - Analyzes compatibility
    2. Scorer - Provides quantitative evaluation
    3. Explanation - Generates comprehensive insights
    
    Returns the complete analysis pipeline results.
    """
    try:
        logger.info("Starting complete policy analysis workflow")
        
        # Initialize OpenAI service manager
        openai_manager = OpenAIServiceManager(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Step 1: Plan Matching
        logger.info("Step 1: Running Plan Matcher")
        plan_matcher = PlanMatcherAgent(openai_manager)
        matching_results = await plan_matcher.run(request.user_profile, request.available_plans)
        
        if matching_results["status"] != "success":
            raise HTTPException(status_code=500, detail=f"Plan matching failed: {matching_results.get('error')}")
        
        # Step 2: Policy Scoring
        logger.info("Step 2: Running Policy Scorer")
        scorer = ScoringAgent(openai_manager)
        scoring_results = await scorer.run(matching_results["matching_results"], request.user_profile)
        
        if scoring_results["status"] != "success":
            raise HTTPException(status_code=500, detail=f"Policy scoring failed: {scoring_results.get('error')}")
        
        # Step 3: Explanation Generation
        logger.info("Step 3: Running Explanation Generator")
        explainer = ExplanationAgent(openai_manager)
        
        # Get the top scored plan
        top_plan = {
            "plan": scoring_results["top_scored_plans"][0]["plan"],
            "analysis": scoring_results["top_scored_plans"][0]["analysis"],
            "scoring": scoring_results["top_scored_plans"][0]["scoring"]
        }
        
        explanation_results = await explainer.run(top_plan, request.user_profile)
        
        if explanation_results["status"] != "success":
            raise HTTPException(status_code=500, detail=f"Explanation generation failed: {explanation_results.get('error')}")
        
        # Compile complete workflow results
        workflow_steps = {
            "plan_matching": {
                "status": "completed",
                "total_plans_analyzed": matching_results["total_plans_analyzed"],
                "top_recommendations": matching_results["top_recommendations"][:3],
                "summary": matching_results["summary"]
            },
            "policy_scoring": {
                "status": "completed",
                "total_plans_scored": scoring_results["total_plans_scored"],
                "top_scored_plans": scoring_results["top_scored_plans"][:3],
                "summary": scoring_results["summary"]
            },
            "explanation": {
                "status": "completed",
                "plan_name": explanation_results["plan_name"],
                "key_highlights": explanation_results["key_highlights"]
            }
        }
        
        final_recommendation = {
            "best_plan": {
                "name": explanation_results["plan_name"],
                "compatibility_score": explanation_results["key_highlights"]["compatibility_score"],
                "overall_score": explanation_results["key_highlights"]["overall_score"],
                "recommendation_level": explanation_results["key_highlights"]["recommendation_level"]
            },
            "explanation": explanation_results["explanation"],
            "confidence": explanation_results["explanation"].get("key_benefits", [])
        }
        
        summary = {
            "total_plans_processed": len(request.available_plans),
            "workflow_duration": "completed",
            "ai_services_used": ["OpenAI Policy Analysis", "OpenAI Policy Scoring"],
            "final_decision": explanation_results["key_highlights"]["recommendation_level"]
        }
        
        logger.info("Complete workflow finished successfully")
        
        return CompleteWorkflowResponse(
            status="success",
            workflow_steps=workflow_steps,
            final_recommendation=final_recommendation,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Complete workflow error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-workflow")
async def test_complete_workflow():
    """
    Test the complete workflow with sample data.
    
    This endpoint demonstrates the full pipeline using mock data.
    Perfect for testing and demonstration purposes.
    """
    try:
        # Initialize OpenAI service manager
        openai_manager = OpenAIServiceManager(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Sample user profile
        user_profile = {
            "age": 35,
            "city": "Austin",
            "state": "TX",
            "monthly_budget": "$300-$500",
            "current_conditions": "diabetes, infection, cancer",
            "current_perscriptions": "metformin, omeprazole",
            "coverage_type": "Individual",
            "coverage_level": "Bronze"
        }
        
        # Sample available plans
        available_plans = [
            {
                "name": "Blue Cross Bronze HMO",
                "coverage": "Comprehensive health coverage with HMO network",
                "monthly_premium": "$350",
                "deductible": "$6,000",
                "network": "Large HMO network in Austin area",
                "restrictions": "Must use in-network providers"
            },
            {
                "name": "Aetna Silver PPO",
                "coverage": "Flexible PPO coverage with broader network",
                "monthly_premium": "$450",
                "deductible": "$4,000",
                "network": "Extensive PPO network across Texas",
                "restrictions": "Higher out-of-network costs"
            },
            {
                "name": "Cigna Bronze HDHP",
                "coverage": "High-deductible health plan with HSA",
                "monthly_premium": "$280",
                "deductible": "$7,000",
                "network": "National Cigna network",
                "restrictions": "High deductible, HSA-eligible"
            }
        ]
        
        # Run the complete workflow
        request = CompleteWorkflowRequest(
            user_profile=user_profile,
            available_plans=available_plans
        )
        
        return await run_complete_workflow(request)
        
    except Exception as e:
        logger.error(f"Test workflow error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow-status")
async def get_workflow_status():
    """Get the current status of the workflow system."""
    try:
        # Initialize OpenAI service manager
        openai_manager = OpenAIServiceManager(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Get basic service information without health checks
        service_info = openai_manager.get_service_info()
        manager_info = openai_manager.get_manager_info()
        
        return {
            "system_status": "operational",
            "openai_services": {
                "total_services": service_info["total_services"],
                "available_services": manager_info["available_services"],
                "api_key_configured": manager_info["api_key_configured"]
            },
            "available_agents": [
                "PlanMatcherAgent",
                "ScoringAgent", 
                "ExplanationAgent"
            ],
            "workflow_capabilities": [
                "AI-powered policy matching",
                "Quantitative policy scoring",
                "Intelligent explanation generation",
                "Complete end-to-end analysis"
            ],
            "note": "Status check performed without API calls to ensure stability"
        }
        
    except Exception as e:
        logger.error(f"Workflow status error: {str(e)}")
        return {
            "system_status": "error",
            "error": str(e)
        }
