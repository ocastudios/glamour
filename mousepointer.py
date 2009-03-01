from globals import *


class MousePointer():
    def __init__(self,mouse_pos,level):        
        self.images = ObjectImages('data/images/interface/mouse-icon/pointer/')
        self.image_number = 0
        self.image_list = self.images.left
        self.image = self.images.left[self.image_number]
        self.size = self.image.get_size()
        self.pos = (mouse_pos[0]+(self.size[0]/2),mouse_pos[1]+(self.size[1]/2))
        self.count = 0
        for i in level:
            i.pointer.append(self)

    def update(self,mouse_pos):
        self.pos = (mouse_pos[0]-(self.size[0]/2),mouse_pos[1]-(self.size[1]/2))
        number_of_files = len(self.image_list)-2
        self.image = self.image_list[self.image_number]

        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.count+=1
