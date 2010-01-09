import obj_images
from pygame.locals import *
from settings import *

class Floor():
    images = None

    def __init__(self,index,dir,level,height=0):
        height = {'all':(186+height)*scale}
        self.level = level
        self.images = self.images or obj_images.OneSided(dir)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = (self.size[0])*index
        self.set_pos()


    def set_pos(self):
        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]


    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)



class Water(Floor):
    height = 101*scale
    max    = 125*scale
    min    = 95*scale
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


class Water2(Water):
    height = 81*scale
    max = 90*scale
    min = 80*scale
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

        if main:            self.center_distance = scale*((int(400)*(index))-int(400))
        else:               self.center_distance = scale*(int(400)*(index))

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
        self.center_distance = scale*(400*index)
        self.pos = [self.level.universe.center_x+(self.center_distance),int(scale*900)-self.size[1]]
        level.floor_image[index]= self

    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)
