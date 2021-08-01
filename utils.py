import math

import pygame
from pygame.locals import *


# Adapted from: http://www.jeffreythompson.org/collision-detection/circle-rect.php
def circle_square_collider(circle, square):

    # temporary variables to set edges for testing
    testX, testY = cx, cy = circle.rect.center
    radius = circle.radius
    rx, ry = square.rect.topleft
    rw, rh = square.rect.size
    # testY = cy;

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