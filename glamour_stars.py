import princess
import obj_images
from pygame.locals import *

class Glamour_Stars():
    rotating = None
    def __init__(self,level):
        self.level = level
        self.rotating = obj_images.OneSided('data/images/interface/star/star0/')
        self.image = self.rotating.list[0]
        self.size = self.image.get_size()
        self.pos = (200,60)

    def update_all(self):
        self.image = self.rotating.list[self.rotating.itnumber.next()]
