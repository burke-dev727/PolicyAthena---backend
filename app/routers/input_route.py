from fastapi import APIRouter
from app.models.input_models import UserProfileInput
from app.agents.input_interpreter import InputInterpreterAgent
from app.db.crud import save_user_profile
from app.services.user_input import user_input

router = APIRouter(prefix="/userInput", tags=["userInput"])

@router.post("/profile")
async def process_user_profile(data: UserProfileInput):
    try:
        interpreter = InputInterpreterAgent()
        parsed_profile = interpreter.run(data.dict())
        profile_id = user_input(parsed_profile)
        return {
            "message": "Profile received and stored.",
            "profile_id": profile_id,
            "parsed_profile": parsed_profile
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}
