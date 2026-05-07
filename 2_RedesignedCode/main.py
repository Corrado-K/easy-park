"""Entry point. Wires the three MVC layers together and starts tkinter.

View (tkinter widgets) <-- Controller (glue) --> Model (ParkingLot, Factory, Strategy)
"""

from ParkingLotController import ParkingLotController
from ParkingLotView import ParkingLotView


def main() -> None:
    view = ParkingLotView()
    ParkingLotController(view)
    view.root.mainloop()


if __name__ == "__main__":
    main()
