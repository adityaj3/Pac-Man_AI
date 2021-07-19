import pygame
import resources
vec = pygame.math.Vector2


class Tile:
    def __init__(self, x, y):
        self.wall = False
        self.dot = False
        self.bigDot = False
        self.eaten = False
        self.pos = (x, y)

    def show(self):
        if self.dot:
            if not self.eaten:
                pygame.draw.rect(resources.SCREEN, (255, 255, 0), (self.pos[0] - 1, self.pos[1] - 1, 2, 2))
        elif self.bigDot:
            if not self.eaten:
                if resources.bigDotsActive:
                    pygame.draw.rect(resources.SCREEN, (255, 255, 0), (self.pos[0] - 2, self.pos[1] - 2, 5, 5))
                else:
                    pygame.draw.rect(resources.SCREEN, (255, 255, 0), (self.pos[0] - 1, self.pos[1] - 1, 2, 2))
        # pygame.display.update()

    def clone(self):
        cln = Tile(self.pos[0], self.pos[1])
        cln.wall = self.wall
        cln.dot = self.dot
        cln.bigDot = self.bigDot
        cln.eaten = self.eaten
        return cln
