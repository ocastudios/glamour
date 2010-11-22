import interactive.princess as princess
import utils.obj_images     as obj_images
from pygame.locals import *
from settings import *


def p(positions):
    return [int(i*scale) for i in positions ]
    
class Glamour_Stars():
    rotating = None
    def __init__(self,level):
        self.level = level
        self.rotating = obj_images.OneSided(main_dir+'/data/images/interface/star/star0/')
        self.image = self.rotating.list[0]
        self.size = self.image.get_size()
        self.pos = p((195,45))

    def update_all(self):
        self.image = self.rotating.list[self.rotating.itnumber.next()]
        
class Lil_Stars():
    def __init__(self,level, pos):
        self.level = level
        self.rotating = obj_images.There_and_back_again(main_dir+'/data/images/interface/lil_star/right/', second_dir = 'data/images/interface/lil_star/left/')
        self.image = self.rotating.list[0]
        self.size = self.image.get_size()
        self.pos = p(pos)

    def update_all(self):
        self.image = self.rotating.list[self.rotating.itnumber.next()]
        
class Lil_Star_Back():
    def __init__(self,level,pos):
        self.level=level
        self.image = obj_images.image(main_dir+'/data/images/interface/lil_star/back.png')
        self.pos = p(pos)
    def update_all(self):
        pass
