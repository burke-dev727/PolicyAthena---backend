# app/db/crud.py
# Created by Xinrui Hou
# Date: 2025-07-22
from .session import SessionLocal
from .models import UserProfile

def save_user_profile(profile_data: dict):
    db = SessionLocal()
    user_profile = UserProfile(data=profile_data)
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    db.close()
    return user_profile.id


