from abc import ABC, abstractmethod

class Vehicle(ABC):
    """ Abstract base class for all vehicles """
    def __init__(self, regnum: str, make: str, model: str, color: str) -> None:
        self._regnum = regnum
        self._make = make
        self._model = model
        self._color = color

    @property
    def regnum(self) -> str:
        return self._regnum
    
    @property
    def make(self) -> str:
        return self._make
    
    @property
    def model(self) -> str:
        return self._model
    
    @property
    def color(self) -> str:
        return self._color

    @abstractmethod
    def get_type(self) -> str:
        """Returns the type of vehicle."""
        pass

    def __str__(self) -> str:
        return f"{self.get_type()} - color: {self._color}, make: {self._make}, model: {self._model}, regnum: {self._regnum}"

class Car(Vehicle):
    """Represents a standard petrol/diesel car."""

    def get_type(self) -> str:
        return "Car"

class Truck(Vehicle):
    """Represents a truck."""

    def get_type(self) -> str:
        return "Truck"

class Motorcycle(Vehicle):
    """Represents a motorcycle."""

    def get_type(self) -> str:
        return "Motorcycle"

class Bus(Vehicle):
    """Represents a bus."""

    def get_type(self) -> str:
        return "Bus"
        
class ElectricVehicle(Vehicle):
    """
        Abstract base class for electric vehicles.
        Extends Vehicle with charge level tracking.
    """
    def __init__(self, regnum: str, make: str, model: str, color: str) -> None:
        super().__init__(regnum, make, model, color)
        self._charge: int = 0
    
    @property
    def charge(self) -> int:
        return self._charge
    
    @charge.setter
    def charge(self, charge: int) -> None:
        """Sets charge level, clamped between 0 and 100."""
        if not 0 <= charge <= 100:
            raise ValueError(
                f"Charge level must be 0-100, got {charge}"
            )
        self._charge = charge
    
    def __str__(self) -> str:
        return f"{self.get_type()} - color: {self.color}, make: {self.make}, model: {self.model}, regnum: {self.regnum}, charge: {self.charge}"
    

class ElectricCar(ElectricVehicle):
    """Represents an electric car."""

    def get_type(self) -> str:
        return "Electric Car"

class ElectricBike(ElectricVehicle):
    """Represents an electric bike."""

    def get_type(self) -> str:
        return "Electric Bike"
    
