import math

import pygame
from pygame.locals import *


class Robot(pygame.sprite.Sprite):
    MAX_SPEED_X = 5
    MAX_SPEED_THETA = 5

    def __init__(self, init_pos, radius = 50):
        super().__init__() 

        self.og_image = pygame.Surface((radius, radius), SRCALPHA)

        pygame.draw.circle(self.og_image, (0, 128, 0), (radius/2, radius/2), radius/2, 0)
        pygame.draw.circle(self.og_image, (0, 0, 0), (radius/2, radius/2), radius/2, 3)
        pygame.draw.line(self.og_image, (128, 0, 0), (radius/2, radius/2), (radius/2, 0), 2)
        self.image = self.og_image

        self.rect = self.image.get_rect(center = init_pos)

        self.theta = 0

        self.speed_x = 0
        self.speed_theta = 0

    def process_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_UP:
                self.speed_x = -1 * self.MAX_SPEED_X if event.type == KEYDOWN else 0
            if event.key == K_DOWN:
                self.speed_x = 1 * self.MAX_SPEED_X if event.type == KEYDOWN else 0
            if event.key == K_LEFT:
                self.speed_theta = 1 * self.MAX_SPEED_THETA if event.type == KEYDOWN else 0
            if event.key == K_RIGHT:
                self.speed_theta = -1 * self.MAX_SPEED_THETA if event.type == KEYDOWN else 0


    def update(self, env):

        self.theta = self.theta + self.speed_theta

        self.image = pygame.transform.rotate(self.og_image, self.theta)
        center = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center)  # Put the new rect's center at old center.


        old_rect = self.rect
        self.rect = self.rect.move(self.speed_x * math.sin(math.radians(self.theta)), self.speed_x * math.cos(math.radians(self.theta)))

        collision_list = pygame.sprite.spritecollide(self, env, False)

        if collision_list:
            self.rect = old_rect


    def draw(self, surface):
        surface.blit(self.image, self.rect)
