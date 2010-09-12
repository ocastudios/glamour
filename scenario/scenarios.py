import os
import utils.obj_images         as obj_images
import pygame
import random
from pygame.locals import *
from pygame.image import load
from settings import *


class Scenario():
    """It is necessary to extend this class in order to separete several classes of Scenario. Trees, Clouds, Posts and Buildings have different atributes and different functions."""
    def __init__(self,center_distance,dir,level,invert = False, height = False):
        self.lights = None
        self.images         = obj_images.OneSided(dir)
        self.image          = self.images.list[0]
        if invert:
            self.image      = pygame.transform.flip(self.image, 1,0)
        self.size           = self.images.size
        self.center_distance= center_distance
        self.level          = level
        if not height:
            self.pos  = [(self.center_distance),level.floor-(self.size[1]-(15*scale))]
        else:
            self.pos = [(self.center_distance), int(level.floor-self.size[1]-(height))]

        if self.images.lenght > 1:
            self.update_pos = self.update_with_images
        else:
            self.update_pos = self.update_without_images

        if dir[-5:] == 'base/':
            light_directory = dir[0:len(dir)-5]
        else:
            light_directory = dir
        files = os.listdir(light_directory)
#        print files
        if 'light' in files:
            light = 'light/'
        elif 'lights' in files:
            light = 'lights/'
        try:
            self.lights = {'images':obj_images.OneSided(light_directory+light),'status':'off','position':self}
        except:
            pass

    def update_all(self):
        self.update_pos()

    def update_with_images(self):
        self.image          = self.images.list[self.images.itnumber.next()]
        self.pos[0]         = self.level.universe.center_x+self.center_distance

    def update_without_images(self):
        self.pos[0]         = self.level.universe.center_x+self.center_distance


class Flower(Scenario):
    def __init__(self,center_distance,dir,level,frames,):
        Scenario.__init__(self,center_distance,dir,level)
        self.images         = obj_images.GrowingUngrowing(dir,frames)

    def update_all(self):
        self.update_pos()


class Gate(Scenario):
    arrow_up = None
    def __init__(self,center_distance,dir,level,goal,goalpos=None):
        Scenario.__init__(self,center_distance,dir,level)
        icon_directory = main_dir+'/data/images/interface/icons/'
        self.goalpos = goalpos
        if goal == level.BathhouseSt:
            icon_directory += 'bath/0.png'
        elif goal == level.DressSt:
            icon_directory += 'dress/0.png'
        elif goal == level.MakeupSt:
            icon_directory += 'make-up/0.png'
        elif goal == level.AccessorySt:
            icon_directory += 'ribbon/0.png'
        elif goal == level.ShoesSt:
            icon_directory += 'shoes/0.png'
        self.change_level = False
        self.goal = goal
        self.rect           = Rect(self.pos, self.size)
        self.image.blit(obj_images.scale_image(pygame.image.load(icon_directory).convert_alpha()),(91*scale,59*scale))

    def update_all(self):
        self.set_level(self.level.princesses[0])
        self.update_pos()
        self.rect           = Rect(self.pos, self.size)

    def set_level(self,princess):
        if self.rect.colliderect(princess.rect):
            if princess.action[0] == 'open_door':
                self.goal(self.goalpos)


class BuildingDoor():
    def __init__(self,pos,directory,level,interior = None, bath = False):
        self.open = False
        self.level = level
        self.position = pos
        self.pos = [self.level.universe.center_x+self.position[0],self.position[1]]
        self.images = obj_images.OneSided(directory)
        self.images.number = 0
        self.image = self.images.list[self.images.number]
        self.size = self.images.size
        self.rect = Rect(self.pos, self.size)
        self.once = True
        self.interior = interior
        self.bath = bath

    def update_all(self):
        self.indicate_exit(self.level.princesses[0])
        self.pos[0] = self.level.universe.center_x+self.position[0]
        self.rect = Rect(self.pos, self.size)

    def indicate_exit(self,princess):
        if self.rect.colliderect(princess.rect):
            if not princess.inside:
                if princess.action[0] == 'open_door':
                    self.level.inside = self.interior
                    self.open = True
        else:
            self.open = False
            self.once = True
        if self.open:
            if self.images.number < self.images.lenght -1:
                self.images.number += 1
                self.image = self.images.list[self.images.number]
            else:
                self.open = False
            if self.once:
                if self.images.number == self.images.lenght -1:
                    self.inside()
                    self.once = False
        else:
            if self.images.number > 0:
                self.images.number -= 1
                self.image = self.images.list[self.images.number]

    def inside(self):
        if self.bath:
            self.level.inside.status = 'bath'
        else:
            self.level.inside.status = 'inside'
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','animated_scenarios','princesses','gates','lights','enemies','menus')
        self.level.princesses[0].inside = True

    def outside(self):
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','gates','animated_scenarios','lights','princesses','enemies','menus')
        self.level.princesses[0].inside = False

class Background():
    def __init__(self,pos_x,level,dir):
        self.level = level
        self.images = obj_images.There_and_back_again(dir)
        self.images.number = 0
        self.image = self.images.list[self.images.number]
        self.size = self.images.size
        self.pos = (pos_x,self.level.universe.floor-self.size[1])
        if self.images.lenght > 3:
            self.update_images = self.update_with_images
        else:
            self.update_images = self.update_without_images
    def update_all(self):
        self.update_images()
    def update_without_images(self):
        pass
    def update_with_images(self):
        self.image          = self.images.list[self.images.itnumber.next()]


class ExitSign():
    def __init__(self,level):
        self.level = level
        self.pos = [-1000,-1000]
        self.images = obj_images.OneSided(main_dir+'/data/images/interface/up-arrow/')
        self.image = self.images.list[0]
        self.size = self.image.get_size()
        self.rect = Rect(self.pos, self.size)

    def update_all(self):
        princess = self.level.princesses[0]
        control = 0
        if not princess.inside:
            for i in self.level.gates:
                if (i.__class__ == Gate or i.__class__ == BuildingDoor):
                    if i.rect.colliderect(princess.rect):
                        control += 1
                        self.pos = (i.pos[0]+(i.size[0]/2-(self.size[0]/2)),i.pos[1]-(150*scale))
                        self.image = self.images.list[self.images.number]
                        self.images.update_number()
        if control ==0:
            self.images.number =0
            self.image = None
        else:
            control = 0


class Cloud():
    nimbus= None
    def __init__(self,level):
        dir = main_dir+'/data/images/scenario/skies/nimbus/'
        self.level = level
        self.pos = (random.randint(0,int(level.universe.width)),random.randint(0,int(level.universe.height/4)))
        self.nimbus = self.nimbus or [
                            obj_images.scale_image(load(dir+'/0/0.png').convert_alpha()),
                            obj_images.scale_image(load(dir+'/1/0.png').convert_alpha()),
                            obj_images.scale_image(load(dir+'/2/0.png').convert_alpha()),
                            obj_images.scale_image(load(dir+'/3/0.png').convert_alpha())
                            ]
        self.image = self.nimbus[random.randint(0,3)]
    def update_all(self):
        pass
