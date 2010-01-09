import obj_images
import pygame

class MousePointer():
    def __init__(self,mouse_pos,level, type = 1):
        if type == 2:
            self.images         = obj_images.OneSided('data/images/interface/mouse-icon/pointer/')
        else:
            self.images         = obj_images.OneSided('data/images/interface/mouse-icon/pointer/')
        self.image          = self.images.list[self.images.number]
        self.size           = self.image.get_size()

        self.pos            = (mouse_pos[0]+(self.size[0]/2), mouse_pos[1]+(self.size[1]/2))
#TODO: substitute level.pointer.append by the direct instantiation of the instance into a list of the level
        self.rect           = pygame.Rect(self.pos,self.size)
    def update(self):
        number_of_files     = len(self.images.list)-2
        self.image          = self.images.list[self.images.number]
        self.images.update_number()
        self.rect           = pygame.Rect(self.pos,self.size)
    def update_all(self):
        pass
