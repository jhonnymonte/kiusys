from datetime import date
from app.domain.entities import Journey
from app.domain.ports import FlightEventsProvider
from app.domain.rules import is_valid_connection
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class SearchJourneysUseCase:
    def __init__(self, client: FlightEventsProvider) -> None:
        self._client = client
        
    
    async def execute(self, search_date: date, origin:str, destination:str ) -> list[Journey]:
        logger.info(
            "Searching journeys",
            extra={
                "date": str(search_date),
                "origin": origin,
                "destination": destination,
            },
        )
        
        all_events = await self._client.get_events()
        #leg 1 always start for the search date
        departing = [e for e in all_events if e.departure_datetime.date() == search_date]
        
        journeys: list[Journey] = []
        
        #direct fly
        for event in departing:
            if event.departure_city == origin  and event.arrival_city == destination:
                journeys.append(Journey(path=[event]))
        
        #conections
        by_departure: dict[str, list] = {}
        for event in all_events:
            by_departure.setdefault(event.departure_city, []).append(event)
            
        for leg1 in departing:
            if leg1.departure_city != origin:
                continue
            
            for leg2 in by_departure.get(leg1.arrival_city,[]):
                if is_valid_connection(leg1, leg2, destination):
                    journeys.append(Journey(path=[leg1,leg2]))
        
        logger.info("Seach complete", extra={"results":len(journeys)})
        return journeys