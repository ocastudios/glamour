import globals
import obj_images
from pygame.locals import *

class MovingScenario():
    def __init__(self,index,level,dir):
        self.images = obj_images.OneSided(dir)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = 2000
        self.pos = (globals.universe.center_x+self.center_distance, globals.universe.floor - self.size[1])
        self.move = False
        self.dir = 'left'
        self.speed = 4
        self.count = 0
        self.rect = Rect(self.pos, self.size)

        level.moving_scenario.insert(index,self)
    def update_all(self,act,direction):
        self.set_pos(act,direction)
    def set_pos(self,act,direction):
        if globals.universe.speed != 0:
            self.center_distance -= globals.universe.speed/1.1
        self.pos = (globals.universe.center_x + self.center_distance,globals.universe.floor - (self.size[1]))
        self.rect = Rect(self.pos, self.size)
