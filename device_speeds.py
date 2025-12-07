# Device speeds for Factorio machines

DEVICE_SPEEDS = {
    "assembling-machine-1": 0.5,
    "assembling-machine-2": 0.75,
    "assembling-machine-3": 1.25,
    "stone-furnace": 1.0,
    "steel-furnace": 2.0,
    "electric-furnace": 2.0,
    "burner-mining-drill": 0.25,
    "electric-mining-drill": 0.5,
    "pumpjack": 1.0,
    "inserter": 0.857,
    "long-handed-inserter": 1.2,
    "fast-inserter": 2.5,
    "transport-belt": 15.0,
    "fast-transport-belt": 30.0,
    "express-transport-belt": 45.0,
    "turbo-transport-belt": 60.0,
}


class DeviceCalculator:
    """Helper class for calculating production rates and machine requirements."""
    
    @staticmethod
    def normalize_device_name(device_name: str) -> str:
        """Normalize device name to match DEVICE_SPEEDS """
        return device_name.lower().strip().replace(" ", "-")
    
    @staticmethod
    def get_device_speed(device_name: str) -> float:
        key = DeviceCalculator.normalize_device_name(device_name)
        return DEVICE_SPEEDS.get(key, 1.0)
    
    @staticmethod
    def calculate_crafting_time(recipe_time: float, device_name: str) -> float:
        crafting_speed = DeviceCalculator.get_device_speed(device_name)
        return recipe_time / crafting_speed
    
    @staticmethod
    def calculate_production_rate(recipe_time: float, device_name: str, yield_amount: int = 1) -> float:
        actual_time = DeviceCalculator.calculate_crafting_time(recipe_time, device_name)
        if actual_time <= 0:
            return 0.0
        return yield_amount / actual_time
    
    @staticmethod
    def calculate_machines_needed(recipe_time: float, target_rate: float, 
                                  device_name: str = "assembling-machine-3",
                                  yield_amount: int = 1) -> float:
        """
        Calculate how many machines are needed to produce a target rate.
        
        Args:
            recipe_time: Base recipe time in seconds
            target_rate: Desired production rate (items/second)
            device_name: Type of machine to use
            yield_amount: Number of items produced per craft (default 1)
        
        Returns:
            Number of machines needed (can be fractional)
        """
        rate_per_machine = DeviceCalculator.calculate_production_rate(
            recipe_time, device_name, yield_amount
        )
        if rate_per_machine <= 0:
            return float('inf')
        return target_rate / rate_per_machine
    
    @staticmethod
    def get_device_type(device_name: str) -> str:
        """Determine the type of device based on its name."""
        key = DeviceCalculator.normalize_device_name(device_name)
        
        if "assembling" in key:
            return "assembler"
        elif "furnace" in key:
            return "furnace"
        elif "inserter" in key:
            return "inserter"
        elif "belt" in key:
            return "belt"
        else:
            return "unknown"
    
    @staticmethod
    def print_device_info(device_name: str):
        """Print formatted information about a device."""
        key = DeviceCalculator.normalize_device_name(device_name)
        
        if key not in DEVICE_SPEEDS:
            print(f"Device '{device_name}' not found in database.")
            return
        
        speed = DEVICE_SPEEDS[key]
        device_type = DeviceCalculator.get_device_type(key)
        
        print(f"\nDevice: {device_name}")
        print(f"Type: {device_type}")
        
        if device_type == "assembler":
            print(f"Crafting Speed: {speed}x")
            example_rate = DeviceCalculator.calculate_production_rate(1.0, key)
            print(f"Example: 1.0s recipe → {example_rate:.3f} items/sec")
        
        elif device_type == "furnace":
            print(f"Smelting Speed: {speed}x")
            example_rate = DeviceCalculator.calculate_production_rate(3.5, key)
            print(f"Example: 3.5s recipe → {example_rate:.3f} items/sec")
        
        elif device_type == "belt":
            print(f"Throughput: {speed:.1f} items/second (both lanes)")
        
        elif device_type == "inserter":
            print(f"Transfer Rate: {speed:.3f} items/second")

        else:
            print(f"Speed/Rate: {speed}")
