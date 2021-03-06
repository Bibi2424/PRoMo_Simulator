import json
import pygame
from pygame.locals import *

import robot
import obstacle
import environnement

FPS = 60

BACKGROUND_COLOR = (32, 32, 32)
RESOLUTION = (1200, 800)


def save_environnement(file_name, env_list, env):
    obstacles = []
    for s in env:
        obstacles.append({'pos': s.rect.topleft, 'size': s.rect.size})
    env_list['obstacles'] = obstacles

    with open(file_name, 'w') as f:
        json.dump(env_list, f, indent = 4)


def main():

    with open('environnement.json', 'r') as f:
        env_list = json.load(f)

    pygame.init()

    game_display = pygame.display.set_mode(RESOLUTION)
    game_display.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(env_list['caption'])

    FramePerSec = pygame.time.Clock()

    terrain = pygame.Surface((2000, 2000))
    terrain.fill(BACKGROUND_COLOR)
    for i in range(0, 2000, 50):
        pygame.draw.line(terrain, (50, 50, 50), (0, i), (2000, i), 1)
        pygame.draw.line(terrain, (50, 50, 50), (i, 0), (i, 2000), 1)
    # terrain = environnement.Terrain((2000, 2000))

    borders = pygame.sprite.Sprite()
    borders.rect = terrain.get_rect()

    main_robot = robot.Robot((1000, 1000))
    main_group = pygame.sprite.GroupSingle(main_robot)

    env = environnement.Environnement()

    for obs in env_list['obstacles']:
        env.add(obstacle.Obstacle(tuple(obs['pos']), tuple(obs['size'])))

    scale = 1
    running = True
    screens_offset = (-(int(main_robot.rect.center[0] * scale) - game_display.get_size()[0]/2), -(int(main_robot.rect.center[1] * scale) - game_display.get_size()[1]/2))

    while running:

        # Event
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
                # NOTE: change mouse position to world coordinate
                event.pos = (int((event.pos[0] - screens_offset[0]) / scale), int((event.pos[1] - screens_offset[1]) / scale))

            env.process_event(event)
            main_robot.process_event(event)

            if event.type == KEYDOWN and event.key == K_m:
                save_environnement('environnement.json', env_list, env)

            if event.type == MOUSEMOTION:
                env.update_selection(event.pos, main_group)

            # if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            #     print(event.type, event.button)

            if event.type == MOUSEWHEEL:
                # print(f'mouse wheel: {event.which}, {event.flipped}, {event.x}, {event.y}')
                scale += event.y / 10
                if scale <= 0.1:
                    scale = 0.1

        # Update
        main_robot.update(env, borders)

        # Display
        game_display.fill((0, 0, 0))
        bkg = pygame.Surface(terrain.get_size())

        bkg.blit(terrain, (0, 0))

        main_robot.draw(bkg)
        env.draw(bkg)

        new_size = terrain.get_size()
        new_size = (int(new_size[0] * scale), int(new_size[1] * scale))
        temp = pygame.transform.scale(bkg, new_size)

        screens_offset = (-(int(main_robot.rect.center[0] * scale) - game_display.get_size()[0]/2), -(int(main_robot.rect.center[1] * scale) - game_display.get_size()[1]/2))
        game_display.blit(temp, screens_offset)
             
        pygame.display.update()
        FramePerSec.tick(FPS)

    pygame.quit()



if __name__ == "__main__" :
    main()
