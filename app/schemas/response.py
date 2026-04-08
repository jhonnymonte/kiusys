from pydantic import BaseModel, Field
from app.domain.entities import FlightEvent, Journey

class SegmentResponse(BaseModel):
    flight_number: str
    from_city: str = Field(serialization_alias="from")
    to_city: str=Field(serialization_alias="to")
    departure_time:str
    arrival_time:str
    
    model_config = {"populate_by_name":True}
    
    @classmethod
    def from_domain(cls, event:FlightEvent) -> "SegmentResponse":
        return cls(
            flight_number=event.flight_number,
            from_city=event.departure_city,
            to_city=event.arrival_city,
            departure_time=event.departure_datetime.strftime("%Y-%m-%d %H:%M"),
            arrival_time=event.arrival_datetime.strftime("%Y-%m-%d %H:%M"),
        )
        
class JourneyResponse(BaseModel):
    connections:int
    path:list[SegmentResponse]
    
    @classmethod
    def from_domain(cls, journey: Journey)-> "JourneyResponse":
        return cls(
            connections=journey.connections,
            path=[SegmentResponse.from_domain(event)for event in journey.path]
        )