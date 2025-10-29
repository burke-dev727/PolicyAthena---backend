# app/routers/matcher_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for intelligent policy matching using OpenAI services

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.agents.plan_matcher import PlanMatcherAgent
from app.services.openai import OpenAIServiceManager
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/policyMatcher", tags=["policyMatcher"])

class ProfileData(BaseModel):
    """User profile data for policy matching."""
    age: Optional[int] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    preferences: Optional[List[str]] = None
    monthly_budget: Optional[str] = None
    current_conditions: Optional[str] = None
    current_perscriptions: Optional[str] = None
    coverage_type: Optional[str] = None
    coverage_level: Optional[str] = None
    # Add other fields from your userInput data structure
    have_insurance: Optional[bool] = False
    insurance_provider: Optional[str] = None
    source: Optional[str] = None
    providers: Optional[str] = None
    is_us_citizen: Optional[bool] = False
    is_medicaid: Optional[bool] = False
    is_medicare: Optional[bool] = False
    is_veteran: Optional[bool] = False
    is_student_eligible: Optional[bool] = False

class PolicyData(BaseModel):
    """Policy data for matching."""
    name: str
    coverage: str
    monthly_premium: str
    deductible: str
    network: str
    restrictions: Optional[str] = None

class MatchingRequest(BaseModel):
    """Request for policy matching."""
    profile: ProfileData
    available_plans: List[PolicyData]

class MatchingResponse(BaseModel):
    """Response from policy matching."""
    status: str
    total_plans_analyzed: int
    top_recommendations: List[Dict[str, Any]]
    summary: Dict[str, Any]
    agent: str
    service_used: str

@router.post("/match", response_model=MatchingResponse)
async def match_plans(request: MatchingRequest):
    """
    Match user profile with available insurance policies using AI.
    
    This endpoint:
    - Analyzes user profile and requirements
    - Evaluates policy compatibility using OpenAI
    - Ranks policies by match quality
    - Returns top recommendations with detailed analysis
    """
    try:
        logger.info("Starting policy matching request")
        
        # Initialize the plan matcher agent
        openai_manager = OpenAIServiceManager()
        plan_matcher = PlanMatcherAgent(openai_manager)
        
        # Convert Pydantic models to dictionaries
        profile_dict = request.profile.dict()
        plans_dict = [plan.dict() for plan in request.available_plans]
        
        # Run the matching analysis
        matching_results = await plan_matcher.run(profile_dict, plans_dict)
        
        if matching_results["status"] == "success":
            logger.info(f"Successfully matched {matching_results['total_plans_analyzed']} plans")
            return MatchingResponse(**matching_results)
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Matching failed: {matching_results.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Policy matching error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match-simple")
async def match_plans_simple(profile: ProfileData):
    """
    Simple policy matching with mock data for testing.
    
    This endpoint uses sample policy data to demonstrate the matching functionality.
    """
    try:
        # Sample policy data for testing
        sample_plans = [
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
        
        # Initialize and run the matcher
        openai_manager = OpenAIServiceManager()
        plan_matcher = PlanMatcherAgent(openai_manager)
        
        profile_dict = profile.dict()
        matching_results = await plan_matcher.run(profile_dict, sample_plans)
        
        return matching_results
        
    except Exception as e:
        logger.error(f"Simple matching error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent-info")
async def get_agent_info():
    """Get information about the plan matcher agent."""
    try:
        openai_manager = OpenAIServiceManager()
        plan_matcher = PlanMatcherAgent(openai_manager)
        return plan_matcher.get_agent_info()
    except Exception as e:
        logger.error(f"Agent info error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
