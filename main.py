
class GraphConverter:
    def node_to_constraints(self, node):
        """
        Returns a list of constraints based on this graph node.
        """
    
        # If this is a...
        # source:
        # - create symbolic variable node.p
        # - return a single constraint: node.p = source_production_rate
        # inserter:
        # - create symbolic variable node.p
        # - emit a disjunction node.p = spd for every possible inserter 
        #   speed spd
        # - emit an inequality: node.p <= node.src[0].p
        #   note the assumption that inserter nodes have a single src.
        #   it is important that node.src[0].p is actually the existing
        #   symbolic variable for that quantity.
        # assembler:
        # - create fresh symbolic variable node.p
        # - create fresh symbolic variable node.asm.s
        # - emit node.p = node.asm.s / node.asm.recipe.t
        # - emit a disjunction node.asm.s = spd for every possible
        #   assembler speed spd
        # - for every ingredient q_i in node's recipe, emit the
        #   inequality (aggregate production rate of q_i from
        #   node.sources) >= node.asm.recipe.q_i * node.asm.s /
        #   node.asm.recipe.t
        #   note that node.asm.recipe.q_i and node.asm.recipe.t are
        #   static quantities. again, aggregate production rate
        #   calculation should use existing symbolic variables.
    
        pass
