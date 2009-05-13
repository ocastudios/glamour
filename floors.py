
import obj_images
from pygame.locals import *
class Floor():
    images = None

    def __init__(self,index,dir,level,height={'all':186}):
        self.level = level
        self.images = self.images or obj_images.OneSided(dir)

        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = (self.size[0]*(index))

        self.set_pos()
        self.rect = Rect(self.pos, self.size)

    def set_pos(self):
        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]


    def update_all(self):
        self.update_pos()

    def update_pos(self):
        self.images.update_number()
        self.image = self.images.list[self.images.number]
        self.pos[0] = self.level.universe.center_x+(self.center_distance)
        self.rect = Rect(self.pos, self.size)


class Water(Floor):
    height = 90
    max    = 100
    min    = 90
    speed = [2,1]
    direction = 'up'

    def set_pos(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)

    def update_pos(self):
        self.center_distance += self.speed[0]
        self.images.update_number()
        self.image = self.images.list[self.images.number]

        if self.direction == 'up':          self.height += self.speed[1]
        else:                               self.height -= self.speed[1]

        if self.height > self.max:          self.direction = 'down'
        if self.height < self.min:          self.direction = 'up'

        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.height)
        if self.pos[0] > self.level.universe.width:
            self.center_distance -= self.level.universe.width+(self.size[0]*2)
        if self.pos[0] < -self.size[0]:
            self.center_distance += self.level.universe.width+(self.size[0]*2)
        self.rect = Rect(self.pos, self.size)

class Water2(Water):
    height = 75
    max = 85
    min = 75
    direction = 'up'
    speed = [6,1]

class Bridge():
    def __init__(self,directory,index,level,main=True):
        if main:            self.images = obj_images.OneSided(directory+'bridge/')
        else:               self.images = obj_images.OneSided(directory) 

        if main:
            self.left_bank = Bridge(str(directory)+'left_bank/',index-1,level,main = False)
            self.right_bank= Bridge(str(directory)+'right_bank/',index+1,level,main = False)

        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.level = level

        if main:            self.center_distance = (400*(index))-400
        else:               self.center_distance = (400*(index))

        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]
        if main:
            del level.floor_image[index]
            level.floor_image.insert(0,self)
        else:
            level.floor_image[index]= self
        self.rect = Rect(self.pos, self.size)
    def update_all(self):
        self.update_pos()
    def update_pos(self):
        self.images.update_number()
        self.image = self.images.list[self.image_number]
        self.pos[0] = self.level.universe.center_x+self.center_distance
        self.rect = Rect(self.pos, self.size)
