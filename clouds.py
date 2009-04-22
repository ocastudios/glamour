import obj_images
import random
from pygame.locals import *

class Cloud():
    nimbus= 0
    def __init__(self, p,level):
        self.pos = p
        self.nimbus = self.nimbus or [
                            obj_images.OneSided('data/images/scenario/skies/nimbus/1/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/2/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/3/')
                            ]
        self.images = self.nimbus[random.randint(0,2)]
        self.image = self.images.list[0]
        self.deep = random.random()/2
        self.rect = Rect(self.pos,self.image.get_size())


    def update_all(self,level):
        self.movement(level.act,level.dir)
        self.set_image()


    def movement(self,dir,act):
        self.pos = (self.pos[0]-10 * self.deep,self.pos[1])
        self.rect = Rect(self.pos,self.image.get_size())


    def set_image(self):
        self.image = self.images.list[self.images.number]
        self.images.update_number()

