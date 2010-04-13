import obj_images
import pygame

class GameClock():
    def __init__(self,level):
        self.image = obj_images.image('data/images/interface/clock/page_border.png')
        self.pos   =((level.universe.width-self.image.get_width()),0)
    def update_all(self):
        pass


class ClockPointer():
    def __init__(self,level):
        self.level          = level
        self.rotate_list    = [float(i)/10 for i in range(-900,5,5)]
        self.clock_pointer_basic= obj_images.image('data/images/interface/clock/clock_pointer.png')
        self.clock_pointer      = []
        self.count              = 0
        self.tick               = 0
        self.time               = 'day' #morning,day,evening,night
        self.clock_pointer = [pygame.transform.rotate(self.clock_pointer_basic,degree) for degree in self.rotate_list]
        self.image  = self.clock_pointer[self.count]
        imagesize   = self.image.get_size()
        self.pos    = (self.level.universe.width-imagesize[0],0)
        self.level.universe.frames_per_second
        self.pointerpos = 0

    def update_all(self):
        self.tick += 1
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


