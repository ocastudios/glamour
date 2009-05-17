import obj_images
import random
from pygame.locals import *

class Cloud():
    nimbus= None
    def __init__(self,level):
        self.level = level
        self.pos = (random.randint(0,level.universe.width),random.randint(0,250))
        self.nimbus = self.nimbus or [
                            obj_images.OneSided('data/images/scenario/skies/nimbus/1/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/2/'),
                            obj_images.OneSided('data/images/scenario/skies/nimbus/3/')
                            ]
        self.images = self.nimbus[random.randint(0,2)]
        if self.images.lenght > 1:
            self.update_all = self.change_number
        else:
            self.update_all = self.dont_change
        self.image = self.images.list[0]
        self.deep = random.random()/2
        self.rect = Rect(self.pos,self.image.get_size())
        self.size = self.image.get_size()
        
    def change_number(self):
        self.image = self.images.list[self.images.itnumber.next()]
    def dont_change(self):
        pass
