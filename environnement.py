import pygame
from pygame.locals import *

import obstacle

class Environnement(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.new_obs = None

    def process_event(self, event):

        if event.type == MOUSEBUTTONDOWN:
            print(f'Mouse down {event.pos} at {event.button}')

            # Check for collision
            clicked_sprites = [s for s in self if s.rect.collidepoint(event.pos)]

            if event.button == 1 and self.new_obs == None:
                if not clicked_sprites:
                    # Create new obstacle
                    self.new_obs = obstacle.Obstacle(event.pos, (0, 0))
                    self.add(self.new_obs)

            if event.button == 3:
                for s in clicked_sprites:
                    self.remove(s)

        if event.type == MOUSEBUTTONUP:
            print(f'Mouse up {event.pos} at {event.button}')
            if event.button == 1 and self.new_obs != None:

                size = self.new_obs.rect.size
                if size[0] < 1 or size[1] < 1:
                    print('Remove sprite, too small')
                    self.remove(self.new_obs)
                self.new_obs = None

        return self.new_obs