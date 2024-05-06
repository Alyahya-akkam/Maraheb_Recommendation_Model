from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from recommendation import predicting

class EventInformation(BaseModel):
    title: str
    category: str
    type: str
    price: float
    description: str
    frequency: str
    organizerId: int
    start_date: date
    end_date: date
    event_id: int


class SeekerInformation(BaseModel):
    seeker_id: int
    gender: str
    category_list: list[str]
    dob: date


class RecommendationInformation(BaseModel):
    events: list[EventInformation]
    seeker: SeekerInformation


class GetTenEventsIds(BaseModel):
    events: list[int]


router = APIRouter(prefix="/recommendation")


@router.post("/", response_model=GetTenEventsIds)
def recommendation(recommendationInfo: RecommendationInformation):
    tenIds = predicting(recommendationInfo.seeker, recommendationInfo.events)
    print(tenIds)
    return GetTenEventsIds(events=tenIds)