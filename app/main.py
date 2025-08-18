from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    input_route,
    # profile_route,
    matcher_route,
    scorer_route,
    explanation_route,
    orchestrator_route
)
from app.routers import contact_route

app = FastAPI(title="PolicyAthena Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include each agent's router
app.include_router(input_route.router)
# app.include_router(profile_route.router)
app.include_router(matcher_route.router)
app.include_router(scorer_route.router)
app.include_router(explanation_route.router)
app.include_router(orchestrator_route.router)
app.include_router(contact_route.router)