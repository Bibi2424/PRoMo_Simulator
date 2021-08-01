import json
import pygame
from pygame.locals import *

import robot
import obstacle
import environnement

FPS = 60

BACKGROUND_COLOR = (32, 32, 32)


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

    DISPLAYSURF = pygame.display.set_mode((800,600))
    DISPLAYSURF.fill(BACKGROUND_COLOR)
    pygame.display.set_caption(env_list['caption'])

    terrain = pygame.Surface((2000, 2000))

    FramePerSec = pygame.time.Clock()

    main_robot = robot.Robot((400, 300))

    env = environnement.Environnement()

    for obs in env_list['obstacles']:
        env.add(obstacle.Obstacle(tuple(obs['pos']), tuple(obs['size'])))

    running = True
    start_point = None
    new_obs = None

    while running:

        # Event
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            new_obs = env.process_event(event)
            main_robot.process_event(event)

            if event.type == KEYDOWN and event.key == K_s:
                save_environnement('environnement.json', env_list, env)

            if event.type == MOUSEBUTTONDOWN:
                print(event.button)

        # Update
        main_robot.update(env)
        if new_obs:
            new_obs.update_button_right(pygame.mouse.get_pos())

        # Display
        DISPLAYSURF.fill(BACKGROUND_COLOR)
        main_robot.draw(DISPLAYSURF)
        env.draw(DISPLAYSURF)
             
        pygame.display.update()
        FramePerSec.tick(FPS)

    pygame.quit()



if __name__ == "__main__" :
    main()
