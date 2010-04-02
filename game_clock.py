import obj_images
import pygame

class GameClock():
    def __init__(self,level):
        self.level = level
        self.image = obj_images.scale_image(pygame.image.load('data/images/interface/clock/page_border.png').convert_alpha())
        self.pos   =((self.level.universe.width-self.image.get_width()),0)
        self.time  = 'day' 
        level.clock.append(self)


class ClockPointer():
    def __init__(self,level):
        self.level          = level
        self.rotate_list    = []
        x                   = -90
        while x != 0:
            self.rotate_list.append(x)
            x+= 0.5
        self.clock_pointer_basic= obj_images.scale_image(pygame.image.load('data/images/interface/clock/clock_pointer.png').convert_alpha())
        self.clock_pointer      = []
        self.count              = 0
        self.tick               = 0
        self.time               = 'day' #morning,day,evening,night
        self.clock_pointer = [pygame.transform.rotate(self.clock_pointer_basic,degree) for degree in self.rotate_list]
        if self not in level.clock:
            level.clock.append(self)
        self.image  = self.clock_pointer[self.count]
        imagesize   = self.image.get_size()
        self.pos    = (self.level.universe.width-imagesize[0],0)
        self.level.universe.frames_per_second
        self.pointerpos = 0

    def update_image(self):
        self.tick += 5
        if self.tick == self.level.universe.frames_per_second:
            if self.count < 180:
                if self.pointerpos > (len(self.rotate_list)-2):
                    self.pointerpos  =0
                else:
                    self.pointerpos  +=1
                self.image  = self.clock_pointer[self.count]
                imagesize   = self.image.get_size()
                self.pos    = (self.level.universe.width-imagesize[0],0)

            if self.count < 300:
                self.count += 1
            else:
                self.count = 0

        elif self.tick > self.level.universe.frames_per_second:
            self.tick = 0

        if self.count < 40:
            self.time = 'morning'
        elif self.count < 80:
            self.time = 'day'
        elif self.count < 120:
            self.time = 'evening'
        elif self.count < 179:
            self.time = 'night'
        else:
            self.time = 'ball'


