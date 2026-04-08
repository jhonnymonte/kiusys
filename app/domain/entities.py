from dataclasses import dataclass
from datetime import datetime

@dataclass
class FlightEvent:
    flight_number: str
    departure_city: str
    arrival_city:str
    departure_datetime: datetime
    arrival_datetime: datetime
    
    def __post_init__(self):
        if self.departure_datetime >= self.arrival_datetime:
            raise ValueError(
                f"Flight event {self.flight_number}: departure must be before arrival"
                f"({self.departure_datetime} >= {self.arrival_datetime})"
            )
    
@dataclass
class Journey:
    path: list[FlightEvent]
    
    @property
    def connections(self) -> int:
        return len(self.path)