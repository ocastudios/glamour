import globals
from pygame.locals import *

class GameCamera():
    def __init__(self,level):
        self.rect = Rect((0,0),(globals.os_screen.current_w,globals.os_screen.current_h))
        self.end_x = float(globals.os_screen.current_w)
        self.start_x = 0
        self.level = level
        self.limit = 0.4
        self.count = 0
        for i in self.level:
            i.cameras.append(self)

    def update_all(self,princess):
        self.update_pos(princess)

    def update_pos(self,princess):
        if princess.pos[0]+100 > (self.end_x - (self.end_x*self.limit)):
            globals.universe.speed -= self.count
            self.count += 1
        elif princess.pos[0]+100 < (self.start_x + (self.end_x*self.limit)):
            globals.universe.speed += self.count
            self.count += 1
        else:
            self.count = 0
            if globals.universe.speed != 0:
                if princess.pos[0]+100 > (self.end_x - (self.end_x*(self.limit+0.1))):
                    globals.universe.speed += 1
                if princess.pos[0]+100 < (self.start_x + (self.end_x*(self.limit +0.1))):
                    globals.universe.speed -= 1
            
