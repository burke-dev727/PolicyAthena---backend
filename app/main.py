from fastapi import FastAPI
from app.routers import (
    input_route,
    profile_route,
    matcher_route,
    scorer_route,
    explanation_route,
    orchestrator_route
)

app = FastAPI(title="PolicyAthena Backend")

# Include each agent's router
app.include_router(input_route.router)
app.include_router(profile_route.router)
app.include_router(matcher_route.router)
app.include_router(scorer_route.router)
app.include_router(explanation_route.router)
app.include_router(orchestrator_route.router)
