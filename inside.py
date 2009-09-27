import pygame
import itertools
import obj_images
import save
import princess

class Inside():
    def __init__(self, level, item_type, item_list):
        self.status = 'outside'
        self.level  = level
        self.type_of_items = item_type
        self.items = []
        self.buttons = []
        if item_type != 'shower':
            counter = itertools.count()
            self.items = [Item(self, i,counter.next()) for i in item_list]
            self.buttons    = (
                                Button('data/images/interface/title_screen/button_ok/',
                                        (410,450),self.level,self.all_set),
                                Button('data/images/interface/title_screen/arrow_right/',
                                        (4*(self.level.universe.width/6),450),self.level,self.forward),
                                Button('data/images/interface/title_screen/arrow_right/',
                                        (2*(self.level.universe.width/6),450),self.level,self.rewind,invert=True)
                                )

    def forward(self,param):
        for i in self.items:
            i.queue_pos -= 1
        self.level.universe.click = False

    def rewind(self,param):
        for i in self.items:
            i.queue_pos += 1
        self.level.universe.click = False

    def all_set(self,param):
        self.status = 'done'

        for i in self.items:
            if i.queue_pos == 1:
                chosen_item = i.name
        exec('file = save.save_file(self.level.universe, self.level.princesses[0],'+
                     self.type_of_items+' = "'+self.type_of_items+"_"+chosen_item+'")')
        self.level.princesses[0] = princess.Princess(self.level,save=file, INSIDE = True)
        thumbnail = pygame.transform.scale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,'data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def NOTSETYET(self,param):
        pass


class Button():
    def __init__(self,directory,position, level,function,parameter = None,invert = False,):
        self.level = level
        self.images     = obj_images.Buttons(directory,5)
        if invert:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]

        self.size = self.image.get_size()
        self.position = position
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect = pygame.Rect(self.pos,self.size)
        self.function = function
        self.parameter = parameter

    def update_all(self):
        self.click_detection()

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        if self.rect.colliderect(self.level.game_mouse.rect):
            self.image = self.images.list[self.images.itnumber.next()]
            if self.level.universe.click:
                self.function(self.parameter)
        else:
            if self.image != self.images.list[0]:
                self.image = self.images.list[self.images.itnumber.next()]


class Item():
    def __init__(self, room, directory,queue_pos):
        self.name   = directory
        self.level  = room.level
        self.type   = room.type_of_items
        if self.type != 'shower':
            self.image  = pygame.image.load('data/images/princess/'+self.type+'_'+directory+'/stay/0.png').convert_alpha()
            self.size   = self.image.get_size()
            self.queue_pos = queue_pos-1
            self.available_pos = (self.level.universe.width/2-(self.size[0]),
                                  self.level.universe.width/2-(self.size[0]/2),
                                  self.level.universe.width/2)
            if queue_pos <= len(self.available_pos):
                self.pos    = [self.available_pos[self.queue_pos],(self.level.universe.height/2)-(self.size[1]/2)]
            else:
                self.pos = [0,0]
            self.speed  = 1
            self.positions= (
                            (self.level.universe.width/2-(self.size[0])),
                            (self.level.universe.width/2-(self.size[0]/2)),
                            (self.level.universe.width/2)
                            )
            self.choose_position = 0
            if 2 >= (self.queue_pos) >= 0:
                self.queue = True
            else:
                self.queue = False

    def update_all(self):
        if self.type != 'shower':
            if 0<= self.queue_pos <= 2:
                self.queue = True
                self.pos[0]= self.positions[self.queue_pos]
            else:
                self.queue = False
