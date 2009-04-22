
import pygame

class GameClock():
    def __init__(self,level):
        self.level = level
        self.image = pygame.image.load('data/images/interface/clock/page_border.png').convert_alpha()
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
        self.clock_pointer_basic= pygame.image.load('data/images/interface/clock/clock_pointer.png').convert_alpha()
        self.clock_pointer      = []
        self.count              = 0
        self.tick               = 0
        self.time               = 'day' #morning,day,evening,night
        for degree in self.rotate_list:
            image = pygame.transform.rotate(self.clock_pointer_basic,degree)
            self.clock_pointer.append(image)
        
        level.clock.append(self)
            
        self.image  = self.clock_pointer[self.count]
        imagesize   = self.image.get_size()
        self.pos    = (self.level.universe.width-imagesize[0],0)
        

    def update_image(self):
        self.tick += 1
        number = 20
        if self.tick == number:
            if self.count>(len(self.rotate_list)-2):
                self.count  =0
            else:
                self.count  +=1
            self.image  = self.clock_pointer[self.count]
            imagesize   = self.image.get_size()
            self.pos    = (self.level.universe.width-imagesize[0],0)
        elif self.tick >number:
            self.tick = 0
    
        if self.count < 40:
            self.time = 'morning'
        elif self.count < 80:
            self.time = 'day'
        elif self.count < 120:
            self.time = 'evening'
        else:
            self.time = 'night'

