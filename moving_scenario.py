import globals
import obj_images


class MovingScenario():
    def __init__(self,index,level,dir):
        self.pos = (0,200)
        self.images = obj_images.OneSided(dir)
        self.image_number = 0
        self.move = False
        self.dir = 'left'
        self.distance_from_center = 1500
        self.speed = 4
        self.count = 0
        self.image = self.images.list[self.image_number]
        self.size = self.image.get_size()
        self.pos = (globals.universe.center_x+self.distance_from_center, globals.universe.floor - self.size[1])
        for i in level:
            i.moving_scenario.insert(index,self)
    def update_all(self,act,direction):
        self.set_pos(act,direction)
    def set_pos(self,act,direction):
        if globals.universe.speed != 0:
            self.distance_from_center -= globals.universe.speed/1.1
        self.pos = (globals.universe.center_x + self.distance_from_center,globals.universe.floor - (self.size[1]))

