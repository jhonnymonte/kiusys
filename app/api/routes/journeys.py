from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.application.use_cases.search_journeys import SearchJourneysUseCase
from app.domain.ports import FlightEventsProvider
from app.schemas.response import JourneyResponse

router = APIRouter(prefix="/journeys", tags=["journeys"])

def get_flight_client(request: Request) -> FlightEventsProvider:
    return request.app.state.flight_client


@router.get(
    "/search",
    response_model=list[JourneyResponse],
    response_model_by_alias=True,
)
async def search_journeys(
    date: date = Query(..., description="Departure date (YYYY-MM-DD)"),
    from_:str = Query(
        ...,
        alias="from",
        min_length=3,
        max_length=3,
        description="Origin city code",
    ),
    to: str= Query(
        ...,
        min_length=3,
        max_length=3,
        description="Destination city code",  
    ),
    client: FlightEventsProvider = Depends(get_flight_client),
    
)-> list[JourneyResponse]:
    if from_.upper() == to.upper():
        raise HTTPException(status_code=400, detail="Origin and destination must differ")
    
    use_case = SearchJourneysUseCase(client)
    journeys = await use_case.execute(date, from_.upper(), to.upper())
    
    return [JourneyResponse.from_domain(journey) for journey in journeys]

