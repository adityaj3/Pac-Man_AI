import pygame
import resources
import Player
import Population
import Tile

pygame.init()
vec = pygame.math.Vector2

pad_x, pad_y = resources.pad_x, resources.pad_y
width, height = resources.width, resources.height
SCREEN = resources.SCREEN
FPS = 100
clock = pygame.time.Clock()


def setup():
    # clock.tick(FPS)
    for j in range(31):
        tile_row = []
        for i in range(28):
            tile_coords = resources.tile_to_pixel(i, j)
            tile_element = Tile.Tile(tile_coords[0], tile_coords[1])
            if resources.tilesRepresentation[j][i] == 1:
                tile_element.wall = True
            elif resources.tilesRepresentation[j][i] == 0:
                tile_element.dot = True
            elif resources.tilesRepresentation[j][i] == 8:
                tile_element.bigDot = True
            elif resources.tilesRepresentation[j][i] == 6:
                tile_element.eaten = True
            tile_row.append(tile_element)
        resources.originalTiles.append(tile_row)

    resources.pop = Population.Population(500)
    resources.humanPlayer = Player.Player()
    # resources.speciesChamp = Player.Player()
    # resources.genPlayerTemp = Player.Player()


def draw():
    # global genPlayerTemp, speciesChamp, pop
    draw_to_screen()
    if resources.showBestEachGen:
        if not resources.genPlayerTemp.dead:
            resources.genPlayerTemp.look()
            resources.genPlayerTemp.think()
            resources.genPlayerTemp.update()
            resources.genPlayerTemp.show()
        else:
            resources.upToGen += 1
            if resources.upToGen >= len(resources.pop.gen_players):
                resources.upToGen = 0
                resources.showBestEachGen = False
                resources.enter_stage(resources.upToStage)
            else:
                print(f"STAGE: {resources.pop.gen_players[resources.upToGen].stage}")
                resources.enter_stage(resources.pop.gen_players[resources.upToGen].stage)
                resources.genPlayerTemp = resources.pop.gen_players[resources.upToGen].clone_for_replay()
    elif resources.runThroughSpecies:
        if not resources.speciesChamp.dead:
            resources.speciesChamp.look()
            resources.speciesChamp.think()
            resources.speciesChamp.update()
            resources.speciesChamp.show()
        else:
            resources.upToSpecies += 1
            if resources.upToSpecies >= len(resources.pop.species):
                resources.runThroughSpecies = False
            else:
                resources.speciesChamp = resources.pop.species[resources.upToSpecies].champ.clone_for_replay()
    else:
        if resources.humanPlaying:
            if not resources.humanPlayer.dead:
                resources.humanPlayer.look()
                resources.humanPlayer.update()
                resources.humanPlayer.show()
            else:
                resources.humanPlaying = False
        elif resources.runBest:
            if not resources.pop.best_player.dead:
                resources.pop.best_player.look()
                resources.pop.best_player.think()
                resources.pop.best_player.update()
                resources.pop.best_player.show()
            else:
                resources.runBest = False
                resources.pop.gen_players = resources.pop.best_player.clone_for_replay()
        else:
            if not resources.pop.done():
                resources.pop.update_alive()
            else:
                if resources.pop.gen == 20:
                    if resources.pop.best_score < 200:
                        resources.pop = Population.Population(500)
                        return
                    resources.upToStage = 3
                    resources.enter_stage(3)
                    resources.pop.new_stage = True
                elif resources.pop.gen == 60:
                    resources.upToStage = 4
                    resources.enter_stage(4)
                    resources.pop.new_stage = True
                elif resources.pop.gen == 120:
                    if resources.pop.best_score < 220:
                        resources.pop = Population.Population(500)
                        return

                resources.pop.natural_selection()


