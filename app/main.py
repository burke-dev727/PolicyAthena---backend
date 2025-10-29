# app/main.py
# Created by Xinrui Hou
# Date: 2025-08-10
# Updated: Added CORS middleware for React frontend integration
#          Restored all router endpoints for complete API functionality

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    user_route,
    input_route,
    plan_route,
    matcher_route,
    scorer_route,
    explanation_route,
    orchestrator_route
)

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="PolicyAthena Backend", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Create React App default port
        "http://localhost:3001",    # Alternative CRA port
        "http://localhost:5173",    # Vite default port (React app current port)
        "http://localhost:5174",    # Vite alternative port
        "http://localhost:8080",    # Common development port
        "http://127.0.0.1:5173",   # Vite with IP address
        "http://127.0.0.1:3000",   # CRA with IP address
    ],
    allow_credentials=True,        
    allow_methods=["*"],           # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Allow all request headers
)

# Router Configuration
# Include all agent and service routers for complete API functionality
# Each router provides specific endpoints for different business logic areas
app.include_router(user_route.router)       
app.include_router(input_route.router)     
app.include_router(plan_route.router)      
app.include_router(matcher_route.router)   
app.include_router(scorer_route.router)     
app.include_router(explanation_route.router) 
app.include_router(orchestrator_route.router) 

@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {"message": "PolicyAthena Backend API"}
