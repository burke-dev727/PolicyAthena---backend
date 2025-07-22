# app/db/create_tables.py
# Created by Xinrui Hou
# Date: 2025-07-22
from .session import engine
from .models import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created!")