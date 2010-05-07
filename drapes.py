import obj_images
import pygame
import os
import random
from settings import *
import getscreen

def p(positions):
    return [int(i*scale) for i in positions ]
class Drape():
    images = None
    def __init__(self):
        size = p((1440,900))
        directory = 'data/images/interface/omni/drapes/drapes/'
        frames = []
        drapes_size = p([720,900])
        speed  = 0
        right_x     = 0
        left_x      = 645*scale
#        prep_images = []
#        tiles = getscreen.drapes_tiles#[obj_images.image(directory+frame) for frame in sorted(os.listdir(directory))]
#        tile_index = 0
#        while right_x > -1000*scale:
#            drape_image = pygame.Surface(size,pygame.SRCALPHA)
#            if tile_index < len(tiles):
#                tile=tiles[tile_index]
#                tile_index += 1
#            else:
#                tile=tiles[-1]
#            tile_size = tile.get_size()
#            for x in range(left_x,int(1440*scale),int(110*scale)):
#                drape_image.blit(tile,(x,0))
#            for x in range(int(right_x+(610*scale)),int(-200*scale),int(-110*scale)):
#                drape_image.blit(pygame.transform.flip(tile,1,0),(x,0))
#            right_x = right_x - speed
#            left_x  = left_x  + speed
#            if speed < 15*scale:
#                speed += 3*scale
#            prep_images.append(drape_image)

        self.images= getscreen.prep_images
        self.image = self.images[0]
        self.action = 'stay'
        self.speed = 0
        self.image_number = 0
        self.size = self.image.get_size()
        self.counter = 0
        del getscreen.prep_images

    def update_all(self):
        self.counter += 1
        if self.counter >5:
            if self.action == "open" and self.image_number < len(self.images)-1:
                self.image_number +=1
            elif self.action =="close" and self.image_number > -len(self.images):
                self.image_number -=1
            self.image = self.images[self.image_number]


class UperDrape():
    def __init__(self):
        size = (1540,356)
        prep = pygame.Surface(size, pygame.SRCALPHA)
        tile = pygame.image.load('data/images/interface/omni/drapes/upper_drapes/0.png').convert_alpha()
        x = 0
        for i in range(14):
            prep.blit(tile,(x,0))
            x += 110
        self.image = obj_images.scale_image(prep)
        self.action = 'stay'
        self.y = 0
        self.size_y = 356*scale

    def update_all(self):
        if self.action == 'open':
            self.y -= (3*scale)
        if self.y < -self.size_y:
            self.y = -self.size_y
