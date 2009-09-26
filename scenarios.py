import os
import obj_images
import pygame
from pygame.locals import *
class Scenario():
    """It is necessary to extend this class in order to separete several classes of Scenario. Trees, Clouds, Posts and Buildings have different atributes and different functions."""
    def __init__(self,center_distance,dir,level,index = 1,invert = False, height = False):
        self.lights = None
        self.images         = obj_images.OneSided(dir)
        self.image          = self.images.list[0]
        if invert:
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size           = self.images.size
        self.center_distance= center_distance
        self.level          = level
        if not height:
            self.pos  = [(self.center_distance),level.floor-(self.size[1]-15)]
        else:
            self.pos = [(self.center_distance),height]

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
    def __init__(self,center_distance,dir,level,frames,index = 1):
        Scenario.__init__(self,center_distance,dir,level,index)
        self.images         = obj_images.GrowingUngrowing(dir,frames)

    def update_all(self):
        self.update_pos()

class FrontScenario(Scenario):
        pass

class Gate(Scenario):
    arrow_up = None
    def __init__(self,center_distance,dir,level,goal,goalpos=None,index = 1):
        Scenario.__init__(self,center_distance,dir,level,index)
        icon_directory = 'data/images/interface/icons/'
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

        if not self.arrow_up:
            self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = [center_distance,self.pos[1]-150]
        self.arrow_size = self.arrow_image.get_size()
        self.change_level = False
        self.goal = goal
        self.rect           = Rect(self.pos, self.size)
        self.image.blit(pygame.image.load(icon_directory).convert_alpha(),(91,59))

    def update_all(self):
        self.indicate_exit(self.level.princesses[0])
        self.set_level(self.level.princesses[0])
        self.update_pos()
        self.rect           = Rect(self.pos, self.size)

    def indicate_exit(self,princess):
        if self.rect.colliderect(princess.rect):
            self.arrow_image = self.arrow_up.list[self.arrow_up.itnumber.next()]
            self.arrow_pos[0] = self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2))

    def set_level(self,princess):
        if self.rect.colliderect(princess.rect):
            if princess.action[0] == 'open_door':
                self.goal(self.goalpos)


class BuildingDoor():
#TODO: use the save class to change the values of the princess attributes. Then create a new princess.
    def __init__(self,pos,directory,level,interior = None, bath = False):
        self.open = False
        self.level = level
        self.position = pos
        self.pos = [self.level.universe.center_x+self.position[0],self.position[1]]
        self.images = obj_images.OneSided(directory)
        self.images.number = 0
        self.image = self.images.list[self.images.number]
        self.size = self.images.size
        self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = (0,0)
        self.arrow_size = self.arrow_image.get_size()
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
                self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)
                self.arrow_image = self.arrow_up.list[self.arrow_up.itnumber.next()]
                if princess.action[0] == 'open_door':
                    self.level.inside = self.interior
                    self.open = True
            else:
                self.arrow_image = None
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
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','princesses','gates','enemies','menus')
        self.level.princesses[0].inside = True

    def outside(self):
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','gates','enemies','menus','princesses')


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
