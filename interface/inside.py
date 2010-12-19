import pygame
import itertools
import utils.obj_images as obj_images
import utils.save as save
import interactive.princess as princess
import os
import random
import interface.widget as widget
import interactive.messages as messages
from settings import *

import gettext
t = gettext.translation('glamour', 'locale')
_ = t.ugettext

def p(positions):
    return [int(i*scale) for i in positions ]

class Inside():
    def __init__(self, level, item_type, item_list):
        self.status = 'outside'
        self.level  = level
        self.type_of_items = item_type
        self.items = []
        self.buttons = []
        dir = data_dir+'/images/interface/title_screen/'
        if item_type != 'shower':
            counter = itertools.count()
            self.items = [Item(self, i,counter.next()) for i in item_list]
            self.chosen_glow = Chosen_Glow(self, pos = [-200,500], degree = 90)
            self.buttons    = (
                 widget.Button(dir+'button_ok/',(410,530),self.level,self.all_set),
                 self.chosen_glow
                                )
        self.chosen_item = None
        self.big_princess = BigPrincess(self)
        self.music = data_dir+"/sounds/music/menu.ogg"

#    def forward(self):
##        for i in self.items:
##            i.queue_pos -= 1
#        self.level.universe.click = False

#    def rewind(self):
#        for i in self.items:
#            i.queue_pos += 1
#        self.level.universe.click = False

    def all_set(self):
        self.status = 'done'
        if self.chosen_item:
            exec('save.save_file(self.level,'+self.type_of_items+' = "'+self.type_of_items+"_"+self.chosen_item.name+'")')
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.flip(pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100)),1,0)
        pygame.image.save(thumbnail,data_dir+'/saves/'+self.level.princesses[0].name.encode('utf-8')+'/thumbnail.PNG')

    def NOTSETYET(self):
        pass


class Item():
    def __init__(self, room, directory,index):
        self.name   = directory
        self.level  = room.level
        self.room   = room
        self.type   = room.type_of_items
        if self.type != 'shower':
            self.image  = obj_images.scale_image(pygame.image.load(data_dir+'/images/princess/'+self.type+'_'+directory+'/big_icons/0.png').convert_alpha())
            self.size   = self.image.get_size()
            self.pos    = [450*scale+(index*(self.size[0])),(self.level.universe.height/2)-(self.size[1]/2)]
            self.speed  = 1
        self.rect       = pygame.Rect((self.pos),(self.size))
        self.active     = False

    def update_all(self):
        self.click_detection()

    def click_detection(self):
        if self.rect.colliderect(self.level.game_mouse.rect):
            self.active = True
            if self.level.universe.click:
                self.room.chosen_item = self
                self.room.big_princess.images[self.room.big_princess.image_dict[self.type]] = obj_images.image(data_dir+'/images/princess/'+self.type+'_'+self.name+"/big.png", invert = True)
                self.room.chosen_glow.pos = self.pos[0]-(40*scale),self.pos[1]-(40*scale)
                if self.type == "hair":
                    if self.name in ("black","brown","rapunzel", "rastafari","red"):
                        self.room.big_princess.images[self.room.big_princess.image_dict["hair_back"]] = obj_images.image(data_dir+'/images/princess/'+self.type+'_'+self.name+"_back/big.png", invert = True)
                    else:
                        self.room.big_princess.images[self.room.big_princess.image_dict["hair_back"]] = None
                elif self.type == "dress":
                    if self.name in ("yellow","red"):
                        self.room.big_princess.images[self.room.big_princess.image_dict["armdress"]] = obj_images.image(data_dir+'/images/princess/sleeve_'+self.name+'/big.png',invert = True)
                    else:
                        self.room.big_princess.images[self.room.big_princess.image_dict["armdress"]] = None

