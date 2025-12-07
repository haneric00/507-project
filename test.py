from draftsman.blueprintable import *
from draftsman.constants import Direction
from draftsman.entity import *

from factory import *

bp = '0eNqtl21zoyAQx78Lr7EjIEbzVW46GTSbljlFD7BzmYzf/VCTpmk0RS7vIg+/ZXf/G5YTKqoOWi2VRdsTkmWjDNr+OiEj35SohjElakBbJIyBuqikeotqUb5LBRFBPUZS7eEv2pIez2yyWijTNtpGBVT2y3Lav2IEykorYTI4fhx3qqsL0I6HFxgYtY1x2xo12HGoKH3hGB3dD8ZfeD+c4xuLhrCSeRb7ZEllQFs3dk/hNxSM9lJDOS0gdAaa4IdRvjfAvhlweNkO+8umbUFHpSgqQJfx3Z9OVM6em1eNrl2GZs7A/YMU3wT8xr1shpyGkBMf8sYnGWRlMrIQtbB5teQhLDrPInFIHJlPHAkJQVMvdFDxkYUQsBBYvABL1pUy8VIP4eG1TJ5VyySo5IhXPjch6NgLna0rZ8+EhNQgzRdukjgEli3AyCoBjpif/aU0WIBnC08QIGUBKhmD/qNKaBKCzrzQfJUAfROShmhms6CZTQgsXYBlIaHceIUyD0GnPmh2rUHTFcaKcekdllySNNvFeZXeNYBe3QgLueroQs/K1jWalHtpkT3sNOnDPwf+rD8Hdi2z3zo6CGOjqhH7WQfjBynAyB7bKUBtZ2cthdyD1KupZet6T9/8fL0CD1K5uah8B/NYQlOPd9mwM2CtS6sZFmqomw/YdW6uckeE/U5aqN3UQVQGMJqGpxfY2fA5sW0l7JDYsumGtyGJXdnVzX6UjksYiPFQn6+/11kR5/7uxP/ljtUd9MObcvh25q6vWow+nIOjIZ7SPMlznhGW53HS9/8AKoXg8w=='
#bp = '0eNqtlt1urCAUhd+Fa2zEERVf5aQxyOy2JAgWsDnNxHfvdmyncyb2RCa9HH6+tdeGxXgivZlg9NpG0p6IVs4G0v45kaCfrTTLmJUDkJbIEGDojbbP2SDVi7aQMTJTou0R/pKWzXRjU/TShtH5mPVg4tXyYn6kBGzUUcMqeP7x3tlp6MEjj34xtA3gI45RMrqAG5xdFBCS8eKBU/JO2kPDHzjSj9qDWlewYqnohlpcUZ+0xalMvUCIW+zDDftrRxcgRmxDWFZ6GNwbdBPOGawRjp2OMODUkzQBKFmHV4efysqNI/hsNDIC6io3Lb1neU7J4I7nVsfMgDxXdenu47xh50B/aPSGHfZzq8oNdJmAztPQfM/RliLxaCv635u6oVDfKCBfj1cnpGRvlhNax7vXSRoUxHnr/IDXfKOIepc1fhGudllrkq193936X2tgUMk7q1WmtFeTjmkGRWIsxS6DLL8rl+JXc6mxLb+SSsbuiqXYkx1W3JXLfeyE56RsLuxmFzvhPbmK/j42v4u99GSLViXQqsRK6wR2nchuEt+eZiOa+Ke85AQZ358FlLxhUs4reFWIUgjesIMQeTnPH3TUsvw='
bp = '0eNqtVNtOwzAM/ZXKzylab7D2gR8BVKWpAUtpUpIUgab+O247tjHGtEm8JbZzjo8v2UCjB+wdmQDVBlr0ylEfyBqoQNm+RxfF99H2pGSjcbqjRhWcNaQiRU4NFPyjITZEvZYB/Z8xxkYN6uBBAClrPFQPG/D0YqSe+I3skIml99g1msxL3En1SgbjBEZ+Ylr8gCoZnwSgCRQIF4T58lmboWvQcYD4RiLzTIZdsXpFH5i1t54WeRtgqDgrbgoBn1Bld+lNMXMsL2qPIXAGfop02Nl3rAf26YAO25oCdux6ltqjgMW85LJlXkoWz/VgXmWHqcTJaiWgs+2sMsQa5ZzVXtg4il9y0gM5Hh0znRKSHwlpyXED5ogkPYGaibPlPsGQHjEwPvUHWufxgG97/TZIzYTsN9Z13OATSeQXSVvtiLOLpBVXohYXod5eMVXJEfZ/TdW0Y/8yU3fXdj9d7yTlP7u/X/R4u+jnZoBXd1LJlv3PI+Cddc5kxW1a5mVZrJOsLFf5OH4BYMmMqg=='
#bp = '0eNp9kN1qBCEMRt8l107p/C3VVynL4rhhG9Bo1SldBt+9mV2WQlt6Zz7jOSYbLH7FlIkrmA3IRS5gXjcodGHr94xtQDBgS8GweOJLF6x7I8auh6aA+IyfYPp2VIBcqRLeCbfieuI1LJilQT1IxAVzlUxBikUeRN49AunG6WlWcAUzHuQk9DNldPeOfmjqF3VQ//7vD8PwwyB8SjvAxZQwd84uHuGRn95X60Uo9xxzkI3sc1LFIMn36hR8YC43zXwY9KT1/NKPWj9PrX0Bru90gQ=='
#bp = '0eNqV0dsKgzAMBuB3yXUVD9XZvsoYw0MYBY3S1jGRvvuqXowxhXmZ8OcLJDNU7YiDVmRBzqDqngzI6wxGPahslx6VHYIEq0syQ69tUGFrwTFQ1OALZOxuDJCssgq32bWY7jR2FWofYAcGg6E3fqynZY+nggsPMwYTyLQQYeYc+8GSE1jyhTFolMZ6S/AdOj1BR8d0sUPz/+m8OKbjZLm1sth56fM4Bk/UZk1keSK4EFkRp0JE3Lk3Z2ic9A=='
blueprint = Blueprint.from_string(bp)




