import obj_images
import pygame

class MousePointer():
    def __init__(self,mouse_pos,level):        
        self.images         = obj_images.OneSided('data/images/interface/mouse-icon/pointer/')
        self.image          = self.images.list[self.images.number]
        self.size           = self.image.get_size()
        self.pos            = (mouse_pos[0]+(self.size[0]/2), mouse_pos[1]+(self.size[1]/2))
#TODO: substitute level.pointer.append by the direct instantiation of the instance into a list of the level
        level.pointer.append(self)

    def update(self):
        mouse_pos           = pygame.mouse.get_pos()
        self.pos            = (mouse_pos[0]-(self.size[0]/2),mouse_pos[1]-(self.size[1]/2))
        number_of_files     = len(self.images.list)-2
        self.image          = self.images.list[self.images.number]
        self.images.update_number()
    def update_all(self):
        pass
