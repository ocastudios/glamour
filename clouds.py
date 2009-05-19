import random
from pygame.image import load

class Cloud():
    nimbus= None
    def __init__(self,level):
        dir = 'data/images/scenario/skies/nimbus/'
        self.level = level
        self.pos = (random.randint(0,level.universe.width),random.randint(0,level.universe.height/4))
        self.nimbus = self.nimbus or [
                            load(dir+'/0/0.png').convert_alpha(),
                            load(dir+'/1/0.png').convert_alpha(),
                            load(dir+'/2/0.png').convert_alpha(),
                            load(dir+'/3/0.png').convert_alpha()
                            ]
        self.image = self.nimbus[random.randint(0,3)]
    def update_all(self):
        pass
