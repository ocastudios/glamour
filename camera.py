import pygame
from princess import *
from globals import *

class GameCamera():
    def __init__(self,level):
        self.end_x = float(os_screen.current_w)
        self.start_x = 0
        self.level = level
        self.limit = 0.4
        self.count = 0
        for i in self.level:
            i.cameras.append(self)
    def update_pos(self,universe):
        if princess.pos[0]+100 > (self.end_x - (self.end_x*self.limit)):
            universe.speed -= self.count
            self.count += 2
        elif princess.pos[0]+100 < (self.start_x + (self.end_x*self.limit)):
            universe.speed += self.count
            self.count += 2 
        else:
            self.count = 0            
#            universe.speed = 0
            if universe.speed != 0:            
                if princess.pos[0]+100 > (self.end_x - (self.end_x*(self.limit+0.1))):
                    universe.speed += 1
                if princess.pos[0]+100 < (self.start_x + (self.end_x*(self.limit +0.1))):
                    universe.speed -= 1
            
