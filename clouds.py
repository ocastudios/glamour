import obj_images
import random
from pygame.locals import *

class Cloud():
    nimbus= None
    def __init__(self,x,y,level):
        self.level = level
        self.pos = [x,y]
        self.nimbus = self.nimbus or [
                            obj_images.OneSided('data/images/scenario/skies/nimbus/1/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/2/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/3/')
                            ]
        self.images = self.nimbus[random.randint(0,2)]
        self.image = self.images.list[0]
        self.deep = random.random()/2
        self.rect = Rect(self.pos,self.image.get_size())
        self.size = self.image.get_size()
    def update_all(self):
        self.pos[0] = self.pos[0]-10.*self.deep
        self.rect = Rect(self.pos,self.size)
        self.image = self.images.list[self.images.number]
        self.images.update_number()

