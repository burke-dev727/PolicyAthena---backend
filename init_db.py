#!/usr/bin/env python3
"""
Database initialization script
Creates all tables defined in the models
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.session import engine
from app.db.models import Base

def init_database():
    """Initialize the database by creating all tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # List all tables
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"))
            print("\nTables created:")
            for row in result:
                print(f"  - {row[0]}")
                
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("PolicyAthena Database Initialization")
    print("=" * 40)
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL environment variable not set!")
        print("Please create a .env file with your database connection string.")
        sys.exit(1)
    
    success = init_database()
    
    if success:
        print("\n🎉 Database initialization completed successfully!")
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1)
