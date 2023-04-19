from typing import Optional

from fastapi import APIRouter

from eventService.handler.eventHandler import EventHandler
from pydantic import BaseModel
from starlette.responses import JSONResponse

eventRoutes = APIRouter()

class CreateEventRequest(BaseModel):
    email: str
    start_time: str
    end_time: str
    title: str
    description: Optional[str] = None
    guests: Optional[str] = None
    room: str
    isStudent: bool

class FinalizeEventRequest(BaseModel):
    event: dict
    google_auth_token: str
    email: str

@eventRoutes.get("/")
async def root():
    return {"message": "Hello World"}

@eventRoutes.post("/events")
async def create_event(request: CreateEventRequest):
    try:
        return EventHandler().create_event(request)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

@eventRoutes.put("/events/finalize")
async def finalize_event(request: FinalizeEventRequest):
    try:
        drafts = EventHandler().finalize_event(request)
        return drafts
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
