import utils.obj_images as obj_images
from pygame.locals import *
from settings import *

class Floor():
    images = None

    def __init__(self,index,dir,level,height=0):
        height = {'all':round((186+height)*scale)}
        self.level = level
        self.images = self.images or obj_images.OneSided(dir)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = round((self.size[0])*index)
        self.set_pos()


    def set_pos(self):
        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]


    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)


class Water(Floor):
    height = round(101*scale)
    max    = round(125*scale)
    min    = round(95*scale)
    speed = [2,1]
    direction = 'up'

    def set_pos(self):
        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]
    def update_all(self):
        self.center_distance += self.speed[0]
        if self.direction == 'up':
            self.height += self.speed[1]
        else:
            self.height -= self.speed[1]

        if self.height > self.max:          self.direction = 'down'
        if self.height < self.min:          self.direction = 'up'

        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.height)
        if self.pos[0] > self.level.universe.width:
            self.center_distance -= self.level.universe.width+(self.size[0]*2)
        if self.pos[0] < -self.size[0]:
            self.center_distance += self.level.universe.width+(self.size[0]*2)
        if self.__class__ != Water2:
            self.level.water_level = self.level.universe.floor-self.height


class Water2(Water):
    height = round(81*scale)
    max =    round(90*scale)
    min =    round(80*scale)
    direction = 'up'
    speed = [6,1]

class Bridge():
    def __init__(self,directory,index,level,main=True):
        if main:            self.images = obj_images.OneSided(directory+'main/')
        else:               self.images = obj_images.OneSided(directory) 

        if main:
            self.left_bank = Bridge(str(directory)+'left_bank/',index-1,level,main = False)
            self.right_bank= Bridge(str(directory)+'right_bank/',index+1,level,main = False)

        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.level = level
        width = round(400*scale)
        if main:            self.center_distance = round((width*index)-width)
        else:               self.center_distance = round(width*index)

        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]
        if main:
            del level.floor_image[index]
            level.floor_image.insert(0,self)
        else:
            level.floor_image[index]= self

    def update_all(self):
        self.update_pos()
    def update_pos(self):
        self.pos[0] = self.level.universe.center_x+self.center_distance


class Drain():
    def __init__(self,directory,index,level):
        self.images = obj_images.OneSided(directory) 
        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.level = level
        self.center_distance = round(scale*400)*index
        self.pos = [self.level.universe.center_x+(self.center_distance),int(round(scale*900))-self.size[1]]
        level.floor_image[index]= self

    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)
