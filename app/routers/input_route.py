# Author: James Zheng
# Created: 7/20/2025
# Updated: 8/10/2025
# Description: Takes in API route from userinput route and sends it to input_interpreter
# Notes: Will need to move the saved files into DB
#   - Modifed the source variable to be 'userinput' or 'userprofile'
#   - Saved the JSON file to the appropriate directory based on the source
#   - Saved the JSON file to the DB based on the source
#   - Interpreted the input using a custom agent
#   - Returned the result to the frontend
#   - Returned the success status, file_saved, filename, filepath, db_id, source, and data to the frontend
#   - Added error handling for JSON decode error and other exceptions
#   - Changed the input route to be '/userInput/profile' and removed the '/userInput' part
from fastapi import APIRouter, Request, HTTPException
from app.agents.input_interpreter import InputInterpreterAgent
from app.db.crud import save_userprofile_data, save_userinput_data
import os
import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Receive the json_input
@router.post("/userInput/profile")
async def receive_user_input(request: Request):
    try:
        logger.info("=== Starting new data submission ===")
        json_data = await request.json()
        source = json_data.get("source", "userinput")
        
        logger.info(f"Received data from source: {source}")
        logger.info(f"Data keys: {list(json_data.keys())}")
        
        # Validate source
        if source not in ["userinput", "userprofile"]:
            logger.error(f"Invalid source: {source}")
            raise HTTPException(status_code=400, detail="Invalid source. Must be 'userinput' or 'userprofile'")
        
        # Save JSON to appropriate directory based on source
        if source == "userprofile":
            save_dir = "data/user_profiles"
            filename_prefix = "userprofile"
        else:
            save_dir = "data/user_inputs"
            filename_prefix = "userinput"
        
        logger.info(f"Saving to directory: {save_dir}")
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(save_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)
            file_saved = True
            logger.info(f"File saved successfully: {filepath}")
        except Exception as file_error:
            logger.error(f"File save failed: {file_error}")
            return {"success": False, "error": f"File save failed: {file_error}"}
        
        # Save to DB
        try:
            logger.info("Starting database save operation...")
            if source == "userprofile":
                logger.info("Saving UserProfile data to database...")
                db_id = save_userprofile_data(json_data)
                logger.info(f"UserProfile saved to database with ID: {db_id}")
            else:
                logger.info("Saving UserInput data to database...")
                db_id = save_userinput_data(json_data)
                logger.info(f"UserInput saved to database with ID: {db_id}")
        except Exception as db_error:
            logger.error(f"Database save failed: {db_error}")
            return {"success": False, "error": f"DB save failed: {db_error}"}
        
        # Interpret the input using a custom agent
        try: 
            logger.info("Starting input interpretation...")
            interpreter = InputInterpreterAgent()
            result = interpreter.run(json_data)
            logger.info("Input interpretation completed successfully")
            
            response_data = {
                "success": True,
                "file_saved": file_saved,
                "filename": filename,
                "filepath": filepath,
                "db_id": db_id,
                "source": source,
                "data": result
            }
            
            logger.info("=== Data submission completed successfully ===")
            logger.info(f"Response: {response_data}")
            
            return response_data
        
        except Exception as e:
            logger.error(f"Input interpretation failed: {str(e)}")
            return {"success": False, "error": f"Input interpretation failed: {str(e)}"}
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    