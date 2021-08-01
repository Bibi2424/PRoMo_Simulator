import pygame
from pygame.locals import *

import obstacle
from utils import *



class Environnement(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.new_obs = None

    def process_event(self, event):

        if event.type == MOUSEBUTTONDOWN:
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
                    s.kill()

        if event.type == MOUSEBUTTONUP:
            if event.button == 1 and self.new_obs != None:

                size = self.new_obs.rect.size
                if size[0] < 1 or size[1] < 1:
                    print('Remove sprite, too small')
                    self.remove(self.new_obs)
                self.new_obs = None

        return self.new_obs


    def update_selection(self, new_pos, collision_group):
        if self.new_obs == None:
            return
        
        # NOTE: Really ugly but I haven't found a better solution yet
        next_obs = obstacle.Obstacle(self.new_obs.rect.topleft, self.new_obs.rect.size)
        next_obs.update_button_right(new_pos)

        print(next_obs.rect, self.new_obs.rect)

        collision_list = pygame.sprite.spritecollide(next_obs, collision_group, False, collided = square_circle_collider)
        if collision_list:
            return

        self.new_obs.update_button_right(new_pos)