def draw_to_screen():
    if not resources.showNothing:
        SCREEN.fill((10, 10, 10))
        pygame.draw.rect(SCREEN, (0, 0, 0), (0, height - pad_y - pad_x, width, pad_x))  # brain
        pygame.draw.rect(SCREEN, (0, 0, 0), (pad_x, 0, 448, height - 496 - pad_y))  # score

        pygame.draw.line(SCREEN, (29, 48, 137), (0, height - pad_x - pad_y - 4), (width, height - pad_x - pad_y - 4), 6)
        pygame.draw.line(SCREEN, (32, 56, 178), (0, height - pad_x - pad_y - 4), (width, height - pad_x - pad_y - 4), 4)

        pygame.draw.line(SCREEN, (29, 48, 137), (0, height - pad_y + 2), (width, height - pad_y + 2), 6)
        pygame.draw.line(SCREEN, (32, 56, 178), (0, height - pad_y + 2), (width, height - pad_y + 2), 4)

        pygame.draw.line(SCREEN, (29, 48, 137), (350, 150 - 4), (350 + 448, 150 - 4), 6)
        pygame.draw.line(SCREEN, (32, 56, 178), (350, 150 - 4), (350 + 448, 150 - 4), 4)

        pygame.draw.line(SCREEN, (29, 48, 137), (pad_x - 4, 0), (pad_x - 4, height - pad_y + 2), 6)
        pygame.draw.line(SCREEN, (32, 56, 178), (pad_x - 4, 0), (pad_x - 4, height - pad_y + 2), 4)

        pygame.draw.line(SCREEN, (29, 48, 137), (pad_x + 448 + 2, 0), (pad_x + 448 + 2, height - pad_y + 2), 6)
        pygame.draw.line(SCREEN, (32, 56, 178), (pad_x + 448 + 2, 0), (pad_x + 448 + 2, height - pad_y + 2), 4)

        SCREEN.blit(resources.img, (pad_x, pad_y))
        draw_brain()
        write_info()
        # pygame.display.update()


def draw_brain():
    if resources.runThroughSpecies:
        resources.speciesChamp.brain.draw_genome(width - pad_x, height - pad_y - pad_x, 350, 350)
    elif resources.runBest:
        resources.pop.best_player.brain.draw_genome(width - pad_x, height - pad_y - pad_x, 350, 350)
    elif resources.humanPlaying:
        resources.showBrain = False
    elif resources.showBestEachGen:
        resources.genPlayerTemp.brain.draw_genome(width - pad_x, height - pad_y - pad_x, 350, 350)
    else:
        resources.pop.pop[0].brain.draw_genome(width - pad_x, height - pad_y - pad_x, 350, 350)
    # pygame.display.update()


