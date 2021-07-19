import Player
import resources
import Species
import operator


class Population:
    def __init__(self, size):
        self.best_player = None
        self.best_score = 0
        self.gen = 0
        self.innovation_history = []
        self.gen_players = []
        self.species = []
        self.mass_extinction_event = False
        self.new_stage = False
        self.pop = []
        for i in range(size):
            self.pop.append(Player.Player())
            self.pop[i].brain.generate_network()
            self.pop[i].brain.mutate(self.innovation_history)

    def update_alive(self):
        for i in range(len(self.pop)):
            if not self.pop[i].dead:
                self.pop[i].look()
                self.pop[i].think()
                self.pop[i].update()
                if (not resources.showNothing) and ((not resources.showBest) or i == 0):
                    self.pop[i].show()

    def done(self):
        for p in self.pop:
            if not p.dead:
                return False
        return True

    def set_best_player(self):
        temp_best = self.species[0].players[0]
        temp_best.gen = self.gen

        if temp_best.score > self.best_score:
            temp_best.stage = resources.upToStage
            self.gen_players.append(temp_best.clone_for_replay())
            print(f"old best: {self.best_score}")
            print(f"new best: {temp_best.score}")
            self.best_score = temp_best.score
            self.best_player = temp_best.clone_for_replay()

    def natural_selection(self):
        self.speciate()
        self.calculate_fitness()
        self.sort_species()
        if self.mass_extinction_event:
            self.mass_extinction()
            self.mass_extinction_event = False
        self.cull_species()
        self.set_best_player()
        self.kill_stale_species()
        self.kill_bad_species()

        print(f"generation: {self.gen} Number of mutations: {len(self.innovation_history)} species: {len(self.species)}"
              f" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        average_sum = self.get_avg_fitness_sum()
        children = []
        print("Species: ")
        for sp in self.species:
            print(f"best unadjusted fitness: {sp.best_fitness}")
            for i in range(len(sp.players)):
                print(f"player {i} fitness: {sp.players[i].fitness} score: {sp.players[i].score} ")
            print()
            children.append(sp.champ.clone_for_replay())
            no_of_children = int(sp.average_fitness / average_sum * len(self.pop)) - 1
            for _ in range(no_of_children):
                children.append(sp.give_me_baby(self.innovation_history))

        while len(children) < len(self.pop):
            children.append(self.species[0].give_me_baby(self.innovation_history))
        # self.pop.clear()
        self.pop = []
        self.pop = children.copy()
        self.gen += 1

        for p in self.pop:
            p.brain.generate_network()

        if self.new_stage:
            # import PacNeat
            resources.enter_new_stage()
            self.new_stage = False

    def speciate(self):
        for s in self.species:
            # s.players.clear()
            s.players = []
        for p in self.pop:
            species_found = False
            for s in self.species:
                if s.same_species(p.brain):
                    s.add_to_species(p)
                    species_found = True
                    break
            if not species_found:
                self.species.append(Species.Species(p))

    def calculate_fitness(self):
        for i in range(1, len(self.pop)):
            self.pop[i].calculate_fitness()

    def sort_species(self):
        for s in self.species:
            s.sort_species()

        # for i in range(len(self.species)):
        #     self.species[i].sort_species()
        #
        # temp = []
        # for i in range(len(self.species)):
        #     max_value = 0
        #     max_index = 0
        #     for j in range(len(self.species)):
        #         if self.species[j].best_fitness > max_value:
        #             max_value = self.species[j].best_fitness
        #             max_index = j
        #     temp.append(self.species[max_index])
        #     del self.species[max_index]
        #     i -= 1
        # self.species = temp.copy()

        temp = sorted(self.species, key=operator.attrgetter('best_fitness'), reverse=True)
        self.species = temp.copy()

    def kill_stale_species(self):
        j = 2
        for _ in range(2, len(self.species)):
            if self.species[j].staleness >= 15:
                del self.species[j]
                j -= 1
            j += 1

    def kill_bad_species(self):
        average_sum = self.get_avg_fitness_sum()
        j = 1
        for _ in range(1, len(self.species)):
            if (self.species[j].average_fitness / average_sum) * len(self.pop) < 1:
                del self.species[j]
                j -= 1
            j += 1

    def get_avg_fitness_sum(self):
        average_sum = 0
        for s in self.species:
            average_sum += s.average_fitness
        return average_sum

    def cull_species(self):
        for s in self.species:
            s.cull()
            s.fitness_sharing()
            s.set_average()

    def mass_extinction(self):
        # j = 5
        # for i in range(5, len(self.species)):
        #     del self.species[j]
        del self.species[5:]
