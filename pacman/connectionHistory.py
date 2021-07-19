class ConnectionHistory:
    def __init__(self, from_node, to_node, i_num, i_nums):
        self.from_node = from_node
        self.to_node = to_node
        self.innovation_num = i_num
        self.innovation_nums = i_nums.copy()

    def matches(self, genome, from_node, to_node):
        if len(genome.genes) == len(self.innovation_nums):
            if from_node.number == self.from_node and to_node.number == self.to_node:
                for gene in genome.genes:
                    if gene.innovation_num not in self.innovation_nums:
                        return False
                return True
        return False
