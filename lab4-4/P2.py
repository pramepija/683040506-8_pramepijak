"""
pramepijak ueasri
683040506-8
P2
"""


from abc import ABC, abstractmethod # abstract base class

class Vehicle(ABC):
    def __init__(self, make, model, year, is_running = False): # constructor
        self.make = make #convert to instance attribute
        self.model = model
        self.year = year
        self.is_running = is_running
    
    @abstractmethod
    def start_engine(self):
        """Start the vehicle engine"""
        pass

    @abstractmethod
    def stop_engine(self):
        """Stop the vehicle engine"""
        pass

    def get_info(self):
        """
        get vehicle information

        Args:
            None

        Returns:
            String : vehicle information
        
        Raises:            
            None

        """
        return f"Year: {self.year} \nMake: {self.make} \nModel: {self.model}"
    
class CommercialVehicle:
    def __init__(self, license_number, max_load, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0

    def load_cargo(self, weight):
        """
        load cargo into the vehicle
        
        Args:
            weight (float): weight of the cargo to be loaded in kg

        Returns:
            Bool : True if cargo is loaded successfully
            Bool : False if cargo cannot be loaded

        Raises:
            None

        """
        if weight > 0 and (self.current_load + weight <= self.max_load):
            self.current_load += weight
            return True
        return False
    
    def unload_cargo(self, weight):
        """
        unload cargo from the vehicle

        Args:
            weight (float): weight of the cargo to be unloaded in kg

        Returns:
            Float : current load after unloading
        
        Raises:
            None
        """
        if weight > 0 and (self.current_load - weight >= 0):
            self.current_load -= weight
            return self.current_load
        self.current_load = 0
        return self.current_load 
    
class Car(Vehicle):
    def __init__(self, num_doors, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_doors = num_doors

    def start_engine(self):
        """
        start the vehicle engine

        Args:
            None
        
        Returns:
            String : engine status
        """
        self.is_running = True
        return "started."

    def stop_engine(self):
        """
        stop the vehicle engine

        Args:
            None
        
        Returns:
            String : engine status

        Raises:
            None
        """
        self.is_running = False
        return "stopped."
    
class Trailer(CommercialVehicle):
    def __init__(self, num_axles = 2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_axles = num_axles

    def get_weight_per_axle(self):
        """
        get weight per axle

        Args:
            None

        Returns:
            Float : weight per axle in kg
        
        Raises:
            None
        """
        if self.num_axles <= 0:
            return 0
        return self.current_load / self.num_axles
    
class DeliveryVan(CommercialVehicle, Car):
    def __init__(self, make, model, year, license_number, max_load, num_doors, is_running = False):
        super().__init__(license_number=license_number, max_load=max_load, make=make, model=model, year=year, is_running=is_running, num_doors=num_doors)
        self.delivery_mode = False

    def toggle_delivery_mode(self):
        """
        Toggle delivery mode

        Args:
            None

        Returns:
            String : delivery mode status

        Raises:
            None
        """
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode set to {self.delivery_mode}"
    
    def get_info(self):
        """
        get delivery van information

        Args:
            None

        Returns:
            String : delivery van information

        Raises:            
            None
        
        """
        return super().get_info() + f" \nLicense Number: {self.license_number} \nMax Load: {self.max_load} kg \nNumber of Doors: {self.num_doors} \nDelivery Mode: {self.delivery_mode}"
    
    def begin_service(self):
        print(self.get_info())
        print(f"Loading 5000 kg: {self.load_cargo(5000)}")
        print(self.start_engine())
        print(self.toggle_delivery_mode())
        print(self.stop_engine())
        print(f"Unloading 2000 kg: Current load is {self.unload_cargo(2000)} kg")
        print(self.toggle_delivery_mode())

        
if __name__ == "__main__":
    Fifa = DeliveryVan("GTR", "R34", 2008,"683040506-8", 10000, "4", is_running = False  )
    Fifa.begin_service()