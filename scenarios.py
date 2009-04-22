
import obj_images

from pygame.locals import *
class Scenario():
    """It is necessary to extend this class in order to separete several classes of Scenario. Trees, Clouds, Posts and Buildings have different atributes and different functions."""
    def __init__(self,pos,dir,level,index = 1):
        self.images         = obj_images.OneSided(dir)
        self.images.number  = -1
        self.speed          = 1
        self.index          = index
        self.image          = self.images.list[self.images.number]
        self.size           = self.image.get_size()
        self.center_distance= pos[0]
        self.level          = level
        self.pos            = (self.level.universe.center_x+(self.center_distance),level.floor-(self.size[1]-15))
        self.rect           = Rect(self.pos, self.size)

    def update_all(self,level):
        self.update_pos()
    def update_pos(self):
        self.images.number += 1
        if self.images.number > len(self.images.list)-1:
            self.images.number = 0
        self.image          = self.images.list[self.images.number]
        self.pos            = (self.level.universe.center_x+(self.center_distance),self.level.floor-(self.size[1]-10))
        self.rect           = Rect(self.pos, self.size)


class FrontScenario(Scenario):
        nonevar = None

class Gate(Scenario):
    try:
        if arrow_up:
            pass
    except:
        arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
    arrow_image_number = 0
    arrow_image = arrow_up.list[0]
    arrow_pos = (0,0)
    arrow_size = (0,0)
    change_level = False
    level = 'bathhouse_st'

    def update_all(self,level):
        self.indicate_exit(level.princess)
        self.set_level(level.princess)
        self.update_pos()
        

    def indicate_exit(self,princess):
        self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)
        if self.rect.colliderect(princess.rect):
            self.arrow_image_number += 1
            if self.arrow_image_number > len(self.arrow_up.list)-1:
                self.arrow_image_number = 0
            self.arrow_image = self.arrow_up.list[self.arrow_image_number]
            self.arrow_size = self.arrow_image.get_size()

    def set_level(self,princess):
        if self.rect.colliderect(princess.rect):
            if princess.action[0] == 'open_door':
                self.change_level = True

class Building(Scenario):
    def __init__(self,pos,directory,level,door,index = 1):
        self.images = obj_images.OneSided(directory)
        self.images.number = -1
        self.index = index
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = pos[0]
        self.level = level
        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.floor-(self.size[1]-15))
        self.rect = Rect(self.pos, self.size)
        self.door = BuildingDoor(self,door['pos'],door['directory'],level)

class BuildingDoor():
    def __init__(self,building,pos,directory,level):
        self.building = building
        self.position = pos
        self.pos = (building.pos[0]+self.position[0],building.pos[1]+self.position[1])
        self.images = obj_images.OneSided(directory)
        self.images.number = -1
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = (0,0)
        self.arrow_size = (0,0)
        self.rect = Rect(self.pos, self.size)
        self.level = 'bathhouse_st'
        self.change_level = False
        level.gates.insert(building.index,self)
    def update_all(self,level):
        self.indicate_exit(level.princess)
        self.update_pos()
    def indicate_exit(self,princess):
        self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)
        if self.rect.colliderect(princess.rect):
            self.arrow_image_number += 1
            if self.arrow_image_number > len(self.arrow_up.list)-1:
                self.arrow_image_number = 0
            self.arrow_image = self.arrow_up.list[self.arrow_image_number]
            self.arrow_size = self.arrow_image.get_size()
            if princess.action[0] == 'open_door':
                self.update_image()
            
    def update_pos(self):
        self.pos = (self.building.pos[0]+self.position[0],self.building.pos[1]+self.position[1])
        self.rect = Rect(self.pos, self.size)
    def update_image(self):
        self.images.number += 1
        if self.images.number > len(self.images.list)-1:
            self.images.number = 0
        self.image = self.images.list[self.images.number]

    def set_level(self,princess):
        pass



class Background():
    def __init__(self,pos,level,index,dir):
        self.level = level
        self.index = index
        self.images = obj_images.OneSided(dir)
        self.images.number = 0
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.pos = (pos[0],self.level.universe.floor-self.size[1])
        self.rect = Rect(self.pos, self.size)
    def update_image(self):
        self.images.number += 1
        if self.images.number > len(self.images.list)-1:
            self.images.number = -1
        self.image = self.images.list[self.images.number]
        self.rect = Rect(self.pos, self.size)
    def update_all(self,level):
        self.update_image()
