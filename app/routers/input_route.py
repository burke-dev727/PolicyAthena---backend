# Author: James Zheng
# Created: 7/20/2025
# Updated: 8/10/2025
# Description: Takes in API route from userinput route and sends it to input_interpreter
# Notes: Will need to move the saved files into DB
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models.input_models import UserProfileInput
from app.agents.input_interpreter import InputInterpreterAgent
from app.db.crud import save_userprofile_data, save_userinput_data
import os
import datetime

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Recieve the json_input
@app.post("/userInput/profile")
async def receive_user_input(request: Request):
    json_data = await request.json()
    source =json_data.get("source", "userinput")

    # Save JSON to file
    save_dir = "data/user_inputs"
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"userinput_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            import json
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
            "db_id": db_id,
            "data": result
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    