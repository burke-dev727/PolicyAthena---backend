# app/db/session.py
# Created by Xinrui Hou
# Date: 2025-07-22
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
            print("Database connected! Tables in public schema:")
            for row in result:
                print(row[0])
    except Exception as e:
        print("Database connection failed:", e)