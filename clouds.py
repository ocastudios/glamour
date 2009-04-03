import obj_images
import random
from pygame.locals import *

class Cloud():
    nimbus= 0
    def __init__(self, p,level):
        self.pos = p
        nimbus = nimbus or [
                            obj_images.OneSided('data/images/scenario/skies/nimbus/1/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/2/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/3/')
                            ]
        self.images = nimbus[random.randint(0,2)]
        self.image = self.images.list[0]
        self.deep = random.random()/2
        self.image_number = 0
        self.rect = Rect(self.pos,self.image.get_size())
        for i in level:
            i.clouds.insert(self.deep,self)
    def update_all(self,dir,act):
        self.movement(dir,act)
        self.set_image()
    def movement(self,dir,act):
        self.pos = (self.pos[0]-10*self.deep,self.pos[1])
        self.rect = Rect(self.pos,self.image.get_size())
        self.set_image
    def set_image(self):
        #choose list
        number_of_files = len(self.images.list)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = self.images.list[self.image_number]

