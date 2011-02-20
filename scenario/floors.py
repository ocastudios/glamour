import utils
import pygame
import settings
import os
p = settings.p

class Floor():
    images = None

    def __init__(self,index,dir,level,height=0):
        height = {'all':p(186+height)}
        self.level = level
        self.images = self.images or utils.img.OneSided(dir)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = round((self.size[0])*index)
        self.set_pos()


    def set_pos(self):
        self.pos = [self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1]]


    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)


class Water(Floor):
    height = p(101)
    max    = p(125)
    min    = p(95)
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
    height = p(81)
    max =    p(90)
    min =    p(80)
    direction = 'up'
    speed = [6,1]

class Bridge():
    def __init__(self,dir,index,level,main=True):
        if main:            self.images = utils.img.OneSided(os.path.join(dir,'main'))
        else:               self.images = utils.img.OneSided(dir) 

        if main:
            self.left_bank = Bridge(os.path.join(str(dir),'left_bank'),index-1,level,main = False)
            self.right_bank= Bridge(os.path.join(str(dir),'right_bank'),index+1,level,main = False)

        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.level = level
        width = p(400)
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
        self.images = utils.img.OneSided(directory) 
        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.level = level
        self.center_distance = p(400)*index
        self.pos = [self.level.universe.center_x+(self.center_distance),int(p(900))-self.size[1]]
        level.floor_image[index]= self

    def update_all(self):
        self.pos[0] = self.level.universe.center_x+(self.center_distance)
