import pygame
import itertools
import utils
import utils.save as save
import interactive.princess as princess
import os
import random


import interface.widget as widget
import interactive.messages as messages
import database
import settings
from settings import directory
p = settings.p
d = settings.d
t = settings.t

class Inside():
    def __init__(self, level, item_type, item_list):
        self.status = 'outside'
        self.level  = level
        self.type_of_items = item_type
        self.items = []
        self.buttons = []
        self.menu = []
        counter = itertools.count()
        if item_type != 'shower':
            self.items = [Item(self, i,counter.next()) for i in item_list]
            self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.items])
            self.chosen_glow = Chosen_Glow(self, pos = [-200,500], degree = 90)
            self.buttons    = (
                 widget.Button(directory.button_ok,(410,530),self.level,self.all_set),
                 self.chosen_glow
                                )
            self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__==widget.Button])
            self.big_princess = BigPrincess(self)
        else:
            self.items = []
            shower      = widget.GameText(t('Take a shower'),(360,400),self.level)
            ok_pos      = d(shower.pos[0]+(shower.size[0]/2)),d(shower.pos[1]+(shower.size[1]))+50
            ok_button   = widget.Button(directory.button_ok,ok_pos,self.level,self.clean_up)
            quit        = widget.GameText(t('Leave'),(1080,400),self.level)
            cancel_pos  = d(quit.pos[0]+(quit.size[0]/2)),d(quit.pos[1]+(quit.size[1]))+50
            cancel_button = widget.Button(directory.button_cancel,cancel_pos,self.level,self.all_set)
            title       = widget.GameText(t('Would you like to take a shower?'),(720,100),self.level)
            self.buttons    = (shower, ok_button, quit, cancel_button, title)
            self.menu = [(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__== widget.Button]
            self.big_princess = BigPrincess(self, pos = "center")
        self.locked = database.query.is_locked(self.level,'face','geisha')
        self.chosen_item = None
        self.chosen_number = 0
        self.music = os.path.join(directory.music,'menu.ogg')

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
        else:
            save.save_file(self.level)
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.flip(pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100)),1,0)
        pygame.image.save(thumbnail,os.path.join(directory.saves,self.level.princesses[0].name.encode('utf-8'),'thumbnail.PNG'))

    def clean_up(self):
        self.status = 'done'
        if self.level.princesses[0].dirt ==0:
            if self.locked:
                self.level.unlocking = {'type':'face','name':'geisha'}
                self.locked = False
                
        self.level.princesses[0].dirt = 0
        database.update.clean_up(self.level)
        print "You look lovely all cleaned up!"
        self.level.princesses[1] = None
        save.save_file(self.level)
        thumbnail = pygame.transform.flip(pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100)),1,0)
        pygame.image.save(thumbnail,os.path.join(directory.saves,self.level.princesses[0].name.encode('utf-8'),'thumbnail.PNG'))



    def NOTSETYET(self):
        pass

 

class Item():
    def __init__(self, room, name,index):
        self.name   = name
        self.level  = room.level
        self.room   = room
        self.type   = room.type_of_items
        if self.type != 'shower':
            self.image  = utils.img.image(os.path.join(directory.princess,self.type+'_'+name,'big_icons','0.png'))
            self.size   = self.image.get_size()
            self.pos    = [p(500,r=0)+(index*(self.size[0])),(self.level.universe.height/2)-(self.size[1]/2)]
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
                BP = self.room.big_princess
                j = os.path.join
                BP.images[BP.image_dict[self.type]] = utils.img.image(j(directory.princess,self.type+'_'+self.name,'big.png'), invert = True)
                self.room.chosen_glow.pos = self.pos[0]-p(40,r=0),self.pos[1]-p(40,r=0)
                if self.type == "hair":
                    if self.name in ("black","brown","rapunzel", "rastafari","red"):
                        BP.images[BP.image_dict["hair_back"]] = utils.img.image(j(directory.princess,self.type+'_'+self.name+"_back",'big.png'), invert = True)
                    else:
                        BP.images[BP.image_dict["hair_back"]] = None
                elif self.type == "dress":
                    if self.name in ("yellow","red"):
                        BP.images[BP.image_dict["armdress"]] = utils.img.image(j(directory.princess, 'sleeve_' + self.name,'big.png'),invert = True)
                    else:
                        BP.images[BP.image_dict["armdress"]] = None

