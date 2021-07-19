import operator
import random


class Species:
    def __init__(self, p):
        self.average_fitness = 0.0
        self.staleness = 0
        self.excess_coeff = 1
        self.weight_diff_coeff = 0.5
        self.compatibility_threshold = 3
        self.players = []

        self.players.append(p)
        self.best_fitness = p.fitness
        self.rep = p.brain.clone()
        self.champ = p.clone_for_replay()

    def same_species(self, g):
        excess_and_disjoint = self.get_excess_disjoint(g, self.rep)
        average_weight_diff = self.get_average_weight_diff(g, self.rep)

        large_genome_normalizer = len(g.genes) - 20
        if large_genome_normalizer < 1:
            large_genome_normalizer = 1

        compatibility = (self.excess_coeff * excess_and_disjoint / large_genome_normalizer) + (self.weight_diff_coeff *
                                                                                               average_weight_diff)
        return self.compatibility_threshold > compatibility

    def add_to_species(self, p):
        self.players.append(p)

    @staticmethod
    def get_excess_disjoint(brain1, brain2):
        matching = 0.0
        for gene1 in brain1.genes:
            for gene2 in brain2.genes:
                if gene1.innovation_num == gene2.innovation_num:
                    matching += 1
                    break
        return len(brain1.genes) + len(brain2.genes) - 2 * matching

    @staticmethod
    def get_average_weight_diff(brain1, brain2):
        if len(brain1.genes) == 0 or len(brain2.genes) == 0:
            return 0

        matching = 0
        total_diff = 0
        for gene1 in brain1.genes:
            for gene2 in brain2.genes:
                if gene1.innovation_num == gene2.innovation_num:
                    matching += 1
                    total_diff += abs(gene1.weight - gene2.weight)
                    break
        if matching == 0:
            return 100
        return total_diff / matching

    def sort_species(self):
        # temp = []
        # for i in range(len(self.players)):
        #     max_value = 0
        #     max_index = 0
        #     for j in range(len(self.players)):
        #         if self.species[j].fitness > max_value:
        #             max_value = self.species[j].fitness
        #             max_index = j
        #     temp.append(self.players[max_index])
        #     del self.players[max_index]
        #     i -= 1

        # self.players = temp.copy()

        temp = sorted(self.players, key=operator.attrgetter('fitness'), reverse=True)
        self.players = temp.copy()

        if len(self.players) == 0:
            print("fucking")
            self.staleness = 200
            return

        if self.players[0].fitness > self.best_fitness:
            self.staleness = 0
            self.best_fitness = self.players[0].fitness
            self.rep = self.players[0].brain.clone()
            self.champ = self.players[0].clone_for_replay()
        else:
            self.staleness += 1

    def set_average(self):
        fitness_sum = 0
        for p in self.players:
            fitness_sum += p.fitness
        self.average_fitness = fitness_sum / len(self.players)

    def give_me_baby(self, innovation_history):
        baby = None
        if random.random() < 0.25:
            baby = self.select_player().clone()
        else:
            parent1 = self.select_player()
            parent2 = self.select_player()

            if parent1.fitness < parent2.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby = parent1.crossover(parent2)
        baby.brain.mutate(innovation_history)
        return baby

    def select_player(self):
        fitness_sum = 0
        for p in self.players:
            fitness_sum += p.fitness
        rand = random.uniform(0, fitness_sum)
        running_sum = 0

        for p in self.players:
            running_sum += p.fitness
            if running_sum > rand:
                return p

        return self.players[0]

    def cull(self):
        if len(self.players) > 2:
            # j = len(self.players)//2
            # for _ in range(len(self.players)//2, len(self.players)):
            #     del self.players[j]
            del self.players[len(self.players)//2:]

    def fitness_sharing(self):
        for p in self.players:
            p.fitness /= len(self.players)
