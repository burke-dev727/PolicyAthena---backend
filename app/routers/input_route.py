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

router = APIRouter()

# Receive the json_input
@router.post("/userInput/profile")
async def receive_user_input(request: Request):
    try:
        json_data = await request.json()
        source = json_data.get("source", "userinput")
        
        # Validate source
        if source not in ["userinput", "userprofile"]:
            raise HTTPException(status_code=400, detail="Invalid source. Must be 'userinput' or 'userprofile'")
        
        # Save JSON to appropriate directory based on source
        if source == "userprofile":
            save_dir = "data/user_profiles"
            filename_prefix = "userprofile"
        else:
            save_dir = "data/user_inputs"
            filename_prefix = "userinput"
        
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(save_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)
            file_saved = True
        except Exception as file_error:
            return {"success": False, "error": f"File save failed: {file_error}"}
        
        # Save to DB
        try:
            if source == "userprofile":
                db_id = save_userprofile_data(json_data)
            else:
                db_id = save_userinput_data(json_data)
        except Exception as db_error:
            return {"success": False, "error": f"DB save failed: {db_error}"}
        
        # Interpret the input using a custom agent
        try: 
            interpreter = InputInterpreterAgent()
            result = interpreter.run(json_data)
            return {
                "success": True,
                "file_saved": file_saved,
                "filename": filename,
                "filepath": filepath,
                "db_id": db_id,
                "source": source,
                "data": result
            }
        
        except Exception as e:
            return {"success": False, "error": f"Input interpretation failed: {str(e)}"}
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    