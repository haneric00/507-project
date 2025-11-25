""" EXAMPLE USAGE:
factory = Factory()

furnace1 = factory.new_node('furance1', prod=[('iron_plate', 2)], cons=[('iron_ore', 1)])
source = factory.new_node('source1', prod=[('iron_ore', 10)], cons=[])

furnace1.add_input(source)


print(factory)
"""

import itertools

class Recipe:

    def __init__(self, result, time, ingredients):
        self.result = result # item produced by recipe
        self.time = time # time in seconds required for recipe
        self.ingredients = ingredients # str -> int dict for ingr counts

    @classmethod
    def from_str(cls, input_str):
        pass # TODO: implement this!



class FactoryNode:
    id_iter = itertools.count()

    def __init__(self, name, prod = [('fish', 1)], recipe = None):
        self.id = next(FactoryNode.id_iter)
        self.name = name # Just the component type, e.g. assembler
        self.items_produced = prod
        self.recipe = Recipe.from_str(recipe) if recipe else None
        self.inputs = set()
        self.factory = None

    
    @staticmethod
    def inserter(ins_type, from_node):
        if ins_type == 'normal':
            return FactoryNode('inserter_normal', prod=[(from_node.prod[0][0], 0.5)], cons=[(from_node.prod[0][0], 0.5)])

    def max_production(self):
        return self.prod
    
    def max_consumption(self):
        return self.cons
    
    def add_input(self, node):
        inserter = FactoryNode.inserter('normal', node)

        if node.factory is not None:
            node.factory.add_node(inserter)
            inserter.factory = node.factory

        self.inputs.add(inserter)
        inserter.inputs.add(node)


class Factory:
    def __init__(self):
        self.nodes = set()
    
    def new_node(self, *args, **kwargs):
        node = FactoryNode(*args, **kwargs)
        self.nodes.add(node)
        node.factory = self
        return node
    
    def add_node(self, node):
        self.nodes.add(node)
        node.factory = self
    
    def __repr__(self):
        out = ''
        for node in self.nodes:
            out += f"Node: {node.name}\n"
            out += f"  Max Production: {node.prod}\n"
            out += f"  Max Consumption: {node.cons}\n"
            out += f"  Inputs: {[input_node.name for input_node in node.inputs]}\n"
        
        return out



