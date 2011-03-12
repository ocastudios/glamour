from pygame.locals import *
from settings import *


class GameCamera():
    def __init__(self,universe, goalpos= None):
        self.universe = universe
        self.rect = Rect((0,0),(self.universe.width,self.universe.height))
        self.end_x = float(self.universe.width)
        self.start_x = 0
        self.limit = 0.38
        self.count = 0
        if goalpos:
            self.universe.center_x = goalpos

    def update_all(self):
        princess_pos = self.universe.level.princesses[0].pos[0]
        if princess_pos+round(100*scale) > (self.end_x - round(self.end_x*self.limit)):
            self.universe.speed -= round(self.count*scale)
            self.count += round(5*scale)
        elif princess_pos+round(100*scale) < (self.start_x + round(self.end_x*self.limit)):
            self.universe.speed += round(self.count*scale)
            self.count += round(5*scale)
        else:
            self.count = 0
            if self.universe.speed != 0:
                if princess_pos+int(round(100*scale)) > (self.end_x - round(self.end_x*(self.limit+0.1))):
                    self.universe.speed += 1
                if princess_pos+int(round(100*scale)) < (self.start_x + round(self.end_x*(self.limit +0.1))):
                    self.universe.speed -= 1