UP      = 0
RIGHT   = 4
DOWN    = 8
LEFT    = 12

class SourcedEntity:
    def __init__(self, entity):
        self.entity = entity
        self.sources = []
    
    def add_source(self, source):
        self.sources.append(source)

for entity in blueprint.entities:
    entity.sources = set()
    entity.sinks = set()

for entity in blueprint.entities:

    if type(entity) in [ElectricPole, Entity]:
        print(f'skipping entity {entity}')

    if type(entity) in [Inserter, TransportBelt, Loader]:
    
        if entity.direction == UP:
            target_pos = (0, 1)
        elif entity.direction == RIGHT:
            target_pos = (1, 0)
        elif entity.direction == DOWN:
            target_pos = (0, -1)
        elif entity.direction == LEFT:
            target_pos = (-1, 0)
        
        target = blueprint.find_entities_filtered(position = entity.position - target_pos)

        print(f'finding feed target for position {entity.position + target_pos}, {target}')

        # These nodes "feed" into something, so add to their sources
        # Either: we are an inserter and feeding into something,
        # or we are a transport belt feeding into another transport belt
        if target and (type(entity) in [Inserter, Loader] or (type(entity) == TransportBelt and type(target[0]) == TransportBelt)):
            target[0].sources.add(entity)
            print(f'{type(entity)} {hex(id(entity))} -> {type(target[0])} {id(target[0])} add feed target')
            print(target[0].sources)

        # add source target
        if target and type(entity) in [Inserter, Loader]:
            source = blueprint.find_entities_filtered(position = entity.position + target_pos)
            if source:
                print(f'{type(source[0])} {id(source[0])} -> {type(entity)} {id(entity)} add source target')
                entity.sources.add(source[0])
                
        
    if type(entity) == AssemblingMachine:
        recipe = Recipe.from_str(entity.recipe)
        entity.factory_node = FactoryNode(entity.name, prod=recipe.result, recipe=recipe, backer=entity)
    
    elif type(entity) == InfinityContainer:
        prod = entity.filters
        if not prod:
            print(f'Infinity Chest does not produce any items! {entity}')
            entity.factory_node = FactoryNode(entity.name, backer=entity)
        else:
            entity.factory_node = FactoryNode(entity.name, prod={prod[0].name}, backer=entity)
    else:
        entity.factory_node = FactoryNode(entity.name, backer=entity)

