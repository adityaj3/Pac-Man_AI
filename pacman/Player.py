import pygame
import math
import resources
import PathNode
import Pacman
import Genome

vec = pygame.math.Vector2


class Player:
    def __init__(self):
        self.pacman = Pacman.Pacman()
        self.brain = Genome.Genome(13, 4)
        self.fitness = 0.0
        self.vision = [0.0]*8
        self.decision = [0.0]*4
        self.unadjusted_fitness = 0.0
        self.lifespan = 0
        self.best_score = 0
        self.dead = False
        self.score = 0
        self.gen = 0
        self.stage = 1

    def show(self):
        for i in range(28):
            for j in range(31):
                self.pacman.tiles[j][i].show()
        self.pacman.blinky.show()
        self.pacman.pinky.show()
        self.pacman.inky.show()
        self.pacman.clyde.show()
        self.pacman.show()
        pygame.display.update()

    def move(self):
        self.pacman.move()
        self.pacman.blinky.move()
        self.pacman.pinky.move()
        self.pacman.inky.move()
        self.pacman.clyde.move()

    def update(self):
        self.move()
        self.check_game_state()

    def check_game_state(self):
        if self.pacman.gameOver:
            self.dead = True
        self.score = self.pacman.score

    def look(self):
        if resources.is_critical_position(self.pacman.pos):
            self.vision = [0]*13
            self.distance_to_ghost_in_direction()
            self.set_distance_to_walls()
            self.vision[-1] = int(self.pacman.blinky.frightened)

    def distance_to_ghost_in_direction(self):
        self.pacman.blinky.set_path_nodes()
        all_nodes = self.pacman.blinky.ghost_path_nodes.copy()
        pacman_node = all_nodes[-1]
        if not self.pacman.blinky.active:
            del all_nodes[0]
        else:
            all_nodes[0].is_ghost = True

        if self.pacman.clyde.active:
            clyde_pos = resources.pixel_to_tile(self.pacman.clyde.pos)
            wall_pos = resources.get_nearest_non_wall_tile(vec(clyde_pos.x, clyde_pos.y))
            all_nodes.append(PathNode.PathNode(wall_pos.x, wall_pos.y, True))
        if self.pacman.pinky.active:
            pinky_pos = resources.pixel_to_tile(self.pacman.pinky.pos)
            wall_pos = resources.get_nearest_non_wall_tile(vec(pinky_pos.x, pinky_pos.y))
            all_nodes.append(PathNode.PathNode(wall_pos.x, wall_pos.y, True))
        if self.pacman.inky.active:
            inky_pos = resources.pixel_to_tile(self.pacman.inky.pos)
            wall_pos = resources.get_nearest_non_wall_tile(vec(inky_pos.x, inky_pos.y))
            all_nodes.append(PathNode.PathNode(wall_pos.x, wall_pos.y, True))

        for node in all_nodes:
            node.add_edges(all_nodes)

        directions = []
        for i in range(4):
            direction_i = vec(self.pacman.vel.x, self.pacman.vel.y)
            direction_i.rotate_ip(90*i)
            direction_i.x = round(direction_i.x)
            direction_i.y = round(direction_i.y)
            directions.append(direction_i)

        vision_index = -1

        for direction in directions:
            vision_index += 1
            distance = 0
            temp = pacman_node
            previous_node = pacman_node

            wrong_way = vec(-direction.x, -direction.y)
            min_val = 100
            min_index = 0
            intersection_passed = False

            while not temp.is_ghost:
                min_val = 100
                i = 0
                for edge in temp.edges:
                    node_in_direction = vec(edge.x - temp.x, edge.y - temp.y)
                    mag = math.sqrt(((edge.x - temp.x) ** 2 + (edge.y - temp.y) ** 2))
                    node_in_direction.x /= mag
                    node_in_direction.y /= mag
                    # node_in_direction.normalize_ip()
                    if node_in_direction.x == direction.x and node_in_direction.y == direction.y:
                        # dist = math.sqrt(((temp.x - edge.x)**2 + (temp.y - edge.y)**2))
                        if mag < min_val:
                            min_val = mag
                            min_index = i
                            wrong_way = vec(-node_in_direction.x, -node_in_direction.y)
                    i += 1
                if min_val == 100:
                    break
                distance += min_val
                previous_node = temp
                temp = temp.edges[min_index]
                if (not intersection_passed) and self.is_intersection(temp):
                    intersection_passed = True

            if temp.is_ghost:
                self.vision[vision_index] = 1 / distance
            else:
                if distance == 0:
                    self.vision[vision_index] = 0.0
                else:
                    if intersection_passed:
                        self.vision[vision_index] = 0.0
                    else:
                        while (not temp.is_ghost) and (not self.is_intersection(temp)):
                            min_val = 100
                            i = 0
                            for edge in temp.edges:
                                node_in_direction = vec(edge.x - temp.x, edge.y - temp.y)
                                mag = math.sqrt(((edge.x - temp.x) ** 2 + (edge.y - temp.y) ** 2))
                                node_in_direction.x /= mag
                                node_in_direction.y /= mag
                                # node_in_direction.normalize_ip()
                                if node_in_direction.x != wrong_way.x or node_in_direction.y != wrong_way.y:
                                    if edge != previous_node:
                                        # dist = math.sqrt(((temp.x - edge.x) ** 2 + (temp.y - edge.y) ** 2))
                                        if mag < min_val:
                                            min_val = mag
                                            min_index = i
                                i += 1
                            if min_val == 100:
                                print("FUCKKKKKK")
                                break

                            previous_node = temp
                            temp = temp.edges[min_index]
                            distance += min_val
                            wrong_way = vec(previous_node.x - temp.x, previous_node.y - temp.y)
                            wrong_way.normalize_ip()
                        if temp.is_ghost:
                            self.vision[vision_index] = 1 / distance
                        else:
                            self.vision[vision_index] = 0.0

    @staticmethod
    def is_intersection(n):
        left = False
        right = False
        up = False
        down = False
        count_directions = 0
        for edge in n.edges:
            if n.x < edge.x and not left:
                count_directions += 1
                left = True
            elif n.x > edge.x and not right:
                count_directions += 1
                right = True
            elif n.y < edge.y and not up:
                count_directions += 1
                up = True
            elif n.y > edge.y and not down:
                count_directions += 1
                down = True

            if count_directions > 2:
                return True
        return False

    def set_distance_to_walls(self):
        matrix_position = resources.pixel_to_tile(self.pacman.pos)
        directions = []
        for i in range(4):
            direction_i = vec(self.pacman.vel.x, self.pacman.vel.y)
            direction_i.rotate_ip(90 * i)
            direction_i.x = round(direction_i.x)
            direction_i.y = round(direction_i.y)
            directions.append(direction_i)
        vision_index = 4
        for direction in directions:
            looking_positions = vec(matrix_position.x + direction.x, matrix_position.y + direction.y)
            if resources.originalTiles[int(looking_positions.y)][int(looking_positions.x)].wall:
                self.vision[vision_index] = 1
            else:
                self.vision[vision_index] = 0

            while True:
                if resources.originalTiles[int(looking_positions.y)][int(looking_positions.x)].wall:
                    self.vision[vision_index + 4] = 0
                    break
                if self.pacman.tiles[int(looking_positions.y)][int(looking_positions.x)].dot and not \
                        self.pacman.tiles[int(looking_positions.y)][int(looking_positions.x)].eaten:
                    self.vision[vision_index + 4] = 1
                    break
                looking_positions.x += direction.x
                looking_positions.y += direction.y
            vision_index += 1

    def think(self):
        max_value = 0
        max_index = 0
        decision = self.brain.feed_forward(self.vision)

        for i in range(len(decision)):
            if decision[i] > max_value:
                max_value = decision[i]
                max_index = i

        if max_value < 0.8:
            return

        current_vel = vec(self.pacman.vel.x, self.pacman.vel.y)
        current_vel.rotate_ip(90 * max_index)
        current_vel.x = round(current_vel.x)
        current_vel.y = round(current_vel.y)
        self.pacman.turnTo = vec(current_vel.x, current_vel.y)
        self.pacman.turn = True

    def clone(self):
        cln = Player()
        cln.brain = self.brain.clone()
        cln.fitness = self.fitness
        cln.brain.generate_network()
        cln.gen = self.gen
        cln.best_score = self.score
        return cln

    def clone_for_replay(self):
        cln = Player()
        cln.brain = self.brain.clone()
        cln.fitness = self.fitness
        cln.brain.generate_network()
        cln.pacman.blinky.frightenedTurns = self.pacman.blinky.frightened_turns.copy()
        cln.pacman.blinky.replay = True
        cln.pacman.pinky.frightenedTurns = self.pacman.pinky.frightened_turns.copy()
        cln.pacman.pinky.replay = True
        cln.pacman.inky.frightenedTurns = self.pacman.inky.frightened_turns.copy()
        cln.pacman.inky.replay = True
        cln.pacman.clyde.frightenedTurns = self.pacman.clyde.frightened_turns.copy()
        cln.pacman.clyde.replay = True
        cln.pacman.replay = True
        cln.gen = self.gen
        cln.bestScore = self.score
        cln.stage = self.stage
        return cln

    def calculate_fitness(self):
        self.score = self.pacman.score
        self.best_score = self.score
        self.lifespan = self.pacman.lifespan
        self.fitness = self.score * self.score

    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generate_network()
        return child
