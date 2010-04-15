import pygame
import itertools
import obj_images
import save
import princess
import os
from settings import *


def p(positions):
    return [int(i*scale) for i in positions ]

class Inside():
    def __init__(self, level, item_type, item_list):
        self.status = 'outside'
        self.level  = level
        self.type_of_items = item_type
        self.items = []
        self.buttons = []
        dir = 'data/images/interface/title_screen/'
        if item_type != 'shower':
            counter = itertools.count()
            self.items = [Item(self, i,counter.next()) for i in item_list]
            self.buttons    = (
                 Button(dir+'button_ok/',(410,450),self.level,self.all_set),
                 Button(dir+'arrow_right/',(4*(self.level.universe.width/6),450),self.level,self.forward),
                 Button(dir+'arrow_right/',(2*(self.level.universe.width/6),450),self.level,self.rewind,invert=True)
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
        exec('save.save_file(self.level,'+self.type_of_items+' = "'+self.type_of_items+"_"+chosen_item+'")')
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,'data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def NOTSETYET(self,param):
        pass


class Button():
    def __init__(self,directory,position, level,function,parameter = None,invert = False,fonte='Domestic_Manners.ttf', font_size=40, color=(0,0,0)):
        self.level = level
        try:
            os.listdir(directory)
            type_of_button = 'image'
        except:
            type_of_button = 'text'
        if type_of_button == 'image':
            self.images     = obj_images.Buttons(directory,5)
            if invert:
                self.images.list = self.invert_images(self.images.list)
            self.image = self.images.list[self.images.number]
            self.size = self.image.get_size()
            self.position = p(position)
            self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                               (self.position[1]-(self.image.get_size()[1])/2)]
            self.rect = pygame.Rect(self.pos,self.size)
            self.function = function
            self.parameter = parameter
            self.list_of_images = self.images.list
        if type_of_button == 'text':
            font_size  = int(font_size*scale)
            font       = fonte
            self.text       = directory
            self.color      = color
            self.fontA      = pygame.font.Font('data/fonts/'+fonte,font_size)
            self.list_of_images= [self.fontA.render(self.text,1,self.color)]
            self.image      = self.list_of_images[0]
            self.size       = self.image.get_size()
            self.position   = p(position)
            self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                               (self.position[1]-(self.image.get_size()[1])/2)]
            self.rect       = pygame.Rect(self.pos,self.size)
            self.function   = function            
            self.parameter  = parameter

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
            try:
                self.image = self.list_of_images[self.images.itnumber.next()]
            except:
                pass
            if self.level.universe.click:
                self.function(self.parameter)
        else:
            if self.image != self.list_of_images[0]:
                try:
                    self.image = self.images.list[self.images.itnumber.next()]
                except: pass

class Item():
    def __init__(self, room, directory,queue_pos):
        self.name   = directory
        self.level  = room.level
        self.type   = room.type_of_items
        if self.type != 'shower':
            self.image  = obj_images.scale_image(pygame.image.load('data/images/princess/'+self.type+'_'+directory+'/stay/0.png').convert_alpha())
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
            if 0 <= self.queue_pos <= 2:
                self.queue = True
                self.pos[0]= self.positions[self.queue_pos]
            else:
                self.queue = False


class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button('data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
                           Button('To the Ball',(500,100),self.level, self.all_set, font_size=80)
                            )

    def all_set(self,param):
        self.status = 'done'
        for i in self.items:
            if i.queue_pos == 1:
                chosen_item = i.name
        exec('file = save.save_file(self.level,'+self.type_of_items+' = "'+self.type_of_items+"_"+chosen_item+'")')
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,'data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

class Princess_Home():
    def __init__(self, level, princess=None):
        print "Creating Princess Home: "+ princess['name'] 
        princess_directory  = 'data/images/princess/'
        ball_directory      = 'data/images/interface/ball/'
        painting_screen = pygame.Surface((200,200), pygame.SRCALPHA).convert_alpha()
        if princess == Rapunzel:
            painting_screen.blit(pygame.image.load(princess_directory+'hair_rapunzel_back'+'/stay/0.png').convert_alpha(),(0,0))
        images  = [pygame.image.load(princess_directory+item+'/stay/0.png').convert_alpha() for item in ('skin_'+princess['skin'],princess['hair'])]
        for img in images:
            painting_screen.blit(img, (0,0))
        self.princess_image = obj_images.scale_image(painting_screen)


        self.princess_icon  =  obj_images.scale_image( pygame.image.load(ball_directory+princess['icon']).convert_alpha())
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button('data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),)

        princess_name = princess["name"].lower()
        cursor = self.level.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+princess_name+" WHERE id = (SELECT MAX(id) FROM "+princess_name+")").fetchone()
        self.princess_image.blit(obj_images.image(princess_directory+row['face']+'/stay/0.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['dress']+'/stay/0.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['arm']+'/stay/0.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['accessory']+'/stay/0.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['shoes']+'/stay/0.png'),(0,0))
        self.princess_image = pygame.transform.flip(self.princess_image,1,0)

    def all_set(self,param):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,'data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]

class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button('data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
                           Button('To the Ball',(500,100),self.level, self.all_set, font_size=80)
                            )

    def all_set(self,param):
        self.status = 'done'
        for i in self.items:
            if i.queue_pos == 1:
                chosen_item = i.name
        exec('file = save.save_file(self.level,'+self.type_of_items+' = "'+self.type_of_items+"_"+chosen_item+'")')
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,'data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')
