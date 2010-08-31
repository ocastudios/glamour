import obj_images


class Button():
    def __init__(self,image_dir,position,level):
        self.level      = level
        self.images     = obj_images.Buttons(image_dir,5)
        self.image      = self.images.list[self.images.number]
        self.size       = self.image.get_size()
        self.position   = position
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect       = pygame.Rect(self.pos,self.size)

    def update_all(self):Button
        self.update_pos()
        self.click_detection()

    def update_pos(self):
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        self.rect = pygame.Rect(self.pos,self.size)
        if self.rect.collidepoint(self.level.mouse_pos):
            self.image = self.images.list[self.images.itnumber.next()]
            if self.level.universe.click:
                exec("self.function("+str(self.parameters)+")")
        else:
            if self.image != self.images.list[0]:
                self.image = self.images.list[self.images.itnumber.next()]
