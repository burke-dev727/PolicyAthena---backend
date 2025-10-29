# app/routers/explanation_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for intelligent policy explanations using OpenAI services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.agents.explanation import ExplanationAgent
from app.services.openai import OpenAIServiceManager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/explanation", tags=["explanation"])

class TopPlanData(BaseModel):
    """Top plan data for explanation generation."""
    plan: Dict[str, Any]
    analysis: Dict[str, Any]
    scoring: Dict[str, Any]

class ExplanationRequest(BaseModel):
    """Request for explanation generation."""
    top_plan: TopPlanData
    profile: Dict[str, Any]

class ExplanationResponse(BaseModel):
    """Response from explanation generation."""
    status: str
    plan_name: str
    explanation: Dict[str, Any]
    key_highlights: Dict[str, Any]
    agent: str
    services_used: list

@router.post("/explain", response_model=ExplanationResponse)
async def generate_explanation(request: ExplanationRequest):
    """
    Generate comprehensive explanation for the top recommended plan.
    
    This endpoint:
    - Explains why the plan was recommended
    - Provides personalized insights and reasoning
    - Generates actionable next steps
    - Creates comprehensive policy summary
    """
    try:
        logger.info("Starting explanation generation request")
        
        # Initialize the explanation agent
        openai_manager = OpenAIServiceManager()
        explainer = ExplanationAgent(openai_manager)
        
        # Convert Pydantic models to dictionaries
        top_plan = request.top_plan.dict()
        profile = request.profile
        
        # Run the explanation generation
        explanation_results = await explainer.run(top_plan, profile)
        
        if explanation_results["status"] == "success":
            logger.info(f"Successfully generated explanation for: {explanation_results['plan_name']}")
            return ExplanationResponse(**explanation_results)
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Explanation generation failed: {explanation_results.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Explanation generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain-simple")
async def generate_simple_explanation(plan: Dict[str, Any], profile: Dict[str, Any]):
    """
    Generate a simple explanation for testing purposes.
    
    This endpoint uses mock analysis and scoring data for demonstration.
    """
    try:
        # Create mock top plan data for testing
        mock_top_plan = {
            "plan": plan,
            "analysis": {
                "compatibility_score": 85,
                "key_matching_factors": ["Good coverage for your conditions", "Fits your budget"],
                "potential_issues": ["Limited network in rural areas"],
                "overall_recommendation": "Good match with minor concerns",
                "confidence_level": "High"
            },
            "scoring": {
                "overall_score": 87,
                "weighted_score": 85.5,
                "cost_score": 92,
                "coverage_score": 85,
                "network_score": 78,
                "preference_score": 89,
                "reasoning": {
                    "cost_score_reason": "Premium is within your budget range",
                    "coverage_score_reason": "Covers all your current conditions",
                    "network_score_reason": "Strong urban network, limited rural coverage",
                    "preference_score_reason": "Excellent match for your preferences"
                }
            }
        }
        
        # Initialize and run the explainer
        openai_manager = OpenAIServiceManager()
        explainer = ExplanationAgent(openai_manager)
        
        explanation_results = await explainer.run(mock_top_plan, profile)
        return explanation_results
        
    except Exception as e:
        logger.error(f"Simple explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent-info")
async def get_agent_info():
    """Get information about the explanation agent."""
    try:
        openai_manager = OpenAIServiceManager()
        explainer = ExplanationAgent(openai_manager)
        return explainer.get_agent_info()
    except Exception as e:
        logger.error(f"Agent info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
