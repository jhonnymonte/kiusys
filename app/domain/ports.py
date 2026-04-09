from typing import Protocol

from app.domain.entities import FlightEvent


class FlightEventsProvider(Protocol):
    """
    Port (interface) for retrieving flight events.

    Allows the use case to be decoupled from the client's specific implementation
    (HTTP, cache, mock, etc.).
    """

    async def get_events(self) -> list[FlightEvent]:
        """
        Retrieves all available flight events from the data source.

        Returns:
            list[FlightEvent]: a list of flight events that have already been parsed into the domain.
        """
        ...
