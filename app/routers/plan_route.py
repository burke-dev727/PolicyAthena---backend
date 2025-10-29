# app/routers/plan_route.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Purpose: API endpoints for plan building and extraction
#          Basic PDF upload and parsing functionality

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.agents.plan_builder import PlanBuilderAgent
from app.services.plan_extract import extract_plan_fields

router = APIRouter(prefix="/planBuilder", tags=["planBuilder"])
UPLOAD_TEMP = "temp_uploads"
os.makedirs(UPLOAD_TEMP, exist_ok=True)

@router.post("/upload")
async def upload_plan(file: UploadFile = File(...)):
    try:
        # Initialize plan builder agent with enhanced extraction
        agent = PlanBuilderAgent()
        
        # Save uploaded file temporarily
        file_location = os.path.join(UPLOAD_TEMP, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Extract plan name from filename
        plan_name = os.path.splitext(file.filename)[0]
        
        # Parse and save plan data with enhanced extraction
        plan_data = await agent.parseAnd_save(file_location, plan_name)
        
        # Clean up temporary file
        os.remove(file_location)
        
        return {
            "message": "Plan uploaded and parsed successfully with enhanced extraction",
            "plan_name": plan_name,
            "document_type": plan_data.extracted_data.get("metadata", {}).get("document_type", "unknown") if plan_data.extracted_data else "unknown",
            "plan_data": plan_data.dict() if hasattr(plan_data, 'dict') else str(plan_data)
        }
        
    except Exception as e:
        # Clean up file on error
        if 'file_location' in locals() and os.path.exists(file_location):
            os.remove(file_location)
        
        raise HTTPException(status_code=500, detail=f"Failed to process plan: {str(e)}")

@router.get("/{plan_name}")
async def get_plan(plan_name: str):
    """
    Retrieve a saved plan by name.
    
    Args:
        plan_name: Name of the plan to retrieve
        
    Returns:
        PlanData object with parsed information
    """
    try:
        # Initialize plan builder agent
        agent = PlanBuilderAgent()
        
        # Get the plan
        plan_data = agent.get_plan(plan_name)
        
        return {
            "plan_name": plan_name,
            "plan_data": plan_data.dict() if hasattr(plan_data, 'dict') else str(plan_data)
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Plan '{plan_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve plan: {str(e)}")

@router.get("/")
async def list_plans():
    """
    List all available plans.
    
    Returns:
        List of plan names and basic information
    """
    try:
        agent = PlanBuilderAgent()
        available_plans = agent.list_available_plans()
        
        return {
            "total_plans": len(available_plans),
            "available_plans": available_plans
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list plans: {str(e)}")

@router.post("/extract-details/{plan_name}")
async def extract_plan_details(plan_name: str):
    """
    Extract detailed plan information from an existing parsed plan.
    
    This endpoint:
    1. Takes an existing plan name
    2. Extracts comprehensive data from the parsed text
    3. Updates the plan with extracted information
    4. Returns the detailed extracted data
    
    Args:
        plan_name: Name of the existing plan
        
    Returns:
        Dict containing the extracted detailed plan information
    """
    try:
        agent = PlanBuilderAgent()
        extracted_data = agent.extract_detailed_data(plan_name)
        
        return {
            "message": f"Successfully extracted detailed data for plan: {plan_name}",
            "plan_name": plan_name,
            "extracted_data": extracted_data
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Plan '{plan_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract plan details: {str(e)}")

@router.get("/details/{plan_name}")
async def get_plan_details(plan_name: str):
    """
    Get a plan with comprehensive extracted information.
    
    This endpoint:
    1. Retrieves the basic plan data
    2. Automatically extracts detailed information if not already available
    3. Returns both basic and extracted data
    
    Args:
        plan_name: Name of the plan to retrieve
        
    Returns:
        Dict containing plan data and extracted details
    """
    try:
        agent = PlanBuilderAgent()
        plan_with_details = agent.get_plan_with_details(plan_name)
        
        return plan_with_details
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Plan '{plan_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get plan details: {str(e)}")

@router.post("/test-extraction")
async def test_enhanced_extraction(text_content: str):
    """
    Test the enhanced extraction with sample text content.
    
    This endpoint:
    1. Accepts text content (can be copied from a plan document)
    2. Tests the enhanced extraction capabilities
    3. Returns extraction results and document type detection
    
    Args:
        text_content: Text content to test extraction
        
    Returns:
        Dict containing extraction test results
    """
    try:
        from app.services.plan_extractor import PlanExtractor
        
        # Initialize the enhanced extractor
        extractor = PlanExtractor()
        
        # Test extraction with the provided text
        test_results = extractor.test_extraction_with_sample_data(text_content)
        
        # Generate a summary
        summary = extractor.get_extraction_summary(test_results)
        
        return {
            "message": "Enhanced extraction test completed",
            "test_results": test_results,
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test extraction: {str(e)}")



@router.get("/plans/{plan_name}")
def get_plan(plan_name: str):
    try:
        # Initialize plan builder agent
        agent = PlanBuilderAgent()
        plan = agent.get_plan(plan_name)
        return plan.model_dump()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get plan: {str(e)}")

# ✅ NEW: return the compact summary JSON for a saved plan
@router.get("/plans/{plan_name}/summary")
def get_plan_summary(plan_name: str):
    try:
        # Initialize plan builder agent
        agent = PlanBuilderAgent()
        summary = agent.summarize(plan_name)
        return {"plan_name": plan_name, "summary": summary}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get plan summary: {str(e)}")