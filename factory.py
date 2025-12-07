import itertools
import json 
from recipe_map import RecipeDatabase


recipe_db = RecipeDatabase('recipes.json')

class Recipe:

    def __init__(self, result, time, ingredients):
        self.result = result # item produced by recipe
        self.time = time # time in seconds required for recipe
        self.ingredients = ingredients # str -> int dict for ingr counts

    @classmethod
    def from_str(cls, input_str):
        """
        Takes a recipe name (string) and returns a Recipe object.
        
        Args:
            input_str: Recipe name like "electronic-circuit" or "iron-plate"
        
        Returns:
            Recipe object with result, time, and ingredients populated
        """
        # Look up the recipe in the loaded recipe map
        recipe_data = recipe_db.get_recipe(input_str)
        
        if recipe_data is None:
            raise ValueError(f"Recipe '{input_str}' not found in recipe database")
        
        # Create and return a Recipe object
        return cls(
            result=input_str,
            time=recipe_data["time"],
            ingredients=recipe_data["ingredients"]
        )
    
    def __repr__(self):
        return f"Recipe(result='{self.result}', time={self.time}, ingredients={self.ingredients})"

class FactoryNode:
    id_iter = itertools.count()

    def __init__(self, name, prod = None, recipe = None, sources = None, backer=None):
        self.id = next(FactoryNode.id_iter)
        self.name = name # Just the component type, e.g. assembler

        if prod:
            self.items_produced = prod # set of names of items produced
        else:
            self.items_produced = set()
        
        if type(recipe) == Recipe:
            self.recipe = recipe
        elif type(recipe) == str:
            self.recipe = Recipe.from_str(recipe)

        if sources:
            self.sources = sources
        else:
            self.sources = set()
        self.factory = None

        self.backer = backer

    def add_prod(self, prod):
        if type(prod) == set:
            self.items_produced = self.items_produced.union(prod)
        else:
            self.items_produced.add(prod) 

    # returns module type
    # 'assembler' for assembling-machine-1, etc.
    def module_type(self):
        if 'assembling' in self.name:
            return 'assembler'
        elif 'inserter' in self.name:
            return 'inserter'
        elif 'chest' in self.name:
            return 'chest'
        return 'unknown'
    
    def __str__(self):
        return str(self.id) + "_" + self.name

class Factory:
    def __init__(self):
        self.nodes = set()
    
    def add_node(self, node):
        self.nodes.add(node)
        node.factory = self
    
    def __repr__(self):
        out = ''
        for node in self.nodes:
            out += f"Node: {node}\n"
            out += f"  Sources: {[str(input_node) for input_node in node.sources]}\n"
            if node.backer:
                out += f"  Data {hex(id(node.backer))} | {node.backer.position}\n"
            if node.items_produced:
                out += f"  Prod: {node.items_produced}\n"
        
        return out