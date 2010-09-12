from pygame.locals import *
from settings import *


class GameCamera():
    def __init__(self,level, goalpos= None):
        self.level = level
        self.rect = Rect((0,0),(self.level.universe.width,self.level.universe.height))
        self.end_x = float(self.level.universe.width)
        self.start_x = 0
        self.limit = 0.38
        self.count = 0
        if goalpos:
            self.level.universe.center_x = goalpos

    def update_all(self):
        princess_pos = self.level.princesses[0].pos[0]
        if princess_pos+(100*scale) > (self.end_x - (self.end_x*self.limit)):
            self.level.universe.speed -= self.count*scale
            self.count += 5*scale
        elif princess_pos+(100*scale) < (self.start_x + (self.end_x*self.limit)):
            self.level.universe.speed += self.count*scale
            self.count += 5*scale
        else:
            self.count = 0
            if self.level.universe.speed != 0:
                if princess_pos+int((100*scale)) > (self.end_x - (self.end_x*(self.limit+0.1))):
                    self.level.universe.speed += 1
                if princess_pos+int((100*scale)) < (self.start_x + (self.end_x*(self.limit +0.1))):
                    self.level.universe.speed -= 1
