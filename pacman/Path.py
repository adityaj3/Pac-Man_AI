import pygame
import resources
import collections
vec = pygame.math.Vector2


class Path:
    def __init__(self):
        self.path = collections.deque()
        self.distance = 0
        self.dist_to_finish = 0
        self.vel_at_last = None

    def add_to_tail(self, n, end_path_node):
        if self.path:
            v1 = vec(self.path[-1].x, self.path[-1].y)
            v2 = vec(n.x, n.y)
            self.distance += v1.distance_to(v2)
        self.path.append(n)
        v1 = vec(self.path[-1].x, self.path[-1].y)
        v2 = vec(end_path_node.x, end_path_node.y)
        self.dist_to_finish += v1.distance_to(v2)

    def clone(self):
        temp = Path()
        temp.path = self.path.copy()
        temp.distance = self.distance
        temp.dist_to_finish = self.dist_to_finish
        temp.vel_at_last = vec(self.vel_at_last.x, self.vel_at_last.y)
        return temp

    def clear(self):
        self.distance = 0
        self.dist_to_finish = 0
        # self.path.clear()
        self.path = collections.deque()

    def show(self, colour):
        flag = True
        x0, y0 = 0, 0
        for path_i in self.path:
            if flag:
                x0, y0 = path_i.x, path_i.y
                flag = False
                continue
            x1, y1 = path_i.x, path_i.y
            prev = resources.tile_to_pixel(x0, y0)
            curr = resources.tile_to_pixel(x1, y1)
            pygame.draw.line(resources.SCREEN, colour, prev, curr, 3)
            x0, y0 = x1, y1
        pygame.draw.circle(resources.SCREEN, colour, (x0, y0), 3)
        # pygame.display.update()
