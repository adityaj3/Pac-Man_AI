import pygame
import resources
import collections


class PathNode:
    def __init__(self, x, y, is_ghost=False):
        self.edges = collections.deque()
        self.x = x
        self.y = y
        self.smallest_dist_to_point = 10000000
        self.degree = None  # 0
        self.value = None  # 0
        self.checked = False
        self.is_ghost = is_ghost

    def show(self):
        pixel = resources.tile_to_pixel(self.x, self.y)
        pygame.draw.circle(resources.SCREEN, (0, 100, 100), (pixel[0], pixel[1]), 5)
        # pygame.display.update()

    def add_edges(self, nodes):
        for node in nodes:
            if (node.y == self.y) ^ (node.x == self.x):
                if node.y == self.y:
                    most_left = min(node.x, self.x) + 1
                    max_val = max(node.x, self.x)
                    edge = True
                    while most_left < max_val:
                        if resources.originalTiles[int(self.y)][int(most_left)].wall:
                            edge = False
                            break
                        most_left += 1
                    if edge:
                        self.edges.append(node)
                elif node.x == self.x:
                    most_up = min(node.y, self.y) + 1
                    max_val = max(node.y, self.y)
                    edge = True
                    while most_up < max_val:
                        if resources.originalTiles[int(most_up)][int(self.x)].wall:
                            edge = False
                            break
                        most_up += 1
                    if edge:
                        self.edges.append(node)

    def clone(self):
        cln = PathNode(self.x, self.y)
        cln.is_ghost = self.is_ghost
        return cln