class BigPrincess():
    def __init__(self, room, pos = "left"):
        self.room           = room
        if pos == "left":
            self.pos        = p((20,270))
        elif pos == "center":
            self.pos        = p((room.level.universe.width/2,270))
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
                img = utils.img.image(os.path.join(directory.princess,row[i],'big.png'), invert = True)
            else:
                img = None
            self.images += [img]


    def update_all(self):
        pass

    def all_set(self):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,os.path.join(saves_dir,self.level.princesses[0].name,'thumbnail.PNG'))

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class Princess_Home():
    def __init__(self, level, princess=None):
        print "Creating Princess Home: "+ princess['name'] 
        painting_screen = pygame.Surface((400,400), pygame.SRCALPHA).convert_alpha()
        if princess == settings.Rapunzel:
            painting_screen.blit(utils.img.image(os.path.join(directory.princess,'hair_rapunzel_back','big.png')),(0,0))
        images  = [utils.img.image(os.path.join(directory.princess,item,'big.png')) for item in ('skin_'+princess['skin'],princess['hair'])]
        for img in images:
            painting_screen.blit(img, (0,0))
        self.princess_image = painting_screen#utils.img.scale_image(painting_screen)
        self.princess_icon  = utils.img.image(os.path.join(directory.ball,princess['icon']))
        self.status = 'outside'
        self.level  = level
        mymessage = messages.princesses_phrases[random.randint(0,(len(messages.princesses_phrases)-1))]
        if '%s' in mymessage:
            self.message = mymessage %self.level.princesses[0].name
        else:
            self.message = mymessage
        self.items = []
        self.menu = []
        self.buttons = []
        self.buttons    = (
                    widget.Button(directory.button_ok,(410,450),self.level,self.all_set),
                    widget.GameText(self.message, (850,820), self.level, font_size = 40, box = (1100,400))
        )
        self.menu.extend([(i.pos[0]+(i.size[0]/4),i.pos[1]+(i.size[1]/4)) for i in self.buttons if i.__class__==widget.Button])
        princess_name = princess["name"].lower()
        cursor = self.level.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+princess_name+" WHERE id = (SELECT MAX(id) FROM "+princess_name+")").fetchone()
        [self.princess_image.blit(utils.img.image(os.path.join(directory.princess,row[i],'big.png')),(0,0)) for i in (
                    'face', 'dress', 'arm', 'accessory', 'shoes')]
        self.name=princess_name
        if self.name =="sleeping_beauty":
            self.name="sleeping"
        elif self.name == "snow_white":
            self.name="snowwhite"
        self.locked = database.query.is_locked(self.level,'hair',self.name)
        self.big_princess = BigPrincess(self)
        self.chosen_number = 0
        self.music = os.path.join(directory.music,'menu.ogg')

    def all_set(self):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,os.path.join(directory.saves,self.level.princesses[0].name,'thumbnail.PNG'))
        if self.locked:
            self.level.unlocking = {'type':'hair','name':self.name}
            self.locked = False


    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]

class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.music = os.path.join(directory.music,'menu.ogg')
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (widget.Button(directory.button_ok,(410,450),self.level,self.all_set),
                           widget.Button(t('Go to the Ball'),(1240,550),self.level, self.to_the_ball),
                           widget.GameText(t("It is not very cute to repeat your outfits. Check out what you wore at past Balls and try to find something different."), (720,750), level, box=(600,300)),
                           widget.GameText(t("Last Ball"),         (600,350), level, font_size = 25),
                           widget.GameText(t("Great Past Ball"),   (800,350), level, font_size = 25),
                           widget.GameText(t("3 Balls Ago"),       (1000,350),level, font_size = 25)
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
                        image.blit(utils.img.image(os.path.join(directory.princess,row[i],'stay','0.png'),(0,0)))
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
        self.images =  utils.img.OneSided(os.path.join(directory.interface,'select'))
        self.image = self.images.list[0]
        self.pos   = p(pos)

    def update_all(self):
        self.image = self.images.list[self.images.itnumber.next()]
        pass