factory = Factory()

# add all nodes to factory with sources
for entity in blueprint.entities:
    node = entity.factory_node
    for source in entity.sources:
        node.sources.add(source.factory_node)
    factory.add_node(node)
    print(node, node.sources)

def find_source_assembler(node):
    #print(node)
    if node.name in ['infinity-chest', 'assembling-machine-1']:
        return node
    for source in node.sources:
        return find_source_assembler(source)
    
    print(f'no item producer for {node}')
    
# add prod types for inserters and belts
for entity in blueprint.entities:
    node = entity.factory_node
    if type(entity) in [TransportBelt, Inserter]:
        #print(node, [str(x) for x in node.sources])
        source = find_source_assembler(node)
        if source:
            node.add_prod(source.items_produced)

print(factory)






from z3 import *


CHEST_PROD = 100 # An arbitrary value, in items/second.
INSERTER_SPEEDS = [0.79, 0.86, 1.2, 2.5, 5] # in items/second.
ASSEMBLER_SPEEDS = [0.5, 0.75, 1.25] # dimensionless, divide recipe time by
                                     # this value to get assembler production
                                     # time.

def factory_to_constraints(solver, factory):
    """
    Parses the given factory, adding constraints to the given solver.
    solver - solver to add constraints to
    factory - factory to parse constraints from
    Returns the dictionary of symbols created in the solving process.
    """


    def to_symb_name(*attrs):
        """
        Helper for converting node attributes to a symbolic variable name.
        Should be used in one of the two following ways:
        - to_symb_name(node.id, item, "p")
        - to_symb_name(node.id, "s")
        """
        res = ""
        for attr in attrs:
            res = res + " " +  str(attr)
        return res.strip()


    # Loop through all factory nodes and create necessary symbolic variables.
    # Store names in a dictionary for access later.
    symbs = {}
    for node in factory.nodes:
        # Every item produced requires its own symbolic production rate.
        for item in node.items_produced:
            symb = to_symb_name(node, item, "p")
            symbs[symb] = Real(symb)

        if (node.module_type() == "inserter" 
            or node.module_type() == "assembler"):
            # Each has a speed setting.
            symb = to_symb_name(node, "s")
            symbs[symb] = Real(symb)

            # Add optimization constraints to all speed symbolic variables.
            # TODO: is this the right way to do this? alternative is minimize
            # sum of all speed symbolic variables.
            solver.minimize(symbs[symb])


    # Add constraints for all factory nodes to the solver.
    for node in factory.nodes:
        match node.module_type():
            case "chest":
                # Chests have a static production rate for items.
                for item in node.items_produced:
                    symb_chest_item_prod = (
                            symbs[to_symb_name(node, item, "p")])
                    solver.add(symb_chest_item_prod == CHEST_PROD)


            case "inserter":
                # An inserter's speed can be any one of severl settings from
                # the game. Add a disjunction indicating the speed takes on one
                # of these values.
                # TODO: update INSERTER_SPEEDS, match real const name
                spd_clauses = []
                symb_inserter_spd = symbs[to_symb_name(node, "s")]
                for spd in INSERTER_SPEEDS:
                    spd_clauses.append(symb_inserter_spd == spd)
                solver.add(Or(*spd_clauses))


                # For every item that the inserter that can produce, three
                # clauses are added:
                # 1. A disjunction of the two possible throughputs: the speed
                #   setting or the weighted* input production rate of the item.
                # 2. An inequality limiting the inserter's throughput to at
                #   most the weighted input production rate of the item.
                # 3. An inequality limiting the inserter's throughput to at 
                #   most the speed setting of the inserter.
                # Together these encode the constraint that the inserter's
                # throughput for the item is the minimum between these two
                # values.
                # *the weighted input production rate is the item's input prod
                # rate times this inserter's speed as a fraction of the sum of
                # all inserter speeds for inserters drawing from the source.
                # NOTE: the items produced by an inserter's sources are equal
                # to the items produced by all its sources. Currently I assume
                # an inserter has a single source.

                # First calculate this inserter's weighted fraction of items
                # produced by its source. NOTE: again assuming 1 source.
                source_id = next(iter(node.sources)).id
                all_inserter_speeds = []
                for other_node in factory.nodes:
                    if (other_node.module_type() == "inserter" and
                        source_id in map(lambda node: node.id,
                                         other_node.sources)):
                        all_inserter_speeds.append(
                                symbs[to_symb_name(other_node, "s")])

                input_weight = (symbs[to_symb_name(node, "s")] 
                                / Sum(*all_inserter_speeds))

                for item in node.items_produced:
                    symb_inserter_item_prod = (
                            symbs[to_symb_name(node, item, "p")])

                    # NOTE: if assuming more than one source, need to aggregate
                    # input production for clauses.
                    for source in node.sources:
                        symb_source_item_prod = (
                                symbs[to_symb_name(source, item, "p")])
                                

                        
                        solver.add(Or(
                            symb_inserter_item_prod == (symb_source_item_prod
                                                        * input_weight),
                            symb_inserter_item_prod == symb_inserter_spd))
                        
                        solver.add(
                            symb_inserter_item_prod <= (symb_source_item_prod
                                                        * input_weight))

                        solver.add(
                            symb_inserter_item_prod <= symb_inserter_spd)


            case "assembler":
                # An assembler's speed can be any one of several settings from
                # the game. Add a disjunction indicating the speed takes on one
                # of these values.
                spd_clauses = []
                symb_asm_spd = symbs[to_symb_name(node, "s")]
                for spd in ASSEMBLER_SPEEDS:
                    spd_clauses.append(symb_asm_spd == spd)
                solver.add(Or(*spd_clauses))

                # If the system is SAT, then the assembler will have no stalls
                # and the throughput will be the spd / recipe time.
                symb_asm_prod = (
                        symbs[to_symb_name(node, node.recipe.result, "p")])
                solver.add(symb_asm_prod == symb_asm_spd / node.recipe.time)

                # For every item in the assembler's recipe, create an
                # inequality mandating the input production rate of that item >=
                # the overall assembler production rate of recipe item *
                # ingredient count per recipe.
                for ingredient, count in node.recipe.ingredients.items():
                    # Determine the aggregate input production rate for this
                    # item.

                    # for each source, if symbol corresponding to source's prod
                    # of this ingredient exists, add to list of input sources.
                    ingredient_inputs = []
                    for source in node.sources:
                        source_ingredient_prod_str = (
                                to_symb_name(source, ingredient, "p"))
                        if source_ingredient_prod_str in symbs:
                            ingredient_inputs.append(
                                    symbs[source_ingredient_prod_str])

                    solver.add(Sum(ingredient_inputs) >= symb_asm_prod * count)


            case name:
                print(f"Skipping unknown node type {name}")

    return symbs




solver = Optimize()
symbs = factory_to_constraints(solver, factory)

print("Symbols:")
for symb in symbs:
    print(f"    {symb}")

print("Constraints:")
for constraint in solver.assertions():
    print(f"    {constraint}")

print("Solver result:")
print(f"    {solver.check()}")

print("Solver assignments:")
model = solver.model()
for name, var in symbs.items():
    print(f"    {name} : {model[var]}")
