from globals import *


class Scenario():
    """It is necessary to extend this class in order to separete several classes of Scenario. Trees, Clouds, Posts and Buildings have different atributes and different functions."""
    def __init__(self,pos,dir,level,index = 1):
        self.images = obj_images.OneSided(dir)
        self.image_number = -1
        self.speed = 1
        self.index = index
        self.image = self.images.list[self.image_number]
        self.size = self.image.get_size()
        self.distance_from_center = pos[0]
        self.level = level
        self.append_into_level_list()
        self.pos = (universe.center_x+(self.distance_from_center),Level_01.floor-(self.size[1]-15))
        self.rect = Rect(self.pos, self.size)
    def update_all(self):
        self.update_pos()
    def update_pos(self):
        self.image_number += 1
        if self.image_number > len(self.images.list)-1:
            self.image_number = 0
        self.image = self.images.list[self.image_number]
        self.pos = (universe.center_x+(self.distance_from_center),Level_01.floor-(self.size[1]-15))
        self.rect = Rect(self.pos, self.size)
    def append_into_level_list(self):
        self.level.scenarios.insert(self.index,self)
class FrontScenario(Scenario):
    def append_into_level_list(self):
        self.level.scenarios_front.insert(self.index,self)
class Gate(Scenario):
    def __init__(self,pos,dir,level,index = 1,type = None, parts=None):
        self.images = obj_images.OneSided(dir)
        self.image_number = -1
        self.speed = 1
        self.image = self.images.list[self.image_number]
        self.size = self.image.get_size()
        self.distance_from_center = pos[0]
        self.type = type
        self.parts = parts
        self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = (0,0)
        self.arrow_size = (0,0)
        level.gates.insert(index,self)
        self.pos = (universe.center_x+(self.distance_from_center),Level_01.floor-(self.size[1]-15))
        self.rect = Rect(self.pos, self.size)
    def update_all(self,princess):
        self.indicate_exit(princess)
        self.update_pos()
    def indicate_exit(self,princess):
        if self.rect.colliderect(princess.rect):
            self.arrow_image_number += 1
            if self.arrow_image_number > len(self.arrow_up.list)-1:
                self.arrow_image_number = 0
            self.arrow_image = self.arrow_up.list[self.arrow_image_number]
            self.arrow_size = self.arrow_image.get_size()
            self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)

class Building(Scenario):
    def __init__(self,pos,directory,level,door,index = 1):
        self.images = obj_images.OneSided(directory)
        self.image_number = -1
        self.index = index
        self.image_list = self.images.list
        self.image = self.image_list[self.image_number]
        self.size = self.image.get_size()
        self.distance_from_center = pos[0]
        self.level = level
        self.append_into_level_list()
        self.pos = (universe.center_x+(self.distance_from_center),Level_01.floor-(self.size[1]-15))
        self.rect = Rect(self.pos, self.size)

        self.door = BuildingDoor(self,door['pos'],door['directory'],level)



class BuildingDoor():
    def __init__(self,building,pos,directory,level):
        self.building = building
        self.position = pos
        self.pos = (building.pos[0]+self.position[0],building.pos[1]+self.position[1])
        self.images = obj_images.OneSided(directory)
        self.image_number = -1
        self.image = self.images.list[self.image_number]
        self.size = self.image.get_size()
        self.arrow_up = obj_images.OneSided('data/images/interface/up-arrow/')
        self.arrow_image_number = 0
        self.arrow_image = self.arrow_up.list[0]
        self.arrow_pos = (0,0)
        self.arrow_size = (0,0)
        self.rect = Rect(self.pos, self.size)
        level.gates.insert(building.index,self)
    def update_all(self,princess):
        self.indicate_exit(princess)
        self.update_pos()
    def indicate_exit(self,princess):
        if self.rect.colliderect(princess.rect):
            self.arrow_image_number += 1
            if self.arrow_image_number > len(self.arrow_up.list)-1:
                self.arrow_image_number = 0
            self.arrow_image = self.arrow_up.list[self.arrow_image_number]
            self.arrow_size = self.arrow_image.get_size()
            self.arrow_pos = (self.pos[0]+(self.size[0]/2-(self.arrow_size[0]/2)),self.pos[1]-150)
    def update_pos(self):
        self.pos = (self.building.pos[0]+self.position[0],self.building.pos[1]+self.position[1])
        self.rect = Rect(self.pos, self.size)
    def update_image(self):
        self.image_number += 1
        if self.image_number > len(self.images.list)-1:
            self.image_number = 0
        self.image = self.images.list[self.image_number]



class Background():
    def __init__(self,pos,level,index,dir):
        self.index = index
        self.images = obj_images.OneSided(dir)
        self.image_number = 0
        self.image = self.images.list[self.image_number]
        self.size = self.image.get_size()
        self.pos = (pos[0],universe.floor-self.size[1])
        level.background.insert(index,self)
    def update_image(self):
        self.image_number += 1
        if self.image_number > len(self.images.list)-1:
            self.image_number = -1
        self.image = self.images.list[self.image_number]
    def update_all(self):
        self.update_image()
