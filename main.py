from z3 import *

def factory_to_constraints(solver, factory):
    """
    Parses the given factory, adding constraints to the given solver.
    solver - solver to add constraints to
    factory - factory to parse constraints from
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
            res = res + attr
        return res


    # Loop through all factory nodes and create necessary symbolic variables.
    # Store names in a dictionary for access later.
    symbs = {}
    for node in factory.nodes:
        if node.name == "inserter" or node.name == "assembler":
            # Every item produced requires its own symbolic production rate.
            for item in node.items_produced:
                symb = to_symb_name(node, item, "p")
                symbs[symb] = Real(symb)

            # Each has a speed setting.
            symb = to_symb_name(node, "s")
            symbs[symb] = Real(symb)

            # Add optimization constraints to all speed symbolic variables.
            # TODO: is this the right way to do this? alternative is minimize
            # sum of all speed symbolic variables.
            solver.minimize(symbs[symb])


    # Add constraints for all factory nodes to the solver.
    for node in factory.nodes:
        match node.name:
            case "chest":
                continue # Chests do not add constraints.
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
                #   setting or the input production rate of the item.
                # 2. An inequality limiting the inserter's throughput to at
                #   most the input production rate of the item.
                # 3. An inequality limiting the inserter's throughput to at 
                #   most the speed setting of the inserter.
                # Together these encode the constraint that the inserter's
                # throughput for the item is the minimum between these two
                # values.
                # NOTE: the items produced by an inserter's sources are equal
                # to the items produced by all its sources. Currently I assume
                # an inserter has a single source.
                for item in node.items_produced:
                    symb_inserter_item_prod = symbs[to_symb_name(node, "s")]

                    # NOTE: if assuming more than one source, need to aggregate
                    # input production for clauses.
                    for source in node.sources:
                        symb_source_item_prod = (
                                symbs[to_symb_name(source, item, "p")])
                                

                        
                        solver.add(Or(
                            symb_inserter_item_prod == symb_source_item_prod,
                            symb_inserter_item_prod == symb_inserter_spd
                            ))
                        
                        solver.add(
                            symb_inserter_item_prod <= symb_source_item_prod
                            )

                        solver.add(
                            symb_inserter_item_prod <= symb_inserter_spd
                            )


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
                # TODO: update node.recipe.item with correct name
                symb_asm_prod = (
                        symbs[to_symb_name(node, node.recipe.item, "p")])
                solver.add(symb_asm_prod == symb_asm_spd / node.recipe.time)

                # For every item in the assembler's recipe, create an
                # inequality mandating the input production rate of that item >=
                # the overall assembler production rate of recipe item *
                # ingredient count per recipe.
                for ingredient, count in node.recipe.quantities:
                    # Determine the aggregate input production rate for this
                    # item.

                    # for each source, if symbol corresponding to source's prod
                    # of this ingredient exists, add to list of input sources.
                    ingredient_inputs = []
                    for source in node.sources:
                        source_ingredient_prod_str = (
                                to_symb_name(source, ingredient, "p"))
                        if source_ingredient_prod_str in symbs:
                            item_inputs.append(
                                    symbs[source_ingredient_prod_str])

                    solver.add(Sum(ingredient_inputs) >= symb_asm_prod * count)


            case name:
                raise Exception(f"Invalid node type in factory: {name}")


solver = Optimize()
