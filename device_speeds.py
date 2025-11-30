# Device speeds for Factorio machines
# For assemblers/furnaces/chemical plants: This is the crafting speed multiplier
# For inserters: Items moved per second (single item mode)
# For belts: Items per second throughput (both lanes combined)
# For miners: Mining speed multiplier

DEVICE_SPEEDS = {
    # --- Assemblers (crafting speed multiplier) ---
    "assembling-machine-1": 0.5,
    "assembling-machine-2": 0.75,
    "assembling-machine-3": 1.25,
    
    # --- Furnaces (smelting speed multiplier) ---
    "stone-furnace": 1.0,
    "steel-furnace": 2.0,
    "electric-furnace": 2.0,
    
    # --- Chemical/Oil Processing (crafting speed multiplier) ---
    "chemical-plant": 1.0,
    "oil-refinery": 1.0,
    "centrifuge": 1.0,
    
    # --- Rocket (crafting speed multiplier) ---
    "rocket-silo": 1.0,
    
    # --- Mining (mining speed multiplier) ---
    "burner-mining-drill": 0.25,
    "electric-mining-drill": 0.5,
    "pumpjack": 1.0,
    
    # --- Inserters (items moved per second) ---
    "inserter": 0.857,
    "long-handed-inserter": 1.2,
    "fast-inserter": 2.5,
    
    # --- Belts (items per second, both lanes) ---
    "transport-belt": 15.0,
    "fast-transport-belt": 30.0,
    "express-transport-belt": 45.0,
    "turbo-transport-belt": 60.0,
    
    # --- Labs (research speed multiplier) ---
    "lab": 1.0,
    
    # --- Pumps (fluid units per second) ---
    "offshore-pump": 1200.0,
    "pump": 200.0,
    
    # --- Beacons (transmission efficiency multiplier) ---
    "beacon": 0.5,
    
    # --- Boilers/Steam (consumption rate) ---
    "boiler": 108.0,  # Water per second
    "heat-exchanger": 600.0,  # For nuclear
}


class DeviceCalculator:
    """Helper class for calculating production rates and machine requirements."""
    
    @staticmethod
    def normalize_device_name(device_name: str) -> str:
        """Normalize device name to match DEVICE_SPEEDS keys."""
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
        elif key in ["chemical-plant", "oil-refinery", "centrifuge"]:
            return "chemical"
        elif "mining" in key or key == "pumpjack":
            return "miner"
        elif "pump" in key:
            return "pump"
        elif key == "lab":
            return "lab"
        elif key == "rocket-silo":
            return "rocket-silo"
        elif key == "beacon":
            return "beacon"
        elif key in ["boiler", "heat-exchanger"]:
            return "boiler"
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
        
        if device_type in ["assembler", "chemical", "rocket-silo", "lab"]:
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
        
        elif device_type == "miner":
            print(f"Mining Speed: {speed}x")
        
        elif device_type == "pump":
            print(f"Flow Rate: {speed:.1f} fluid/second")
        
        elif device_type == "beacon":
            print(f"Transmission Efficiency: {speed}x")
        
        elif device_type == "boiler":
            print(f"Consumption Rate: {speed:.1f} units/second")
        
        else:
            print(f"Speed/Rate: {speed}")


def print_production_example():
    """Print an example production calculation."""
    print("\n" + "="*60)
    print("PRODUCTION CALCULATION EXAMPLE")
    print("="*60)
    
    recipe_name = "Electronic Circuit"
    recipe_time = 0.5
    target_rate = 10.0
    
    print(f"\nTarget: Produce {target_rate} {recipe_name}s per second")
    print(f"Recipe time: {recipe_time}s")
    print()
    
    for assembler in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
        rate = DeviceCalculator.calculate_production_rate(recipe_time, assembler)
        needed = DeviceCalculator.calculate_machines_needed(recipe_time, target_rate, assembler)
        
        print(f"{assembler}:")
        print(f"  Production rate: {rate:.3f} items/sec per machine")
        print(f"  Machines needed: {needed:.2f} ({int(needed) + 1} rounded up)")
        print()


# --- Usage Examples ---
if __name__ == "__main__":
    # Display device information
    print("="*60)
    print("DEVICE INFORMATION")
    print("="*60)
    
    DeviceCalculator.print_device_info("Assembling Machine 3")
    DeviceCalculator.print_device_info("Fast Inserter")
    DeviceCalculator.print_device_info("Electric Furnace")
    DeviceCalculator.print_device_info("Express Transport Belt")
    
    # Production example
    print_production_example()
    
    # Quick calculations
    print("="*60)
    print("QUICK CALCULATIONS")
    print("="*60)
    
    # How fast can assembler-3 make iron gears?
    iron_gear_time = 0.5
    rate = DeviceCalculator.calculate_production_rate(iron_gear_time, "assembling-machine-3")
    print(f"\nIron Gear Wheels on Assembler-3: {rate:.3f} items/sec")
    
    # How many furnaces to smelt 10 iron plates/sec?
    iron_plate_time = 3.5
    needed = DeviceCalculator.calculate_machines_needed(iron_plate_time, 10.0, "electric-furnace")
    print(f"Electric Furnaces needed for 10 iron plates/sec: {needed:.2f}")
    
    # Copper cable production (yields 2 per craft)
    copper_cable_time = 0.5
    copper_cable_yield = 2
    rate = DeviceCalculator.calculate_production_rate(copper_cable_time, "assembling-machine-3", copper_cable_yield)
    print(f"Copper Cable on Assembler-3 (yield 2): {rate:.3f} items/sec")