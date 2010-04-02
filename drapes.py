import obj_images
import pygame
import os
import random
from settings import *


class Drape():
    images = None
    def __init__(self):
        size = (1440,900)
        directory = 'data/images/interface/omni/drapes/drapes/'
        frames = []
        drapes_size = [800,900]
        speed  = 0
        right_x     = 0
        left_x      = 710
        prep_images = []
        tiles = [pygame.image.load(directory+frame).convert_alpha() for frame in sorted(os.listdir(directory))]
        tile_index = 0
        while right_x > -1000:
            drape_image = pygame.Surface(size,pygame.SRCALPHA)
            if tile_index < len(tiles):
                tile=tiles[tile_index]
                tile_index += 1
            else:
                tile=tiles[-1]
            tile_size = tile.get_size()
            for x in range(left_x,1640,110):
                drape_image.blit(tile,(x,0))
            for x in range(right_x+710,-200,-110):
                drape_image.blit(pygame.transform.flip(tile,1,0),(x,0))
            right_x = right_x - speed
            left_x  = left_x  + speed
            if speed < 15:
                speed += 3
            prep_images.append(drape_image)

        self.images=[obj_images.scale_image(i) for i in prep_images]
        self.image = self.images[0]
        self.action = 'stay'
        self.speed = 0
        self.image_number = 0
        self.size = self.image.get_size()
        self.counter = 0

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
