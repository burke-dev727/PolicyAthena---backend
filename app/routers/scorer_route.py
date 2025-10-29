# app/routers/scorer_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for intelligent policy scoring using OpenAI services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.agents.scorer import ScoringAgent
from app.services.openai import OpenAIServiceManager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/planScorer", tags=["planScorer"])

class PlanData(BaseModel):
    """Plan data for scoring."""
    plan: Dict[str, Any]
    analysis: Dict[str, Any]

class ScoringRequest(BaseModel):
    """Request for plan scoring."""
    matched_plans: List[PlanData]
    user_profile: Dict[str, Any]

class ScoringResponse(BaseModel):
    """Response from plan scoring."""
    status: str
    total_plans_scored: int
    top_scored_plans: List[Dict[str, Any]]
    summary: Dict[str, Any]
    categorized_plans: Dict[str, List[Dict[str, Any]]]
    agent: str
    service_used: str

@router.post("/score", response_model=ScoringResponse)
async def score_plans(request: ScoringRequest):
    """
    Score matched plans using AI-powered evaluation.
    
    This endpoint:
    - Evaluates plans based on user profile and analysis
    - Generates quantitative scores for multiple dimensions
    - Provides weighted scoring with detailed reasoning
    - Categorizes plans by performance
    """
    try:
        logger.info("Starting plan scoring request")
        
        # Initialize the scoring agent
        openai_manager = OpenAIServiceManager()
        scorer = ScoringAgent(openai_manager)
        
        # Convert Pydantic models to dictionaries
        matched_plans = [plan.dict() for plan in request.matched_plans]
        user_profile = request.user_profile
        
        # Run the scoring analysis
        scoring_results = await scorer.run(matched_plans, user_profile)
        
        if scoring_results["status"] == "success":
            logger.info(f"Successfully scored {scoring_results['total_plans_scored']} plans")
            return ScoringResponse(**scoring_results)
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Scoring failed: {scoring_results.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Plan scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score-single")
async def score_single_plan(plan_data: PlanData, user_profile: Dict[str, Any]):
    """
    Score a single plan.
    
    This endpoint provides detailed scoring for one specific plan.
    """
    try:
        openai_manager = OpenAIServiceManager()
        scorer = ScoringAgent(openai_manager)
        
        plan_dict = plan_data.dict()
        scoring_result = await scorer.score_single_plan(
            user_profile, 
            plan_dict["plan"], 
            plan_dict["analysis"]
        )
        
        return scoring_result
        
    except Exception as e:
        logger.error(f"Single plan scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_plans(plans: List[Dict[str, Any]], analyses: List[Dict[str, Any]], user_profile: Dict[str, Any]):
    """
    Compare multiple plans side by side.
    
    This endpoint provides a detailed comparison of multiple plans.
    """
    try:
        openai_manager = OpenAIServiceManager()
        scorer = ScoringAgent(openai_manager)
        
        comparison_result = await scorer.compare_plans(user_profile, plans, analyses)
        return comparison_result
        
    except Exception as e:
        logger.error(f"Plan comparison error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent-info")
async def get_agent_info():
    """Get information about the scoring agent."""
    try:
        openai_manager = OpenAIServiceManager()
        scorer = ScoringAgent(openai_manager)
        return scorer.get_agent_info()
    except Exception as e:
        logger.error(f"Agent info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
