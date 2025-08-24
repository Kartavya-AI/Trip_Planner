from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import app
import os
import uvicorn

# Define request schema
class TripRequest(BaseModel):
    origin: str
    destination: str
    travel_date: str
    days: int
    interests: str | None = None
    accommodation_budget: str | None = None
    dietary_preferences: str | None = None
    food_budget: str | None = None

# Response schema
class TripResponse(BaseModel):
    finder_results: str | None = None
    itinerary: str | None = None
    errors: str | None = None

# Initialize FastAPI app
fastapi_app = FastAPI(title="🚗 Road Trip Planner API")

last_result: dict | None = None

@fastapi_app.get("/")   # root URL
def root():
    return {"message": "Road trip planner!"}

@fastapi_app.post("/plan_trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):

    global last_result
    try:
        # Convert request to state dict
        state = request.dict()

        # Run graph pipeline
        result = app.invoke(state)
        last_result = result

        return {
            "finder_results": result.get("finder_results"),
            "itinerary": result.get("itinerary"),
            #"errors": result.get("errors")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=='__main__':
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app:fastapi_app", host="0.0.0.0", port=port)
