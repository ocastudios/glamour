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
        dir = main_dir+'/data/images/interface/title_screen/'
        if item_type != 'shower':
            counter = itertools.count()
            self.items = [Item(self, i,counter.next()) for i in item_list]
            self.arrow = Arrow(self, pos = [-200,500], degree = 90)
            self.buttons    = (
                 Button(dir+'button_ok/',(410,530),self.level,self.all_set),
                 self.arrow
                                )
        self.chosen_item = None
        self.big_princess = BigPrincess(self)

    def forward(self,param):
#        for i in self.items:
#            i.queue_pos -= 1
        self.level.universe.click = False

    def rewind(self,param):
        for i in self.items:
            i.queue_pos += 1
        self.level.universe.click = False

    def all_set(self,param):
        self.status = 'done'
        exec('save.save_file(self.level,'+self.type_of_items+' = "'+self.type_of_items+"_"+self.chosen_item.name+'")')
        self.level.princesses[0] = princess.Princess(self.level, INSIDE = True)
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,main_dir+'/data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

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
            self.fontA      = pygame.font.Font(main_dir+'/data/fonts/'+fonte,font_size)
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
    def __init__(self, room, directory,index):
        self.name   = directory
        self.level  = room.level
        self.room   = room
        self.type   = room.type_of_items
        if self.type != 'shower':
            self.image  = obj_images.scale_image(pygame.image.load(main_dir+'/data/images/princess/'+self.type+'_'+directory+'/stay/0.png').convert_alpha())
            self.size   = self.image.get_size()
            self.pos    = [400*scale+(index*(self.size[0]/2)),(self.level.universe.height/2)-(self.size[1]/2)]
            self.speed  = 1
        self.rect       = pygame.Rect((self.pos[0]+(self.size[0]/4),self.pos[1]),(self.size[0]-(self.size[0]/4),self.size[1]))
        self.active     = False

    def update_all(self):
        self.click_detection()

    def click_detection(self):
        if self.rect.colliderect(self.level.game_mouse.rect):
            self.active = True
            if self.level.universe.click:
                print "updating "+self.type+" "+self.name
                self.room.chosen_item = self
                self.room.big_princess.images[self.room.big_princess.image_dict[self.type]] = obj_images.image(main_dir+'/data/images/princess/'+self.type+'_'+self.name+"/big.png")
                self.room.arrow.pos[0] = (self.pos[0]+(100*scale))-(self.room.arrow.image.get_width()/2)
                if self.type == "hair":
                    if self.name in ("black","brown","rapunzel", "rastafari","red"):
                        self.room.big_princess.images[self.room.big_princess.image_dict["hair_back"]] = obj_images.image(main_dir+'/data/images/princess/'+self.type+'_'+self.name+"_back/big.png")
                    else:
                        self.room.big_princess.images[self.room.big_princess.image_dict["hair_back"]] = None

class BigPrincess():
    def __init__(self, room):
        self.room           = room
        princess_directory  = main_dir+'/data/images/princess/'
        ball_directory      = main_dir+'/data/images/interface/ball/'
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
                img = obj_images.image(princess_directory+row[i]+"/big.png")
            else:
                img = None
            self.images += [img]

    def update_all(self):
        pass

    def all_set(self,param):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,main_dir+'/data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button(main_dir+'/data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
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
        pygame.image.save(thumbnail,main_dir+'/data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

class Princess_Home():
    def __init__(self, level, princess=None):
        print "Creating Princess Home: "+ princess['name'] 
        princess_directory  = main_dir+'/data/images/princess/'
        ball_directory      = main_dir+'/data/images/interface/ball/'
        painting_screen = pygame.Surface((400,400), pygame.SRCALPHA).convert_alpha()
        if princess == Rapunzel:
            painting_screen.blit(pygame.image.load(princess_directory+'hair_rapunzel_back'+'/big.png').convert_alpha(),(0,0))
        images  = [pygame.image.load(princess_directory+item+'/big.png').convert_alpha() for item in ('skin_'+princess['skin'],princess['hair'])]
        for img in images:
            painting_screen.blit(img, (0,0))
        self.princess_image = obj_images.scale_image(painting_screen)
        self.princess_icon  =  obj_images.scale_image( pygame.image.load(ball_directory+princess['icon']).convert_alpha())
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button(main_dir+'/data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),)

        princess_name = princess["name"].lower()
        cursor = self.level.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+princess_name+" WHERE id = (SELECT MAX(id) FROM "+princess_name+")").fetchone()
        self.princess_image.blit(obj_images.image(princess_directory+row['face']+'/big.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['dress']+'/big.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['arm']+'/big.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['accessory']+'/big.png'),(0,0))
        self.princess_image.blit(obj_images.image(princess_directory+row['shoes']+'/big.png'),(0,0))
        self.princess_image = pygame.transform.flip(self.princess_image,1,0)
        self.big_princess = BigPrincess(self)

    def all_set(self,param):
        self.status = 'done'
        thumbnail = pygame.transform.smoothscale(self.level.princesses[0].stay_img.left[0],(100,100))
        pygame.image.save(thumbnail,main_dir+'/data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]

class Home():
    def __init__(self, level):
        self.status = 'outside'
        self.level  = level
        self.items = []
        self.buttons = []
        self.buttons    = (Button(main_dir+'/data/images/interface/title_screen/button_ok/',(410,450),self.level,self.all_set),
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
        pygame.image.save(thumbnail,main_dir+'/data/saves/'+self.level.princesses[0].name+'/thumbnail.PNG')

class Arrow():
    def __init__(self,room, pos = [0,0], degree = 0):
        if not degree:
            self.image = obj_images.image(main_dir+'/data/images/interface/title_screen/arrow_right/0.png')
        else:
            self.image = pygame.transform.rotate(obj_images.image(main_dir+'/data/images/interface/title_screen/arrow_right/0.png'),degree)
        self.pos   = p(pos)
    def update_all(self):
        pass
