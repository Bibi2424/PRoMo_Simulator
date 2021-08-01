import math

import pygame
from pygame.locals import *

from utils import *


class Robot(pygame.sprite.Sprite):
    MAX_SPEED_X = 5
    MAX_SPEED_THETA = 5

    def __init__(self, init_pos, radius = 50):
        super().__init__() 

        self.radius = radius
        self.og_image = pygame.Surface((radius*2, radius*2), SRCALPHA)
        # self.og_image = pygame.Surface((radius*2, radius*2))

        pygame.draw.circle(self.og_image, (0, 128, 0), (radius, radius), radius, 0)
        pygame.draw.circle(self.og_image, (0, 0, 0), (radius, radius), radius, 3)
        pygame.draw.line(self.og_image, (128, 0, 0), (radius, radius), (radius, 0), 2)
        self.image = self.og_image

        self.rect = self.image.get_rect(center = init_pos)

        self.theta = 0

        self.speed_x = 0
        self.speed_theta = 0


    def process_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_w:
                self.speed_x = -1 * self.MAX_SPEED_X if event.type == KEYDOWN else 0
            if event.key == K_s:
                self.speed_x = 1 * self.MAX_SPEED_X if event.type == KEYDOWN else 0
            if event.key == K_a:
                self.speed_theta = 1 * self.MAX_SPEED_THETA if event.type == KEYDOWN else 0
            if event.key == K_d:
                self.speed_theta = -1 * self.MAX_SPEED_THETA if event.type == KEYDOWN else 0


    def update(self, env):
        # Transform based on speed
        self.theta = self.theta + self.speed_theta

        self.image = pygame.transform.rotate(self.og_image, self.theta)
        center = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center)  # Put the new rect's center at old center.

        # Compute next position
        old_rect = self.rect
        self.rect = self.rect.move(self.speed_x * math.sin(math.radians(self.theta)), self.speed_x * math.cos(math.radians(self.theta)))

        # Collision
        collision_list = pygame.sprite.spritecollide(self, env, False, collided = circle_square_collider)

        # inside = terrain.contains(self.rect)
        borders = pygame.sprite.Sprite()
        borders.rect = pygame.Rect((0, 0), (2000, 2000))
        inside = is_circle_inside_rect(self, borders)

        if collision_list or not inside:
            self.rect = old_rect


    def draw(self, surface):
        surface.blit(self.image, self.rect)
