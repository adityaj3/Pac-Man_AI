import pygame
import resources
import Blinky
import Pinky
import Inky
import Clyde

# import Tile
# import math

vec = pygame.math.Vector2


class Pacman:
    def __init__(self):
        self.pos = vec(resources.tile_to_pixel(13, 23))
        self.vel = vec(1, 0)
        self.turnTo = (1, 0)
        self.turn = False
        self.score = 0
        self.lives = 0
        self.gameOver = False
        self.blinky = Blinky.Blinky(self)
        self.inky = Inky.Inky(self)
        self.clyde = Clyde.Clyde(self)
        self.pinky = Pinky.Pinky(self)
        self.lifespan = 0
        self.ttl = 100  # time to live without eating another dot
        self.stopTimer = 0
        self.replay = False
        self.tiles = []
        for j in range(31):
            self.tiles.append([resources.originalTiles[j][i].clone() for i in range(28)])

    def set_ghosts(self, b, p, i, c):
        self.blinky = b
        self.pinky = p
        self.inky = i
        self.clyde = c

    def show(self):
        pac_img = resources.pac2
        if self.vel.x == -1:
            pac_img = pygame.transform.rotate(resources.pac2, 180)
        elif self.vel.y == -1:
            pac_img = pygame.transform.rotate(resources.pac2, 90)
        elif self.vel.y == 1:
            pac_img = pygame.transform.rotate(resources.pac2, 270)

        resources.SCREEN.blit(pac_img, (self.pos.x - 8, self.pos.y - 8))
        # pygame.display.update()

    def move(self):
        if not resources.clydeActive:
            self.ttl -= 1
            if self.ttl <= 0:
                self.kill()
        if self.check_position() and self.vel.magnitude_squared() != 0:
            self.stopTimer = 0
            self.pos.x += 2 * self.vel.x
            self.pos.y += 2 * self.vel.y
        else:
            self.stopTimer += 1
            if self.stopTimer > 100:
                self.kill()
        self.lifespan += 1

    def hit_pacman(self, ghost_pos):
        if self.pos.distance_to(ghost_pos) < 25:
            return True
        return False

    def kill(self):
        self.lives -= 1
        if self.lives < 0:
            self.gameOver = True
        else:
            self.pos = vec(resources.tile_to_pixel(13, 23))

        self.blinky = Blinky.Blinky(self)
        self.inky = Inky.Inky(self)
        self.clyde = Clyde.Clyde(self)
        self.pinky = Pinky.Pinky(self)
        self.vel = vec(-1, 0)
        self.turnTo = (-1, 0)

    def check_position(self):
        if resources.is_critical_position(self.pos):
            matrix_position = resources.pixel_to_tile(self.pos)
            if not self.tiles[int(matrix_position.y)][int(matrix_position.x)].eaten:
                self.tiles[int(matrix_position.y)][int(matrix_position.x)].eaten = True
                self.score += 1
                self.ttl = 600
            if self.tiles[int(matrix_position.y)][int(matrix_position.x)].bigDot and resources.bigDotsActive:
                if not self.blinky.return_home and not self.blinky.dead_for_a_bit:
                    self.blinky.frightened = True
                    self.blinky.flash_count = 0
                if not self.inky.return_home and not self.inky.dead_for_a_bit:
                    self.inky.frightened = True
                    self.inky.flash_count = 0
                if not self.pinky.return_home and not self.pinky.dead_for_a_bit:
                    self.pinky.frightened = True
                    self.pinky.flash_count = 0
                if not self.clyde.return_home and not self.clyde.dead_for_a_bit:
                    self.clyde.frightened = True
                    self.clyde.flash_count = 0

            position_to_check = (matrix_position.x + self.turnTo[0], matrix_position.y + self.turnTo[1])
            # if position_to_check[1] == 23 and position_to_check[0] == 22:
            #       print("found the fucker")
            if self.tiles[int(position_to_check[1])][int(position_to_check[0])].wall:
                if self.tiles[int(matrix_position.y + self.vel.y)][int(matrix_position.x + self.vel.x)].wall:
                    self.vel = vec(self.turnTo[0], self.turnTo[1])
                    return False
                else:
                    return True
            else:
                self.vel = vec(self.turnTo[0], self.turnTo[1])
                # vel.x *= 3 vel.y *= 3
                return True
        else:
            ahead = vec(self.pos.x + 10 * self.vel.x, self.pos.y + 10 * self.vel.y)
            if resources.is_critical_position(ahead):
                matrix_position = resources.pixel_to_tile(ahead)
                if not self.tiles[int(matrix_position.y)][int(matrix_position.x)].eaten:
                    self.tiles[int(matrix_position.y)][int(matrix_position.x)].eaten = True
                    self.score += 1
                    self.ttl = 600
                if self.tiles[int(matrix_position.y)][int(matrix_position.x)].bigDot and resources.bigDotsActive:
                    if not self.blinky.return_home and not self.blinky.dead_for_a_bit:
                        self.blinky.frightened = True
                        self.blinky.flash_count = 0
                    if not self.inky.return_home and not self.inky.dead_for_a_bit:
                        self.inky.frightened = True
                        self.inky.flash_count = 0
                    if not self.pinky.return_home and not self.pinky.dead_for_a_bit:
                        self.pinky.frightened = True
                        self.pinky.flash_count = 0
                    if not self.clyde.return_home and not self.clyde.dead_for_a_bit:
                        self.clyde.frightened = True
                        self.clyde.flash_count = 0

            if self.turnTo[0] + self.vel.x == 0 and self.turnTo[1] + self.vel.y == 0:
                self.vel = vec(self.turnTo[0], self.turnTo[1])
                return True
            return True
