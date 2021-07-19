import pygame
import math

vec = pygame.math.Vector2

# flags = pygame.RESIZABLE
# SCREEN = pygame.display.set_mode((1600, 900), flags)

pad_x, pad_y = 350, 150
width, height = 448 + 2 * pad_x, 496 + 2 * pad_y
SCREEN = pygame.display.set_mode((width, height))

img = pygame.image.load('data/map.jpg').convert()
# img = pygame.transform.scale2x(img)

blinkySprite = pygame.image.load('data/blinky20000.png')
blinkySprite2 = pygame.transform.smoothscale(blinkySprite, (15, 15)).convert()

pinkySprite = pygame.image.load('data/pinky20000.png')
pinkySprite2 = pygame.transform.smoothscale(pinkySprite, (15, 15)).convert()

inkySprite = pygame.image.load('data/inky20000.png')
inkySprite2 = pygame.transform.smoothscale(inkySprite, (15, 15)).convert()

clydeSprite = pygame.image.load('data/clyde20000.png')
clydeSprite2 = pygame.transform.smoothscale(clydeSprite, (15, 15)).convert()

frightenedSprite = pygame.image.load('data/frightenedGhost0000.png')
frightenedSprite_ = pygame.transform.smoothscale(frightenedSprite, (15, 15)).convert()

frightenedSprite2 = pygame.image.load('data/frightenedGhost20000.png')
frightenedSprite_2 = pygame.transform.smoothscale(frightenedSprite2, (15, 15)).convert()

deadSprite = pygame.image.load('data/deadGhost0000.png')
deadSprite2 = pygame.transform.smoothscale(deadSprite, (15, 15)).convert()

pac = pygame.image.load('data/pac.png')
pac2 = pygame.transform.smoothscale(pac, (15, 15)).convert()

blinkyActive = True
pinkyActive = True
inkyActive = True
clydeActive = True

bigDotsActive = True

nextConnectionNo = 1000

speed = 60

pop = None
# Population.Population(500, SCREEN, resources.originalTiles)

humanPlayer = None
# Player.Player(SCREEN, resources.originalTiles)

speciesChamp = None
# Player.Player(SCREEN, resources.originalTiles)

genPlayerTemp = None
# Player.Player(SCREEN, resources.originalTiles)


showBest = True
runBest = False
humanPlaying = False

runThroughSpecies = False
upToSpecies = 0

showBestEachGen = False
upToGen = 0
showBrain = False

usingInputsStart = 4
usingInputsEnd = 11

upToStage = 1

showNothing = False

previousBest = 0

originalTiles = []
tilesRepresentation = (
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 8, 1),
    (1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 6, 1, 1, 6, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1),
    (1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 8, 1),
    (1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1),
    (1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1),
    (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))


def tile_to_pixel(x, y):
    pix = (x * 16 + 8 + pad_x, y * 16 + 8 + pad_y)
    return pix


def pixel_to_tile(pix):
    # tile_coord = vec(pix.x - pad_x, pix.y - pad_y)
    # final_tile_coord = vec((tile_coord.x - 8) / 16, (tile_coord.y - 8) / 16)
    final_tile_coord = vec((pix.x - pad_x - 8) / 16, (pix.y - pad_y - 8) / 16)
    return final_tile_coord


def is_critical_position(pos):
    tile_coord = [pos.x - pad_x, pos.y - pad_y]
    return (tile_coord[0] - 8) % 16 == 0 and (tile_coord[1] - 8) % 16 == 0


def get_nearest_non_wall_tile(target):
    min_val = 100
    min_index_j = 0
    min_index_i = 0
    for i in range(0, 28):
        for j in range(0, 31):
            if not originalTiles[j][i].wall:
                dist = math.sqrt(((target.x - i) ** 2 + (target.y - j) ** 2))
                if dist < min_val:
                    min_val = dist
                    min_index_j = j
                    min_index_i = i
    return vec(min_index_i, min_index_j)


def enter_stage(stage_num):
    global usingInputsStart, usingInputsEnd, blinkyActive, inkyActive, pinkyActive, clydeActive, bigDotsActive
    if stage_num == 1:
        usingInputsStart = 4
        usingInputsEnd = 11
        blinkyActive = False
        inkyActive = False
        pinkyActive = False
        clydeActive = False
        bigDotsActive = False
    elif stage_num == 2:
        usingInputsStart = 0
        usingInputsEnd = 11
        blinkyActive = True
        inkyActive = False
        pinkyActive = True
        clydeActive = False
        bigDotsActive = False
    elif stage_num == 3:
        usingInputsStart = 0
        usingInputsEnd = 11
        blinkyActive = True
        inkyActive = True
        pinkyActive = True
        clydeActive = True
        bigDotsActive = False
    elif stage_num == 4:
        usingInputsStart = 0
        usingInputsEnd = 12
        blinkyActive = True
        inkyActive = True
        pinkyActive = True
        clydeActive = True
        bigDotsActive = True


def enter_new_stage():
    global pop
    pop.best_score = 0
    for p in pop.species:
        p.best_fitness = 0
    for pp in pop.pop:
        pp.best_score = 0
        pp.fitness = 0
        pp.score = 0
