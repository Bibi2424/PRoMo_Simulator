import pygame
from pygame.locals import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, color = (128, 0, 0)):
        super().__init__() 

        print(f'Creating obstacle size:{size} at {pos}')
        self.color = color
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = pos)

    # def update(self, new_pos):
    #   self.rect.center = new_pos

    def update_button_right(self, pos):
        topleft = self.rect.topleft
        bottomright = pos
        size = (abs(bottomright[0] - topleft[0]), abs(bottomright[1] - topleft[1]))
        self.rect.update(topleft, size)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.color)
        # self.image = pygame.Surface(size)
        # self.image.fill(color)
        # self.rect = self.image.get_rect(bottomleft = pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
