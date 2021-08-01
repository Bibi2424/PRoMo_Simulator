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

        self.og_pos = pos


    def update_button_right(self, pos):
        if pos[0] <= self.og_pos[0]:
            left = pos[0]
            right = self.og_pos[0]
        else:
            left = self.og_pos[0]
            right = pos[0]

        if pos[1] <= self.og_pos[1]:
            top = pos[1]
            bottom = self.og_pos[1]
        else:
            top = self.og_pos[1]
            bottom = pos[1]

        topleft = (left, top)
        size = (right-left, bottom-top)
        self.rect.update(topleft, size)
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.image.fill(self.color)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
