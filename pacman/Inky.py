import pygame
import collections
import random
import math
import resources
import Path
import PathNode
# import Pacman

vec = pygame.math.Vector2


class Inky:
    def __init__(self, pac):
        self.pacman = pac
        self.pos = vec(resources.tile_to_pixel(23, 26))
        self.vel = vec(1, 0)
        self.best_path = None  # Path.Path()
        self.ghost_path_nodes = []
        self.start = None  # PathNode.PathNode()
        self.end = None  # PathNode.PathNode()
        self.colour = (135, 206, 250)
        self.chase = True
        self.frightened = False
        self.flash_count = 0
        self.chase_count = 0
        self.return_home = False
        self.dead_for_a_bit = False
        self.dead_count = 0
        self.active = resources.inkyActive
        self.replay = False
        self.frightened_turns = []
        self.up_to_index = 0
        self.set_path()

    def update(self):
        self.chase_count += 1
        if self.chase:
            if self.chase_count > 1500:
                self.chase = False
                self.chase_count = 0
        else:
            if self.chase_count > 800:
                self.chase = True
                self.chase_count = 0

        if self.dead_for_a_bit:
            self.dead_count += 1
            if self.dead_count > 400:
                self.dead_for_a_bit = False
        else:
            if self.frightened:
                self.flash_count += 1
                if self.flash_count > 1000:
                    self.frightened = False
                    self.flash_count = 0

    def show(self):
        if self.active:
            if not self.dead_for_a_bit:
                sprite = resources.inkySprite2
                if not self.frightened:
                    if self.return_home:
                        sprite = resources.deadSprite2.copy()
                        sprite.set_alpha(127)
                    else:
                        sprite = resources.inkySprite2
                    # self.best_path.show(self.colour)
                else:
                    if (self.flash_count // 30) % 2 == 0:
                        sprite = resources.frightenedSprite_2
                    else:
                        sprite = resources.frightenedSprite_
                resources.SCREEN.blit(sprite, (self.pos.x - 8, self.pos.y - 8))
                # pygame.display.update()

    def move(self):
        if self.active:
            if not self.dead_for_a_bit:
                self.pos.x += 2 * self.vel.x
                self.pos.y += 2 * self.vel.y

                self.check_direction()
            self.update()

    def set_path(self):
        self.ghost_path_nodes.clear()
        # self.ghost_path_nodes = []
        self.set_path_nodes()
        self.start = self.ghost_path_nodes[0]
        self.end = self.ghost_path_nodes[-1]
        temp = self.AStar(self.start, self.end, self.vel)
        if temp is not None:
            self.best_path = temp.clone()

    def set_path_nodes(self):
        pos_tile = resources.pixel_to_tile(self.pos)
        self.ghost_path_nodes.append(PathNode.PathNode(pos_tile.x, pos_tile.y))
        for i in range(1, 27):
            for j in range(1, 30):
                if not resources.originalTiles[j][i].wall:
                    if (not resources.originalTiles[j - 1][i].wall) or (not resources.originalTiles[j + 1][i].wall):
                        if (not resources.originalTiles[j][i - 1].wall) or (not resources.originalTiles[j][i + 1].wall):
                            self.ghost_path_nodes.append(PathNode.PathNode(i, j))
        if self.return_home:
            self.ghost_path_nodes.append(PathNode.PathNode(13, 11))
        else:
            if self.chase:
                pacman_pos_tile = resources.pixel_to_tile(self.pacman.pos)
                blinky_pos_tile = resources.pixel_to_tile(self.pacman.blinky.pos)
                blinky_to_pacman = vec(pacman_pos_tile.x - blinky_pos_tile.x, pacman_pos_tile.y - blinky_pos_tile.y)

                target = vec(pacman_pos_tile.x + blinky_to_pacman.x, pacman_pos_tile.y + blinky_to_pacman.y)
                nearest_tile = resources.get_nearest_non_wall_tile(target)
                if nearest_tile.distance_to(pos_tile) < 1:
                    self.ghost_path_nodes.append(PathNode.PathNode(pacman_pos_tile.x, pacman_pos_tile.y))
                else:
                    self.ghost_path_nodes.append(PathNode.PathNode(nearest_tile.x, nearest_tile.y))
            else:
                self.ghost_path_nodes.append(PathNode.PathNode(26, 29))
        for node in self.ghost_path_nodes:
            node.add_edges(self.ghost_path_nodes)

    def check_direction(self):
        if self.pacman.hit_pacman(self.pos):
            if self.frightened:
                self.return_home = True
                self.frightened = False
            elif not self.return_home:
                self.pacman.kill()
        if self.return_home:
            tile_pos = resources.pixel_to_tile(self.pos)
            if tile_pos.distance_to(vec(13, 11)) < 1:
                self.return_home = False
                self.dead_for_a_bit = True
                self.dead_count = 0
        if resources.is_critical_position(self.pos):
            matrix_position = resources.pixel_to_tile(self.pos)
            is_path_node = False
            for node in self.ghost_path_nodes:
                if matrix_position.x == node.x and matrix_position.y == node.y:
                    is_path_node = True
                    break
            if not is_path_node:
                return
            if self.frightened:
                new_vel = None
                rand = random.randint(0, 3)
                if self.replay and self.up_to_index < len(self.frightened_turns):
                    rand = self.frightened_turns[self.up_to_index]
                    self.up_to_index += 1

                if rand == 0:
                    new_vel = vec(1, 0)
                elif rand == 1:
                    new_vel = vec(0, 1)
                elif rand == 2:
                    new_vel = vec(-1, 0)
                elif rand == 3:
                    new_vel = vec(0, -1)

                while resources.originalTiles[int(matrix_position.y + new_vel.y)][
                    int(matrix_position.x + new_vel.x)].wall or (
                        new_vel.x + 2 * self.vel.x == 0 and new_vel.y + 2 * self.vel.y == 0):
                    rand = random.randint(0, 3)
                    if rand == 0:
                        new_vel = vec(1, 0)
                    elif rand == 1:
                        new_vel = vec(0, 1)
                    elif rand == 2:
                        new_vel = vec(-1, 0)
                    elif rand == 3:
                        new_vel = vec(0, -1)

                if not self.replay:
                    self.frightened_turns.append(rand)
                self.vel = vec(new_vel.x / 2, new_vel.y / 2)
            else:
                self.set_path()
                flag = False
                for path_i in self.best_path.path:
                    if flag:
                        self.vel = vec(path_i.x - matrix_position.x, path_i.y - matrix_position.y)
                        self.vel.x *= 100
                        self.vel.y *= 100
                        self.vel.normalize_ip()
                        # mag = self.vel.magnitude() self.vel.x /= mag self.vel.y /= mag
                        return

                    if matrix_position.x == path_i.x and matrix_position.y == path_i.y:
                        flag = True

    @staticmethod
    def AStar(start, finish, vel):
        big = collections.deque()
        extend = Path.Path()
        winning_path = Path.Path()
        extended = Path.Path()
        sorting = collections.deque()

        extend.add_to_tail(start, finish)
        extend.vel_at_last = vec(vel.x, vel.y)
        big.append(extend)

        winner = False

        while True:
            extend = big.popleft()
            if extend.path[-1] == finish:
                if not winner:
                    winner = True
                    winning_path = extend.clone()
                elif winning_path.distance > extend.distance:
                    winning_path = extend.clone()
                if big:
                    extend = big.popleft()
                else:
                    return winning_path.clone()

            if (not extend.path[-1].checked) or extend.distance < extend.path[-1].smallest_dist_to_point:
                dist = math.sqrt(((extend.path[-1].x - finish.x) ** 2 + (extend.path[-1].y - finish.y) ** 2))
                if (not winner) or extend.distance + dist < winning_path.distance:
                    extend.path[-1].smallest_dist_to_point = extend.distance
                    sorting = big.copy()
                    temp_n = PathNode.PathNode(0, 0)
                    if len(extend.path) > 1:
                        temp_n = extend.path[len(extend.path) - 2]
                    for edge in extend.path[-1].edges:
                        if temp_n != edge:
                            direction_to_path_node = vec(edge.x - extend.path[-1].x, edge.y - extend.path[-1].y)
                            mag = vel.magnitude()
                            direction_to_path_node.normalize_ip()
                            direction_to_path_node.x *= mag
                            direction_to_path_node.y *= mag
                            if not (direction_to_path_node.x == -1 * extend.vel_at_last.x and
                                    direction_to_path_node.y == -1 * extend.vel_at_last.y):
                                extended = extend.clone()
                                extended.add_to_tail(edge, finish)
                                extended.vel_at_last = vec(direction_to_path_node.x, direction_to_path_node.y)
                                sorting.append(extended.clone())
                    big.clear()
                    # big = collections.deque()
                    while len(sorting) != 0:
                        max_val = -1
                        i_max = 0
                        i = 0
                        for path in sorting:
                            if max_val < path.distance + path.dist_to_finish:
                                i_max = i
                                max_val = path.distance + path.dist_to_finish
                            i += 1
                        temp = sorting[i_max].clone()
                        del sorting[i_max]
                        big.appendleft(temp)
                extend.path[-1].checked = True
            if len(big) == 0:
                if not winner:
                    return None
                else:
                    return winning_path.clone()
