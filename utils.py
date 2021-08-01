import math

import pygame
from pygame.locals import *


# Adapted from: http://www.jeffreythompson.org/collision-detection/circle-rect.php
def circle_square_collider(circle, square):

    # print(f'Check collision between {circle}, {square}')

    # temporary variables to set edges for testing
    testX, testY = cx, cy = circle.rect.center
    radius = circle.radius
    rx, ry = square.rect.topleft
    rw, rh = square.rect.size

    # which edge is closest?
    # test left edge
    if (cx < rx):
        testX = rx
    # right edge
    elif (cx > rx+rw): 
        testX = rx+rw
    # top edge
    if (cy < ry):
        testY = ry    
    # bottom edge
    elif (cy > ry+rh):
        testY = ry+rh

    # get distance from closest edges
    distX = cx-testX
    distY = cy-testY
    distance = math.sqrt( (distX*distX) + (distY*distY) )

    # if the distance is less than the radius, collision!
    if (distance <= radius):
        return True
    else:
        return False

def square_circle_collider(square, circle):
    return circle_square_collider(circle, square)


# Adapted from: https://stackoverflow.com/questions/59802794/how-to-make-ball-bounce-off-wall-with-pygame/59803018#59803018
def is_circle_inside_rect(circle, rect):

    if  circle.rect.center[0] - circle.radius < rect.rect.left or \
        circle.rect.center[0] + circle.radius > rect.rect.right or \
        circle.rect.center[1] - circle.radius < rect.rect.top or \
        circle.rect.center[1] + circle.radius > rect.rect.bottom:
        return False

    return True


# def screen_to_world_position(pos, )