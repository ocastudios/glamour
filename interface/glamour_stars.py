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
        self.rotating = obj_images.OneSided('data/images/interface/star/star0/')
        self.image = self.rotating.list[0]
        self.size = self.image.get_size()
        self.pos = p((195,45))

    def update_all(self):
        self.image = self.rotating.list[self.rotating.itnumber.next()]