class BigPrincess():
    def __init__(self, room):
        self.room           = room
        princess_directory  = data_dir+'/images/princess/'
        ball_directory      = data_dir+'/images/interface/ball/'
        self.pos        = p([ 20,270])
        cursor = room.level.universe.db_cursor
        sql = "SELECT * FROM princess_garment WHERE id=(SELECT MAX(id) FROM princess_garment)"
        row = cursor.execute(sql).fetchone()
        self.image_dict = {
                        "hair_back" :0,
                        "skin"      :1,
                        "face"      :2,
                        "hair"      :3,
                        "shoes"     :4,
                        "dress"     :5,
                        "arm"       :6,
                        "armdress"  :7,
                        "accessory" :8
                            } 
        garments = ["hair_back", "skin" ,"face", "hair" , "shoes", "dress", "arm", "armdress", "accessory"]
        self.images = []
        for i in garments:
            if row[i] and row[i]!= "None":
                img = obj_images.image(princess_directory+row[i]+"/big.png", invert = True)
            else:
                img = None
            self.images += [img]


    def update_all(self):
        pass

    def all_set(self):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,data_dir+'/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class Princess_Home():
    def __init__(self, level, princess=None):
        print "Creating Princess Home: "+ princess['name'] 
        princess_directory  = data_dir+'/images/princess/'
        ball_directory      = data_dir+'/images/interface/ball/'
        painting_screen = pygame.Surface((400,400), pygame.SRCALPHA).convert_alpha()
        if princess == Rapunzel:
            painting_screen.blit(pygame.image.load(princess_directory+'hair_rapunzel_back'+'/big.png').convert_alpha(),(0,0))
        images  = [pygame.image.load(princess_directory+item+'/big.png').convert_alpha() for item in ('skin_'+princess['skin'],princess['hair'])]
        for img in images:
            painting_screen.blit(img, (0,0))
        self.princess_image = obj_images.scale_image(painting_screen)
        self.princess_icon  = obj_images.scale_image( pygame.image.load(ball_directory+princess['icon']).convert_alpha())
        self.status = 'outside'
        self.level  = level
        mymessage = messages.princesses_phrases[random.randint(0,(len(messages.princesses_phrases)-1))]
        if '%s' in mymessage:
            self.message = mymessage %self.level.princesses[0].name
        else:
            self.message = mymessage
        self.items = []
        self.buttons = []
        self.buttons    = (
                    widget.Button(data_dir+'/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
                    widget.GameText(self.message, (850,820), self.level, font_size = 40, box = (1100,400))
        )
        princess_name = princess["name"].lower()
        cursor = self.level.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+princess_name+" WHERE id = (SELECT MAX(id) FROM "+princess_name+")").fetchone()
        [self.princess_image.blit(obj_images.image(princess_directory+row[i]+ '/big.png'),(0,0)) for i in (
                    'face', 'dress', 'arm', 'accessory', 'shoes')]
        self.big_princess = BigPrincess(self)

        self.music = data_dir+"/sounds/music/menu.ogg"

    def all_set(self):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,data_dir+'/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]

class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.music = data_dir+"/sounds/music/menu.ogg"
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (widget.Button(data_dir+'/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
                           widget.Button(_('Go to the Ball'),(1240,550),self.level, self.to_the_ball),
                           widget.GameText(_("It is not very cute to repeat your outfits. Check out what you wore at past Balls and try to find something different."), (720,750), level, box=(600,300)),
                           widget.GameText(_("Last Ball"),         (600,350), level, font_size = 25),
                           widget.GameText(_("Great Past Ball"),   (800,350), level, font_size = 25),
                           widget.GameText(_("3 Balls Ago"),       (1000,350),level, font_size = 25)
                            )
        self.big_princess = BigPrincess(self)
        self.past_balls = []
        cursor = level.universe.db_cursor
        for i in (1,2,3):
            try:
                sql             = "SELECT * FROM princess_garment WHERE id = (SELECT MAX(id)-"+str(i)+" FROM princess_garment)"
                row = cursor.execute(sql).fetchone()
                image_dict = {  "hair_back" :0,
                                "skin"      :1,
                                "face"      :2,
                                "hair"      :3,
                                "shoes"     :4,
                                "dress"     :5,
                                "arm"       :6,
                                "armdress"  :7,
                                "accessory" :8
                                    } 
                garments = ["hair_back", "skin" ,"face", "hair" , "shoes", "dress", "arm", "armdress", "accessory"]
                image = pygame.Surface(p((200,200)), pygame.SRCALPHA).convert_alpha()
                for i in garments:
                    if row[i] and row[i]!= "None":
                        image.blit(obj_images.image(data_dir+'/images/princess/'+row[i]+"/stay/0.png"),(0,0))
#                image = pygame.transform.flip(self.image,1,0)
                self.past_balls += [image]
            except (TypeError,):
                print "You haven't attended "+str(i)+" Balls yet"
        cursor.close()

    def all_set(self):
        self.status = 'done'

    def to_the_ball(self):
        self.level.clock[1].count = 175
        self.level.clock[1].time = 'night'
        self.status = 'done'


class Chosen_Glow():
    def __init__(self,room, pos = [0,0], degree = 0):
        self.room = room
        self.images =  obj_images.OneSided(data_dir+'/images/interface/select/')
        self.image = self.images.list[0]
        self.pos   = p(pos)

    def update_all(self):
        self.image = self.images.list[self.images.itnumber.next()]
        pass
