from abc import ABC, abstractmethod

from Vehicle import Vehicle


class SearchStrategy(ABC):
    """Strategy for deciding whether a parked vehicle matches a query.

    Collapses the eight near-identical `getSlotNumFromX` / `getRegNumFromX`
    methods in the original ParkingLot into one `find_slots(strategy)` call.
    """

    @abstractmethod
    def matches(self, vehicle: Vehicle) -> bool:
        """Return True if the vehicle satisfies this search."""


class MatchByColor(SearchStrategy):
    def __init__(self, color: str) -> None:
        self._color = color

    def matches(self, vehicle: Vehicle) -> bool:
        return vehicle.color == self._color


class MatchByMake(SearchStrategy):
    def __init__(self, make: str) -> None:
        self._make = make

    def matches(self, vehicle: Vehicle) -> bool:
        return vehicle.make == self._make


class MatchByModel(SearchStrategy):
    def __init__(self, model: str) -> None:
        self._model = model

    def matches(self, vehicle: Vehicle) -> bool:
        return vehicle.model == self._model


class MatchByRegnum(SearchStrategy):
    def __init__(self, regnum: str) -> None:
        self._regnum = regnum

    def matches(self, vehicle: Vehicle) -> bool:
        return vehicle.regnum == self._regnum
