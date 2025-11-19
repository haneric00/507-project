from z3 import *

def factory_to_constraints(solver, factory):
    """
    Parses the given factory, adding constraints to the given solver.
    solver - solver to add constraints to
    factory - factory to parse constraints from
    """

    # Loop through all factory nodes and create necessary symbolic variables.
    # Store names in a dictionary for access later.
    def prod_symb_name(node, item):
        """
        Helper for converting a node and item to the symbolic variable name.
        """
        return str(node.id) + "_" + item + "_p"
    symbs = {}
    for node in factory.nodes:
        if node.name == "inserter" or node.name == "assembler":
            # Every item produced requires its own symbolic production rate.
            for item in node.items_produced:
                symb = prod_symb_name(node, item)
                symbs[symb] = Real(symb)

    # Add constraints for all factory nodes to the solver.
    for node in factory.nodes:
        match node.name:
            case "chest":
                continue # Chests do not add constraints.
            case "inserter":
                # For every item that the inserter that can produce, two
                # clauses are added:
                # 1. A disjunction of all possible throughputs, including max
                #   speed settings and the input production rate of the item.
                # 2. An inequality limiting the inserters throughput to at most
                #   the input production rate of the item.

                # Assemble possible throughput values.
                throughput_clauses = []

                # TODO: assuming one source! update if this changes.
                for item in node.sources[0].items_produced:
                    # TODO: update INSERTER_THROUGHPUTS, match real const name
                    for throughput in INSERTER_THROUGHPUTS:
                        # TODO: finish implementing this
                        pass

            case "assembler":
                # Assemblers produce only one item, therefore only constraints
                # for that item need to be enforced. These are:
                # 1. A disjunction of all possible assembler throughputs, given
                #   the time needed for the assembler's recipe and possible
                #   speed settings for assemblers.
                # 2. For every item in the assembler's recipe, an inequality
                #   mandating the input production rate of that item >= the
                #   overall assembler production rate.
                pass
            case name:
                raise Exception(f"Invalid node type in factory: {name}")

    # Add optimization constraints to all production symbolic variables.
    # TODO: finish this.

solver = Optimize()
