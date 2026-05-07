from dataclasses import dataclass

from SearchStrategy import SearchStrategy
from Vehicle import ElectricVehicle, Vehicle


@dataclass(frozen=True)
class SearchResult:
    """A slot that matched a SearchStrategy query."""
    slot_id: int
    is_ev: bool
    vehicle: Vehicle


class ParkingLot:
    """A single parking lot with a regular section and an EV section.

    Replaces the anti-pattern ParkingLot in old_source_code:
      - no UI / tkinter coupling
      - no module-level globals
      - creation delegated to VehicleFactory
      - lookups delegated to SearchStrategy (one find_slots method instead
        of eight near-identical getSlotNumFromX variants)
    """

    def __init__(self, regular_capacity: int, ev_capacity: int, level: int) -> None:
        self.level = level
        self._regular_slots: list[Vehicle | None] = [None] * regular_capacity
        self._ev_slots: list[Vehicle | None] = [None] * ev_capacity

    def park(self, vehicle: Vehicle) -> int | None:
        """Park a vehicle in the appropriate section. Returns 1-based slot id, or None if full."""
        section = self._ev_slots if isinstance(vehicle, ElectricVehicle) else self._regular_slots
        for i, slot in enumerate(section):
            if slot is None:
                section[i] = vehicle
                return i + 1
        return None

    def leave(self, slot_id: int, is_ev: bool) -> bool:
        section = self._ev_slots if is_ev else self._regular_slots
        index = slot_id - 1
        if 0 <= index < len(section) and section[index] is not None:
            section[index] = None
            return True
        return False

    def find_slots(self, strategy: SearchStrategy) -> list[SearchResult]:
        """Return every occupied slot whose vehicle matches the strategy."""
        results: list[SearchResult] = []
        for i, vehicle in enumerate(self._regular_slots):
            if vehicle is not None and strategy.matches(vehicle):
                results.append(SearchResult(i + 1, False, vehicle))
        for i, vehicle in enumerate(self._ev_slots):
            if vehicle is not None and strategy.matches(vehicle):
                results.append(SearchResult(i + 1, True, vehicle))
        return results

    def occupied_slots(self) -> list[SearchResult]:
        """All occupied slots (used for status/charge displays)."""
        results: list[SearchResult] = []
        for i, vehicle in enumerate(self._regular_slots):
            if vehicle is not None:
                results.append(SearchResult(i + 1, False, vehicle))
        for i, vehicle in enumerate(self._ev_slots):
            if vehicle is not None:
                results.append(SearchResult(i + 1, True, vehicle))
        return results
