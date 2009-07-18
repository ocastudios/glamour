
import obj_images
import pygame
from pygame.locals import *
class Scenario():
    """It is necessary to extend this class in order to separete several classes of Scenario. Trees, Clouds, Posts and Buildings have different atributes and different functions."""
    def __init__(self,center_distance,dir,level,index = 1,invert = False):
        self.images         = obj_images.OneSided(dir)
        self.images.number  = -1
        self.image          = self.images.list[self.images.number]
        if invert:
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size           = self.images.size
        self.center_distance= center_distance
        self.level          = level
        self.pos            = [(self.center_distance),level.floor-(self.size[1]-15)]
        if self.images.lenght > 1:
            self.update_pos = self.update_with_images
        else:
            self.update_pos = self.update_without_images

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
    def __init__(self,center_distance,dir,level,goal,index = 1):
        Scenario.__init__(self,center_distance,dir,level,index)
        try:
            if self.arrow_up:
                pass
        except:
            self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = (0,0)
        self.arrow_size = self.arrow_image.get_size()
        self.change_level = False
        self.goal = goal
        self.rect           = Rect(self.pos, self.size)

    def update_all(self):
        self.indicate_exit(self.level.princesses[0])
        self.set_level(self.level.princesses[0])
        self.update_pos()
        self.rect           = Rect(self.pos, self.size)

    def indicate_exit(self,princess):
        self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)
        if self.rect.colliderect(princess.rect):
            self.arrow_image = self.arrow_up.list[self.arrow_up.itnumber.next()]

    def set_level(self,princess):
        if self.rect.colliderect(princess.rect):
            if princess.action[0] == 'open_door':
                self.goal()


class BuildingDoor():
#TODO: use the save class to change the values of the princess attributes. Then create a new princess.
    def __init__(self,pos,directory,level,interior = None):
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

    def update_all(self):
        self.indicate_exit(self.level.princesses[0])
        self.update_pos()

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

    def update_pos(self):
        self.pos[0] = self.level.universe.center_x+self.position[0]
        self.rect = Rect(self.pos, self.size)

    def set_level(self,princess):
        pass

    def inside(self):
        self.level.inside.status = 'inside'
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','princesses','gates','enemies','menus')
        self.level.princesses[0].inside = True

    def outside(self):
        self.level.blitlist = ('sky','background','moving_scenario','scenarios','gates','enemies','menus','princesses')


class Background():
    def __init__(self,pos_x,level,dir):
        self.level = level
        self.images = obj_images.OneSided(dir)
        self.images.number = 0
        self.image = self.images.list[self.images.number]
        self.size = self.images.size
        self.pos = (pos_x,self.level.universe.floor-self.size[1])
    def update_image(self):
        pass
#        self.images.number += 1
#        if self.images.number > len(self.images.list)-1:
#            self.images.number = -1
#        self.image = self.images.list[self.images.number]

    def update_all(self):
        self.update_image()
