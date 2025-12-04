import json

class RecipeDatabase:
    def __init__(self, filename='recipes.json'):
        self.filename = filename
        self.recipes = {}
        self.load_recipes()
    
    def load_recipes(self):
        """Load and transform recipes from the JSON file."""
        with open(self.filename) as f:
            factorio_data = json.load(f)
        
        self.recipes = self._transform_recipes(factorio_data)
    
    def _transform_recipes(self, data_list):
        recipe_map = {}
        
        for item in data_list:
            item_id = item.get("id")
            recipe_data = item.get("recipe")
            
            # Skip items that don't have a recipe defined (e.g., raw resources)
            if not item_id or not recipe_data:
                continue
            
            # Extract base crafting time
            crafting_time = recipe_data.get("time", 0)
            yield_amount = recipe_data.get("yield", 1)
            
            # Transform the ingredients list into dictionary format
            ingredients_list = recipe_data.get("ingredients", [])
            ingredients_map = {}
            
            for ingredient in ingredients_list:
                ingredient_id = ingredient.get("id")
                amount = ingredient.get("amount")
                if ingredient_id and amount is not None:
                    ingredients_map[ingredient_id] = amount
            
            if yield_amount > 1:
               crafting_time = crafting_time / yield_amount
           
            # Build the final simplified recipe structure
            simplified_recipe = {
                "time": crafting_time,
                "ingredients": ingredients_map
            }
            
            # Add to the final map using the item's ID as the key
            recipe_map[item_id] = simplified_recipe
        
        return recipe_map
    
    def get_recipe(self, item_id):
        return self.recipes.get(item_id)
    
    def has_recipe(self, item_id):
        return item_id in self.recipes
    
    def get_all_recipe_ids(self):
        return list(self.recipes.keys())
    
    def print_recipe(self, item_id):
        recipe = self.get_recipe(item_id)
        if recipe:
            print(f"Recipe for '{item_id}':")
            print(f"  Time: {recipe['time']}s")
            print(f"  Ingredients: {recipe['ingredients']}")
        else:
            print(f"No recipe found for '{item_id}'")
    
    def print_summary(self, num_recipes=3):
        print("--- Recipe Database Summary ---")
        print(f"Total recipes loaded: {len(self.recipes)}")
        print(f"\nFirst {num_recipes} recipes:")
        
        for item_id, recipe in list(self.recipes.items())[:num_recipes]:
            print(f"\nRecipe for '{item_id}':")
            print(f"  Time: {recipe['time']}s")
            print(f"  Ingredients: {recipe['ingredients']}")
            print("-" * 40)
    
    def __len__(self):
        return len(self.recipes)
    
    def __contains__(self, item_id):
        return item_id in self.recipes
    
    def __repr__(self):
        return f"RecipeDatabase({len(self.recipes)} recipes loaded from '{self.filename}')"


# Example usage and testing
if __name__ == "__main__":
    # Create the database
    db = RecipeDatabase('recipes.json')
    
    # Print summary
    db.print_summary(3)
    
    # Example lookups
    print("\n=== Example Lookups ===")
    db.print_recipe("accumulator")
    
    print(f"\n=== Database Info ===")
    print(db)
    print(f"Has 'iron-plate' recipe: {db.has_recipe('iron-plate')}")
    print(f"Has 'iron-ore' recipe: {db.has_recipe('iron-ore')}")
    
    # Use 'in' operator
    print(f"'electronic-circuit' in database: {'electronic-circuit' in db}")