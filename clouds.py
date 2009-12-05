import random
import obj_images
from pygame.image import load

class Cloud():
    nimbus= None
    def __init__(self,level):
        dir = 'data/images/scenario/skies/nimbus/'
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