def write_info():
    font = pygame.font.SysFont("monaco", 25)
    if resources.showBestEachGen:
        txt = font.render(f"Score: {resources.genPlayerTemp.score}", True, (255, 255, 255))
        SCREEN.blit(txt, (pad_x + 50, (height - 496 - pad_y) // 2))
        txt = font.render(f"Gen: {resources.genPlayerTemp.gen + 1}", True, (255, 255, 255))
        SCREEN.blit(txt, (pad_x + 448 - 120, (height - 496 - pad_y) // 2))
        txt = font.render(f"Stage: {resources.genPlayerTemp.stage}", True, (255, 255, 255))
        SCREEN.blit(txt, (20, height - pad_x - pad_y + 50))
    elif resources.runThroughSpecies:
        txt = font.render(f"Score: {resources.speciesChamp.score}", True, (255, 255, 255))
        SCREEN.blit(txt, (pad_x + 50, (height - 496 - pad_y) // 2))
        txt = font.render(f"Species: {resources.upToSpecies + 1}", True, (255, 255, 255))
        SCREEN.blit(txt, (pad_x + 448 - 150, (height - 496 - pad_y) // 2))
        txt = font.render(f"Players in this Species: {len(resources.pop.species[resources.upToSpecies].players)}", True,
                          (255, 255, 255))
        SCREEN.blit(txt, (10, height - pad_x - pad_y + 50))
    else:
        if resources.humanPlaying:
            txt = font.render(f"Score: {resources.humanPlayer.score}", True, (255, 255, 255))
            SCREEN.blit(txt, (pad_x + 50, (height - 496 - pad_y) // 2))
        elif resources.runBest:
            txt = font.render(f"Score: {resources.pop.best_player.score}", True, (255, 255, 255))
            SCREEN.blit(txt, (pad_x + 50, (height - 496 - pad_y) // 2))
            txt = font.render(f"Gen: {resources.pop.gen}", True, (255, 255, 255))
            SCREEN.blit(txt, (pad_x + 448 - 120, (height - 496 - pad_y) // 2))
        else:
            if resources.showBest:
                txt = font.render(f"Score: {resources.pop.pop[0].score}", True, (255, 255, 255))
                SCREEN.blit(txt, (pad_x + 50, (height - 496 - pad_y) // 2))
                txt = font.render(f"Gen: {resources.pop.gen}", True, (255, 255, 255))
                SCREEN.blit(txt, (pad_x + 448 - 120, (height - 496 - pad_y) // 2))
                txt = font.render(f"Species: {len(resources.pop.species)}", True, (255, 255, 255))
                SCREEN.blit(txt, (20, height - pad_x - pad_y + 50))
                txt = font.render(f"Global Best Score: {resources.pop.best_score}", True, (255, 255, 255))
                SCREEN.blit(txt, (20, height - pad_x - pad_y + 150))


def key_pressed():
    # global speciesChamp, genPlayerTemp, humanPlayer
    global run
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                resources.showBest = not resources.showBest
            elif event.key == pygame.K_PLUS:
                resources.speed += 10
                clock.tick(resources.speed)
                print(resources.speed)
            elif event.key == pygame.K_MINUS:
                if resources.speed > 10:
                    resources.speed -= 10
                    clock.tick(resources.speed)
                    print(resources.speed)
            elif event.key == pygame.K_b:
                resources.runBest = not resources.runBest
            elif event.key == pygame.K_s:
                resources.runThroughSpecies = not resources.runThroughSpecies
                resources.upToSpecies = 0
                resources.speciesChamp = resources.pop.species[resources.upToSpecies].champ.clone_for_replay()
            elif event.key == pygame.K_g:
                resources.showBestEachGen = not resources.showBestEachGen
                resources.upToGen = 0
                resources.enter_stage(resources.pop.gen_players[resources.upToGen].stage)
                resources.genPlayerTemp = resources.pop.gen_players[resources.upToGen].clone()
            elif event.key == pygame.K_n:
                resources.showNothing = not resources.showNothing
            elif event.key == pygame.K_p:
                resources.humanPlaying = not resources.humanPlaying
                resources.humanPlayer = Player.Player()
            elif event.key == pygame.K_UP:
                resources.humanPlayer.pacman.turnTo = (0, -1)
                resources.humanPlayer.pacman.turn = True
            elif event.key == pygame.K_DOWN:
                resources.humanPlayer.pacman.turnTo = (0, 1)
                resources.humanPlayer.pacman.turn = True
            elif event.key == pygame.K_LEFT:
                resources.humanPlayer.pacman.turnTo = (-1, 0)
                resources.humanPlayer.pacman.turn = True
            elif event.key == pygame.K_RIGHT:
                if resources.runThroughSpecies:
                    resources.upToSpecies += 1
                    if resources.upToSpecies >= len(resources.pop.species):
                        resources.runThroughSpecies = False
                    else:
                        resources.speciesChamp = resources.pop.species[resources.upToSpecies].champ.clone_for_replay()
                elif resources.showBestEachGen:
                    resources.upToGen += 1
                    if resources.upToGen >= len(resources.pop.gen_players):
                        resources.showBestEachGen = False
                        resources.enter_stage(resources.upToStage)
                    else:
                        resources.enter_stage(resources.pop.gen_players[resources.upToStage].stage)
                        resources.genPlayerTemp = resources.pop.gen_players[resources.upToGen].clone_for_replay()
                elif resources.humanPlaying:
                    resources.humanPlayer.pacman.turnTo = (1, 0)
                    resources.humanPlayer.pacman.turn = True


run = True
setup()
while run:
    draw()
    key_pressed()
    pygame.display.update()
pygame.quit()
