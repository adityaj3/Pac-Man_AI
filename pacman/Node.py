import math


class Node:
    def __init__(self, n):
        self.number = n
        self.input_sum = 0
        self.output_value = 0
        self.output_connections = []
        self.layer = 0
        self.draw_pos = None

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-4.9 * x))

    def engage(self):
        if self.layer != 0:
            self.output_value = self.sigmoid(self.input_sum)
        for connection in self.output_connections:
            if connection.enabled:
                connection.to_node.input_sum += connection.weight * self.output_value

    @staticmethod
    def step_function(x):
        if x < 0:
            return 0
        else:
            return 1

    def is_connected_to(self, node):
        if node.layer == self.layer:
            return False
        if node.layer < self.layer:
            for node_i in self.output_connections:
                if node_i.to_node == self:
                    return True
        else:
            for node_i in self.output_connections:
                if node_i.to_node == node:
                    return True
        return False

    def clone(self):
        cln = Node(self.number)
        cln.layer = self.layer
        return cln

