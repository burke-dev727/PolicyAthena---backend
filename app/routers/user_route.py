from fastapi import APIRouter, Body
from app.agents.user_agent import UserAgent

router = APIRouter(prefix="/users", tags=["users"])
user_agent = UserAgent()

@router.post("/register")
async def register(data: dict = Body(...)):
    username = data.get("username")
    password = data.get("password")
    result = user_agent.register(username, password)
    return {"msg": result}

@router.post("/login")
async def login(data: dict = Body(...)):
    username = data.get("username")
    password = data.get("password")
    result = user_agent.login(username, password)
    return {"msg": result}
