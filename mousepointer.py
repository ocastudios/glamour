import obj_images
import pygame

class MousePointer():
    def __init__(self,level, type = 1):
        self.mouse_pos =  pygame.mouse.get_pos()
        if type == 2:
            self.type = 2
            self.images         = obj_images.OneSided('data/images/interface/mouse-icon/pointer2/')
        else:
            self.type = 1
            self.images         = obj_images.OneSided('data/images/interface/mouse-icon/pointer/')
        self.image          = self.images.list[self.images.number]
        self.size           = self.image.get_size()
        self.pos            = (self.mouse_pos[0]+(self.size[0]/2), self.mouse_pos[1]+(self.size[1]/2))
        self.rect           = pygame.Rect(self.pos,self.size)

    def update(self):
        self.mouse_pos =  pygame.mouse.get_pos()
        number_of_files     = len(self.images.list)-2
        self.image          = self.images.list[self.images.number]
        self.images.update_number()
        self.pos            = (self.mouse_pos[0]+(self.size[0]/2), self.mouse_pos[1]+(self.size[1]/2))
        self.rect           = pygame.Rect(self.pos,self.size)

    def update_all(self):
        pass
