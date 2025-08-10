# Author: James Zheng
# Created: 7/20/2025
# Updated: 8/10/2025
# Description: Takes in API route from userinput route and sends it to input_interpreter
# Notes: Will need to move the saved files into DB
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models.input_models import UserProfileInput
from app.agents.input_interpreter import InputInterpreterAgent
from app.db.crud import save_user_profile
from app.services.user_input import user_input
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
    
    # Interpret the input using a custom agent
    try: 
        interpreter = InputInterpreterAgent()
        result = interpreter.run(json_data)
        return {
            "success": True,
            "file_saved": file_saved,
            "filename": filename,
            "data": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    