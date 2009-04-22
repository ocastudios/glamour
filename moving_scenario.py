import obj_images
from pygame.locals import *

class MovingScenario():
    def __init__(self,index,level,dir):
        self.level = level
        self.images = obj_images.OneSided(dir)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()

        self.center_distance = ((self.level.size-self.level.universe.width) - self.size[0])*self.level.universe.center_x/self.level.size

        self.pos = (self.center_distance, self.level.universe.floor - self.size[1])
        self.move = False
        self.dir = 'left'
        self.speed = 4
        self.count = 0
        self.rect = Rect(self.pos, self.size)


    def update_all(self,level):
        self.set_pos(level.act,level.direction)
    def set_pos(self,act,direction):
        self.center_distance = ((self.level.size-self.level.universe.width) - self.size[0])*self.level.universe.center_x/self.level.size
        self.pos = (self.center_distance,self.level.universe.floor - (self.size[1]))
        self.rect = Rect(self.pos, self.size)
