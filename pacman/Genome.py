import pygame
import resources
import Node
import connectionGene
import connectionHistory
import random

vec = pygame.math.Vector2


class Genome:
    def __init__(self, ins, outs, crossover=False):
        self.inputs = ins
        self.outputs = outs
        self.genes = []
        self.nodes = []
        self.layers = 2
        self.next_node = 0
        self.bias_node = None
        self.network = []

        if not crossover:
            for i in range(self.inputs):
                self.nodes.append(Node.Node(i))
                self.next_node += 1
                self.nodes[i].layer = 0

            for i in range(self.outputs):
                self.nodes.append(Node.Node(i + self.inputs))
                self.nodes[i + self.inputs].layer = 1
                self.next_node += 1

            self.nodes.append(Node.Node(self.next_node))
            self.bias_node = self.next_node
            self.next_node += 1
            self.nodes[self.bias_node].layer = 0

    def get_node(self, node_num):
        for node in self.nodes:
            if node.number == node_num:
                return node
        return None

    def connect_nodes(self):
        for node in self.nodes:
            node.output_connections.clear()
            # node.output_connections = []
        for gene in self.genes:
            gene.from_node.output_connections.append(gene)

    def feed_forward(self, input_values):
        for i in range(self.inputs):
            self.nodes[i].output_value = input_values[i]
        self.nodes[self.bias_node].output_value = 1
        for nw in self.network:
            nw.engage()
        outs = []
        for i in range(self.outputs):
            outs.append(self.nodes[self.inputs + i].output_value)
        for node in self.nodes:
            node.input_sum = 0
        return outs

    def generate_network(self):
        self.connect_nodes()
        network = []
        for layer in range(self.layers):
            for node in self.nodes:
                if node.layer == layer:
                    network.append(node)

    def add_node(self, innovation_history):
        if len(self.genes) == 0:
            self.add_connection(innovation_history)
            return
        random_connection = random.randint(0, len(self.genes) - 1)

        while self.genes[random_connection].from_node == self.nodes[self.bias_node] and len(self.genes) != 1:
            random_connection = random.randint(0, len(self.genes) - 1)

        self.genes[random_connection].enabled = False

        new_node_num = self.next_node
        self.nodes.append(Node.Node(new_node_num))
        self.next_node += 1

        connection_innovation_num = self.get_innovation_num(innovation_history,
                                                            self.genes[random_connection].from_node,
                                                            self.get_node(new_node_num))
        self.genes.append(connectionGene.ConnectionGene(self.genes[random_connection].from_node,
                                                        self.get_node(new_node_num),
                                                        1,
                                                        connection_innovation_num))

        connection_innovation_num = self.get_innovation_num(innovation_history,
                                                            self.get_node(new_node_num),
                                                            self.genes[random_connection].to_node)
        self.genes.append(connectionGene.ConnectionGene(self.get_node(new_node_num),
                                                        self.genes[random_connection].to_node,
                                                        self.genes[random_connection].weight,
                                                        connection_innovation_num))
        self.get_node(new_node_num).layer = self.genes[random_connection].from_node.layer + 1

        connection_innovation_num = self.get_innovation_num(innovation_history,
                                                            self.nodes[self.bias_node],
                                                            self.get_node(new_node_num))
        self.genes.append(connectionGene.ConnectionGene(self.nodes[self.bias_node],
                                                        self.get_node(new_node_num),
                                                        0,
                                                        connection_innovation_num))

        if self.get_node(new_node_num).layer == self.genes[random_connection].to_node.layer:
            for i in range(len(self.nodes) - 1):
                if self.nodes[i].layer >= self.get_node(new_node_num).layer:
                    self.nodes[i].layer += 1
            self.layers += 1
        self.connect_nodes()

    def add_connection(self, innovation_history):
        if self.fully_connected():
            print("connection failed")
            return

        random_node1 = random.randint(0, len(self.nodes)-1)
        random_node2 = random.randint(0, len(self.nodes)-1)
        while self.random_connection_nodes_are_shit(random_node1, random_node2):
            random_node1 = random.randint(0, len(self.nodes)-1)
            random_node2 = random.randint(0, len(self.nodes)-1)
        if self.nodes[random_node1].layer > self.nodes[random_node2].layer:
            temp = random_node2
            random_node2 = random_node1
            random_node1 = temp

        connection_innovation_num = self.get_innovation_num(innovation_history, self.nodes[random_node1],
                                                            self.nodes[random_node2])

        self.genes.append(connectionGene.ConnectionGene(self.nodes[random_node1], self.nodes[random_node2],
                                                        random.uniform(-1, 1), connection_innovation_num))
        self.connect_nodes()

    def random_connection_nodes_are_shit(self, r1, r2):
        if self.nodes[r1].layer == self.nodes[r2].layer:
            return True
        if self.nodes[r1].is_connected_to(self.nodes[r2]):
            return True
        if r1 < self.inputs and (r1 > resources.usingInputsEnd or r1 < resources.usingInputsStart):
            return True
        if r2 < self.inputs and (r2 > resources.usingInputsEnd or r2 < resources.usingInputsStart):
            return True

        return False

    def get_innovation_num(self, innovation_history, from_node, to_node):
        is_new = True
        connection_innovation_num = resources.nextConnectionNo
        for innovation_node in innovation_history:
            if innovation_node.matches(self, from_node, to_node):
                is_new = False
                connection_innovation_num = innovation_node.innovation_num
                break
        if is_new:
            inno_nums = []
            for gene in self.genes:
                inno_nums.append(gene.innovation_num)

            innovation_history.append(connectionHistory.ConnectionHistory(from_node.number, to_node.number,
                                                                          connection_innovation_num, inno_nums))
            resources.nextConnectionNo += 1
        return connection_innovation_num

    def fully_connected(self):
        max_connections = 0
        nodes_in_layers = [0] * int(self.layers)
        nodes_in_layers[0] = resources.usingInputsEnd - resources.usingInputsStart + 1 + 1

        for i in range(1, len(self.nodes)):
            nodes_in_layers[self.nodes[i].layer] += 1

        for i in range(self.layers - 1):
            nodes_in_front = 0
            for j in range(i + 1, self.layers):
                nodes_in_front += nodes_in_layers[j]
            max_connections += nodes_in_layers[i] * nodes_in_front

        if max_connections == len(self.genes):
            return True
        return False

    def mutate(self, innovation_history):
        if len(self.genes) == 0:
            self.add_connection(innovation_history)

        rand1 = random.random()
        if rand1 < 0.8:
            for gene in self.genes:
                gene.mutate_weight()

        rand2 = random.random()
        if rand2 < 0.08:
            self.add_connection(innovation_history)

        rand3 = random.random()
        if rand3 < 0.02:
            self.add_node(innovation_history)

    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)
        child.genes.clear()
        # child.genes = []
        child.nodes.clear()
        # child.nodes = []
        child.layers = self.layers
        child.next_node = self.next_node
        child.bias_node = self.bias_node
        child_genes = []
        is_enabled = []

        for gene in self.genes:
            set_enabled = True
            parent2gene = self.matching_gene(parent2, gene.innovation_num)
            if parent2gene != -1:
                if (not gene.enabled) or (not parent2.genes[parent2gene].enabled):
                    if random.random() < 0.75:
                        set_enabled = False
                rand = random.random()
                if rand < 0.5:
                    child_genes.append(gene)
                else:
                    child_genes.append(parent2.genes[parent2gene])
            else:
                child_genes.append(gene)
                set_enabled = gene.enabled
            is_enabled.append(set_enabled)

        for node in self.nodes:
            child.nodes.append(node.clone())

        for i in range(len(child_genes)):
            child.genes.append(child_genes[i].clone(child.get_node(child_genes[i].from_node.number),
                                                    child.get_node(child_genes[i].to_node.number)))
            child.genes[i].enabled = is_enabled[i]
        child.connect_nodes()
        return child

    @staticmethod
    def matching_gene(parent2, innovation_num):
        for i in range(len(parent2.genes)):
            if parent2.genes[i].innovation_num == innovation_num:
                return i
        return -1

    def print_genome(self):
        print(f"Print genome  layers: {self.layers}")
        print(f"bias node: {self.bias_node}")
        print("nodes")
        for node in self.nodes:
            print(node.number, end=", ")
        print("Genes")
        for gene in self.genes:
            print(f"gene {gene.innovation_num} From node {gene.from_node.number}To Node {gene.to_node.number} is "
                  f"enabled {gene.enabled} from layer {gene.from_node.layer} to layer {gene.to_node.layer} w"
                  f"eight {gene.weight} ")
        print()

    def clone(self):
        cln = Genome(self.inputs, self.outputs, True)
        for node in self.nodes:
            cln.nodes.append(node.clone())
        for gene in self.genes:
            cln.genes.append(gene.clone(cln.get_node(gene.from_node.number), cln.get_node(gene.to_node.number)))
        cln.layers = self.layers
        cln.next_node = self.next_node
        cln.bias_node = self.bias_node
        cln.connect_nodes()
        return cln

    def draw_genome(self, start_x, start_y, w, h):
        all_nodes = []
        node_poses = []
        node_nums = []

        for i in range(self.layers):
            temp = []
            for node in self.nodes:
                if node.layer == i:
                    temp.append(node)
            all_nodes.append(temp)

        index_of_node_nums = {}
        k = 0
        for i in range(self.layers):
            x = start_x + (((i + 1) * w) / (self.layers + 1))
            for j in range(len(all_nodes[i])):
                y = start_y + (((j + 1) * h) / (len(all_nodes[i]) + 1))
                node_poses.append(vec(x, y))
                node_nums.append(int(all_nodes[i][j].number))
                # if int(all_nodes[i][j].number) not in index_of_node_nums:
                index_of_node_nums[int(all_nodes[i][j].number)] = k
                k += 1

        line_color = (255, 255, 255)
        for gene in self.genes:
            if gene.enabled:
                line_color = (255, 255, 255)
            else:
                line_color = (100, 100, 100)
            from_pos = node_poses[index_of_node_nums[gene.from_node.number]]
            to_pos = node_poses[index_of_node_nums[gene.to_node.number]]
            if gene.weight > 0:
                line_color = (255, 0, 0)
            else:
                line_color = (0, 0, 255)
            scaled_weight = int(abs(gene.weight) * 5)  # ((gene.weight - 0)/(1 - 0))*(5 - 0) + 0
            pygame.draw.line(resources.SCREEN, line_color, (from_pos.x, from_pos.y), (to_pos.x, to_pos.y),
                             scaled_weight)

        for i in range(len(node_poses)):
            pygame.draw.circle(resources.SCREEN, (255, 255, 255), (node_poses[i].x, node_poses[i].y), 10)
            font = pygame.font.SysFont("monaco", 16)
            txt = font.render(f"{node_nums[i]}", True, (0, 0, 0))
            resources.SCREEN.blit(txt, (node_poses[i].x - 6, node_poses[i].y - 5))
        # pygame.display.update()
