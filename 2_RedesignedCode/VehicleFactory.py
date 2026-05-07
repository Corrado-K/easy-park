from Vehicle import Vehicle, Car, Truck, Motorcycle, Bus, ElectricCar, ElectricBike


class VehicleFactory:
    """ Factory responsible for creating vehicle instances """

    vehicle_map = {
        "car": Car,
        "truck": Truck,
        "motorcycle": Motorcycle,
        "bus": Bus,
        "electric_car": ElectricCar,
        "electric_bike": ElectricBike,
    }

    @staticmethod
    def create_vehicle(vehicle_type: str, regnum: str, make: str, model: str, color: str) -> Vehicle:
        vehicle_class = VehicleFactory.vehicle_map.get(vehicle_type.lower())
        if vehicle_class is None:
            valid_types = list(VehicleFactory.vehicle_map.keys())
            raise ValueError(
                f"Unknown vehicle type: {vehicle_type}. "
                f"Available types: {valid_types}"
            )
        return vehicle_class(regnum, make, model, color)

    @staticmethod
    def get_available_types() -> list[str]:
        """Returns a list of available vehicle types."""
        return list(VehicleFactory.vehicle_map.keys())
