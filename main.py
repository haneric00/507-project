from z3 import *
from factory import *
from parser import synthesize_factory_graph

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
            res = res + "_" +  str(attr)
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



# Example use! The following factory looks like this:
"""
chest(copper) > inserter V
                    assembler(electronic-circuit)
chest(iron) > inserter ^                V
                                    inserter
                                        V
chest(iron)  >   inserter >   assembler(display-panel)
"""

solver = Optimize()

factory = Factory()

chest1 = FactoryNode('chest', prod = {"copper-cable"})
chest2 = FactoryNode('chest', prod = {"iron-plate"})

inserter1 = FactoryNode('inserter', prod = {"copper-cable"}, sources = {chest1})
inserter2 = FactoryNode('inserter', prod = {"iron-plate"}, sources = {chest2})

assembler1 = FactoryNode('assembling', prod = {"electronic-circuit"}, sources = {inserter1, inserter2})
assembler1.recipe = Recipe('electronic-circuit', 0.5, {"copper-cable":3, "iron-plate":1})

chest3 = FactoryNode('chest', prod = {"iron-plate"})

inserter3 = FactoryNode('inserter', prod = {"electronic-circuit"}, sources = {assembler1})
inserter4 = FactoryNode('inserter', prod = {"iron-plate"}, sources = {chest3})

assembler2 = FactoryNode('assembling', prod = {"display-panel"}, sources = {inserter3, inserter4})
assembler2.recipe = Recipe('display-panel', 0.5, {"electronic-circuit":1, "iron-plate":1})

factory.add_node(chest1)
factory.add_node(chest2)
factory.add_node(chest3)
factory.add_node(inserter1)
factory.add_node(inserter2)
factory.add_node(inserter3)
factory.add_node(inserter4)
factory.add_node(assembler1)
factory.add_node(assembler2)

#bp = '0eNqtVNtOwzAM/ZXKzylab7D2gR8BVKWpAUtpUpIUgab+O247tjHGtEm8JbZzjo8v2UCjB+wdmQDVBlr0ylEfyBqoQNm+RxfF99H2pGSjcbqjRhWcNaQiRU4NFPyjITZEvZYB/Z8xxkYN6uBBAClrPFQPG/D0YqSe+I3skIml99g1msxL3En1SgbjBEZ+Ylr8gCoZnwSgCRQIF4T58lmboWvQcYD4RiLzTIZdsXpFH5i1t54WeRtgqDgrbgoBn1Bld+lNMXMsL2qPIXAGfop02Nl3rAf26YAO25oCdux6ltqjgMW85LJlXkoWz/VgXmWHqcTJaiWgs+2sMsQa5ZzVXtg4il9y0gM5Hh0znRKSHwlpyXED5ogkPYGaibPlPsGQHjEwPvUHWufxgG97/TZIzYTsN9Z13OATSeQXSVvtiLOLpBVXohYXod5eMVXJEfZ/TdW0Y/8yU3fXdj9d7yTlP7u/X/R4u+jnZoBXd1LJlv3PI+Cddc5kxW1a5mVZrJOsLFf5OH4BYMmMqg=='
bp = '0eNqlkttqwzAMQP9Fz07JtSz5lTGC46itwZfMdspK8b9PTjZaujA69hhJ1tGJdIVBzTg5aQJ0V5DCGg/d6xW8PBquUsxwjdAB9x71oKQ5ZpqLkzSYFRAZSDPiB3RFfGOAJsggce2wfFx6M+sBHRWw707SHKShVCZO6AMwmKynZ9YkGrXKqmbXMLhAV+3rXbMw1he9xxBoAp8qHWp7xn6mnArocOxlQE2pA1ceGazhdZYvsrDThC6bFA9IXGHnpF3kOQNtx8UyZAr5MtVNLEb2Q6e80/HoiLQlUj+IjNKhWCuKcqNrxX793RuE8oFA/eV05yr4oJLrGu/fZ64ISHljnaYFbwxRP6WW/1GteX7/Zfv//cd0jylAwNuJMzjTSSyoZl+2dds2L0XVtnkd4ydfxgPr'
factory = synthesize_factory_graph(bp)

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
for name, var in sorted(symbs.items()):
    print(f"    {name} : {model[var]}")
