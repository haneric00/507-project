DEVICE_SPEEDS = {
    # --- Assemblers (multiplier) ---
    "assembling-machine-1": 0.5,
    "assembling-machine-2": 0.75,
    "assembling-machine-3": 1.25,
    
    # --- Furnaces (multiplier: use as crafting speed/multipler)---
    "stone-furnace": 1.0,
    "steel-furnace": 2.0,
    "electric-furnace": 2.0,
    
    # --- Chemical/Oil Processing ---
    "chemical-plant": 1.0,
    "oil-refinery": 1.0,
    "centrifuge": 1.0,
    
    # --- Rocket ---
    "rocket-silo": 1.0,
    
    # --- Mining ---
    "burner-mining-drill": 0.25,
    "electric-mining-drill": 0.5,
    "pumpjack": 1.0,
    
    # --- Inserters (items per second, single item mode) ---
    # "burner-inserter": 0.789,      # 60/76
    "inserter": 0.857,              # 60/70
    "long-handed-inserter": 1.2,    # 60/50
    "fast-inserter": 2.5,           # 60/24
    # "stack-inserter": 2.5,          # 60/24 (moves stacks, not single items)
    # "bulk-inserter": 2.5,           # 60/24
    
    # --- Belts (items per second with both lanes) ---
    "transport-belt": 15.0,
    "fast-transport-belt": 30.0,
    "express-transport-belt": 45.0,
    "turbo-transport-belt": 60.0,  # Space Age
    
    # --- Labs ---
    "lab": 1.0,
    
    # --- Pumps (fluid units per second) ---
    "offshore-pump": 1200.0,
    "pump": 200.0,  # Inline pump
    
    # --- Beacons ---
    "beacon": 0.5,  # Transmission efficiency (affects nearby buildings)
    
    # --- Boilers/Steam ---
    "boiler": 1.8,  # Water consumption (units/tick) * 60
    "heat-exchanger": 10.0 * 60,  # For nuclear
}

# Stack sizes for inserters (when using stack inserters)
STACK_INSERTER_BONUS = {
    "stack-inserter": 12,  # Can grab up to 12 items (with research)
    "bulk-inserter": 12,
}

def get_crafting_time(recipe_time: float, device_name: str) -> float:
    """
    Calculate actual crafting time for a recipe on a specific device.
    
    Args:
        recipe_time: Base recipe time in seconds
        device_name: Name of the crafting device
    
    Returns:
        Actual time in seconds to craft one item
    """
    key = device_name.lower().strip().replace(" ", "-")
    crafting_speed = DEVICE_SPEEDS.get(key, 1.0)
    return recipe_time / crafting_speed

def get_items_per_second(recipe_time: float, device_name: str) -> float:
    """
    Calculate items produced per second for a recipe on a specific device.
    
    Args:
        recipe_time: Base recipe time in seconds
        device_name: Name of the crafting device
    
    Returns:
        Items per second production rate
    """
    crafting_time = get_crafting_time(recipe_time, device_name)
    return 1.0 / crafting_time if crafting_time > 0 else 0.0

def get_device_speed(device_name: str) -> float:
    """
    Get the base speed/rate for a device.
    
    Returns:
        Speed multiplier or operations per second
    """
    key = device_name.lower().strip().replace(" ", "-")
    return DEVICE_SPEEDS.get(key, 1.0)

def print_device_metrics(device_name: str):
    """
    Print metrics for a specific device.
    """
    key = device_name.lower().strip().replace(" ", "-")
    
    if key not in DEVICE_SPEEDS:
        print(f"Device '{device_name}' not found in database.")
        return
    
    speed = DEVICE_SPEEDS[key]
    print(f"\nDevice: {device_name}")
    
    if key.startswith("assembling") or key in ["chemical-plant", "oil-refinery", "centrifuge", "rocket-silo"]:
        print(f"  - Crafting Speed: {speed}x")
        print(f"  - Example: 1.0s recipe → {get_items_per_second(1.0, key):.3f} items/sec")
    elif "furnace" in key:
        print(f"  - Smelting Speed: {speed}x")
        print(f"  - Example: 3.2s recipe → {get_items_per_second(3.2, key):.3f} items/sec")
    elif "belt" in key:
        print(f"  - Throughput: {speed} items/second")
    elif "inserter" in key:
        print(f"  - Swing Rate: {speed:.3f} operations/second")
        if key in STACK_INSERTER_BONUS:
            print(f"  - Max Stack Size: {STACK_INSERTER_BONUS[key]} items")
            print(f"  - Max Throughput: {speed * STACK_INSERTER_BONUS[key]:.1f} items/sec")
    elif "mining" in key or key == "pumpjack":
        print(f"  - Mining Speed: {speed}")
    elif "pump" in key:
        print(f"  - Flow Rate: {speed} fluid/second")
    elif key == "lab":
        print(f"  - Research Speed: {speed}x")
    else:
        print(f"  - Speed/Rate: {speed}")

def calculate_assemblers_needed(recipe_time: float, items_per_second_target: float, 
                                 device_name: str = "assembling-machine-3") -> float:
    """
    Calculate how many assemblers are needed to produce a target rate.
    
    Args:
        recipe_time: Base recipe time in seconds
        items_per_second_target: Desired production rate
        device_name: Type of assembler to use
    
    Returns:
        Number of assemblers needed (can be fractional)
    """
    items_per_assembler = get_items_per_second(recipe_time, device_name)
    return items_per_second_target / items_per_assembler

# --- Examples ---
if __name__ == "__main__":
    # Device lookups
    print_device_metrics("Assembling Machine 3")
    print_device_metrics("Fast Inserter")
    print_device_metrics("Stack Inserter")
    print_device_metrics("Electric Furnace")
    print_device_metrics("Express Transport Belt")
    
    # Production calculation example
    print("\n" + "="*50)
    print("PRODUCTION CALCULATION EXAMPLE")
    print("="*50)
    
    # Electronic circuits: 0.5s base time, want 10/sec
    recipe_time = 0.5
    target_rate = 10.0
    
    for assembler in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
        needed = calculate_assemblers_needed(recipe_time, target_rate, assembler)
        rate = get_items_per_second(recipe_time, assembler)
        print(f"\n{assembler}:")
        print(f"  - Rate per machine: {rate:.3f} items/sec")
        print(f"  - Machines needed for {target_rate}/sec: {needed:.2f}")