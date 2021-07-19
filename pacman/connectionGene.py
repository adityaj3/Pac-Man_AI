import random


class ConnectionGene:
    def __init__(self, from_node, to_node, w, i_num):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = w
        self.enabled = True
        self.innovation_num = i_num

    def mutate_weight(self):
        rand2 = random.random()
        if rand2 < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight = random.normalvariate(0, 1) / 50
            if self.weight > 1:
                self.weight = 1
            elif self.weight < -1:
                self.weight = -1

    def clone(self, from_node, to_node):
        cln = ConnectionGene(from_node, to_node, self.weight, self.innovation_num)
        cln.enabled = self.enabled
        return cln
