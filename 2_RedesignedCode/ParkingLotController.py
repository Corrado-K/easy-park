"""The Controller layer: glue between View and Model.

The Controller holds the only reference to the live `ParkingLot`, knows
how to read form fields from the View, and knows how to call the
VehicleFactory and SearchStrategy subsystems. The View never talks to
domain objects; the domain objects never talk to tkinter. The Controller
sits between them.

Every handler here follows the same three-step shape:

    1. read input from the View (view.read_*)
    2. call the Model (self._lot.*, VehicleFactory.*, MatchBy*)
    3. write a human-readable result back to the View (view.show)
"""

from ParkingLot import ParkingLot, SearchResult
from ParkingLotView import ParkingLotView
from SearchStrategy import MatchByColor, MatchByRegnum
from Vehicle import ElectricVehicle
from VehicleFactory import VehicleFactory


class ParkingLotController:
    def __init__(self, view: ParkingLotView) -> None:
        self._view = view
        self._lot: ParkingLot | None = None
        self._bind_buttons()

    def _bind_buttons(self) -> None:
        self._view.on_create_lot(self._handle_create_lot)
        self._view.on_park(self._handle_park)
        self._view.on_remove(self._handle_remove)
        self._view.on_find_by_regnum(self._handle_find_by_regnum)
        self._view.on_find_by_color(self._handle_find_by_color)
        self._view.on_regnum_by_color(self._handle_regnum_by_color)
        self._view.on_charge_status(self._handle_charge_status)
        self._view.on_status(self._handle_status)

    # --- Handlers (one per button) ---

    def _handle_create_lot(self) -> None:
        try:
            capacity, ev_capacity, level = self._view.read_lot_config()
        except ValueError:
            self._view.show("Capacity and level must be whole numbers.\n")
            return
        self._lot = ParkingLot(capacity, ev_capacity, level)
        self._view.show(
            f"Created lot: {capacity} regular + {ev_capacity} EV on level {level}\n"
        )

    def _handle_park(self) -> None:
        if not self._require_lot():
            return
        form = self._view.read_park_form()
        if not form["regnum"]:
            self._view.show("Registration # is required.\n")
            return
        vehicle_type = self._vehicle_type_for(form["is_ev"], form["is_motor"])
        try:
            vehicle = VehicleFactory.create_vehicle(
                vehicle_type,
                form["regnum"],
                form["make"],
                form["model"],
                form["color"],
            )
        except ValueError as e:
            self._view.show(f"Could not create vehicle: {e}\n")
            return
        slot = self._lot.park(vehicle)
        if slot is None:
            self._view.show("Sorry, parking lot is full.\n")
        else:
            section = "EV" if form["is_ev"] else "regular"
            self._view.show(f"Allocated {section} slot {slot}.\n")

    def _handle_remove(self) -> None:
        if not self._require_lot():
            return
        try:
            slot_id, is_ev = self._view.read_leave_form()
        except ValueError:
            self._view.show("Slot # must be a whole number.\n")
            return
        if self._lot.leave(slot_id, is_ev):
            section = "EV" if is_ev else "regular"
            self._view.show(f"{section.capitalize()} slot {slot_id} is free.\n")
        else:
            self._view.show(f"Unable to remove a car from slot {slot_id}.\n")

    def _handle_find_by_regnum(self) -> None:
        if not self._require_lot():
            return
        results = self._lot.find_slots(MatchByRegnum(self._view.read_search_regnum()))
        if not results:
            self._view.show("Not found.\n")
            return
        for r in results:
            section = "EV" if r.is_ev else "regular"
            self._view.show(f"Identified slot: {r.slot_id} ({section})\n")

    def _handle_find_by_color(self) -> None:
        if not self._require_lot():
            return
        results = self._lot.find_slots(MatchByColor(self._view.read_search_color()))
        self._view.show("Identified slots: " + self._format_slot_list(results) + "\n")

    def _handle_regnum_by_color(self) -> None:
        if not self._require_lot():
            return
        results = self._lot.find_slots(MatchByColor(self._view.read_regnum_by_color()))
        regnums = ", ".join(r.vehicle.regnum for r in results)
        self._view.show(f"Registration Numbers: {regnums}\n")

    def _handle_status(self) -> None:
        if not self._require_lot():
            return
        self._view.show(
            "Vehicles\nSlot\tFloor\tEV?\tReg No.\tColor\tMake\tModel\n"
        )
        for r in self._lot.occupied_slots():
            v = r.vehicle
            self._view.show(
                f"{r.slot_id}\t{self._lot.level}\t{'Y' if r.is_ev else 'N'}\t"
                f"{v.regnum}\t{v.color}\t{v.make}\t{v.model}\n"
            )

    def _handle_charge_status(self) -> None:
        if not self._require_lot():
            return
        ev_results = [
            r for r in self._lot.occupied_slots()
            if isinstance(r.vehicle, ElectricVehicle)
        ]
        if not ev_results:
            self._view.show("No electric vehicles parked.\n")
            return
        self._view.show("EV Charge Levels\nSlot\tFloor\tReg No.\tCharge %\n")
        for r in ev_results:
            self._view.show(
                f"{r.slot_id}\t{self._lot.level}\t{r.vehicle.regnum}\t{r.vehicle.charge}\n"
            )

    # --- Small helpers ---

    def _require_lot(self) -> bool:
        if self._lot is None:
            self._view.show("Create a parking lot first.\n")
            return False
        return True

    @staticmethod
    def _vehicle_type_for(is_ev: bool, is_motor: bool) -> str:
        if is_ev:
            return "electric_bike" if is_motor else "electric_car"
        return "motorcycle" if is_motor else "car"

    @staticmethod
    def _format_slot_list(results: list[SearchResult]) -> str:
        return ", ".join(
            f"{r.slot_id}{'(EV)' if r.is_ev else ''}" for r in results
        )