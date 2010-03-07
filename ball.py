import pygame
import obj_images
import random
from settings import *


def p(positions):
    return [int(i*scale) for i in positions ]

class Ball():
    directory = 'data/images/interface/ball/'
    def __init__(self, level, universe, princess):
        self.universe   = universe
        self.background      = pygame.Surface((level.universe.width,level.universe.height),pygame.SRCALPHA).convert_alpha()

        for file in (self.directory+'ball-back.png',self.directory+'back-bubbles.png'):
            self.background.blit(obj_images.scale_image(pygame.image.load(file).convert_alpha()), (0,0))
        self.left_bar   = VerticalBar(self)
        self.princess   = princess
        self.Bar        = VerticalBar(self)
        self.Frame      = BallFrame(self)
        self.level      = level
        self.dancers    = [Dancer(p(i)) for i in [1200,100],[200,200],[800,300],[600,400],[300,600]]
        self.buttons = [BallButton('data/images/interface/title_screen/button_ok/',(300*scale,200*scale), self.level)]
        pygame.mixer.music.load("data/sounds/music/strauss_waltz_wedley.ogg")
        pygame.mixer.music.play()
        general_enemies_list = ['Schnauzer', 'Bird', 'OldLady', 'FootBoy','Butterfly']
        stage_list           = ['BathhouseSt', 'DressSt', 'AccessorySt', 'MakeupSt','ShoesSt']
        for stage in stage_list:
            chosen_enemy = random.choice(general_enemies_list)
            self.level.enemies_list[stage] = [chosen_enemy]
            general_enemies_list.remove(chosen_enemy)
        self.level.enemies_list[random.choice(['DressSt', 'MakeupSt','ShoesSt'])].append('Carriage')

        princesses_list      = ['Cinderella', 'Snow_White', 'Sleeping_Beauty','Rapunzel']
        garment_list         = ['Accessory', 'Dress', 'Shoes','Makeup']
        Accessory_list       = ['crown', 'purse','ribbon','shades']
        Dress_list           = ['pink','plain','red','yellow']
        Shoes_list           = ['crystal','red','slipper','white']
        Makeup_list          = ['eyelids','eyeshades','lipstick','simple']
        self.princesses_garment = ''
        for princess in princesses_list:
#            exec(princess+'_dict = {"Acessory":"","Dress":"","Shoes":"","Makeup":""}')
            for garment in garment_list:
#                exec(princess+'_dict['+garment+'] = '+exec('random.choice('+garment+'_list)'))
                exec('item = random.choice('+garment+'_list)')
                self.princesses_garment = self.princesses_garment+princess+' '+garment+' '+item+' \n'
        print self.princesses_garment
        self.level.princesses_garment = self.princesses_garment[:-2]
        print self.level.princesses_garment
    def update_all(self):
        self.left_bar.update_all()
        self.level.game_mouse.update()
        self.universe.screen_surface.blit(self.background,(0,0))
        for i in self.dancers:
            self.universe.screen_surface.blit(i.image,i.position)
            i.update_all()
        self.universe.screen_surface.blit(self.Frame.image,self.Frame.position)
        self.Frame.update_all()
        self.universe.screen_surface.blit(self.Bar.image,self.Bar.position)
        self.Bar.update_all()
        for i in self.Frame.texts:
            self.universe.screen_surface.blit(i.image,i.pos)
            i.update_all()

        for i in self.Frame.princesses:
            self.universe.screen_surface.blit(i.image,i.pos)
            self.universe.screen_surface.blit(i.symbol,(i.symbolpos,i.pos[1]-100*scale))
            i.update_all()
        for i in self.buttons:
            self.universe.screen_surface.blit(i.image,i.pos)
            i.update_all()


class VerticalBar():
    def __init__(self, ball, right_or_left = 'left'):
        self.image = obj_images.scale_image(pygame.image.load('data/images/interface/ball/golden-bar.png').convert_alpha())
        if right_or_left == 'right':
            self.image = pygame.transform.flip(self.image, 1,0)
        self.size = self.image.get_size()
        self.position = [-self.size[0],0]
        self.speed = 5
        self.ready = False

    def update_all(self):
        if self.position[0] < 90*scale:
            self.position[0] += self.speed
            self.speed += 5
        else:
            self.position[0] = 90*scale
            self.ready = True


class BallFrame():
    def __init__(self, ball):
        self.image = obj_images.scale_image(pygame.image.load('data/images/interface/ball/back-frame.png').convert_alpha())
        self.size = self.image.get_size()
        self.position = [30*scale, -self.size[1]]
        self.speed = 5
        self.ball = ball
        self.princesses = [
                FairyTalePrincess(self, 100*scale, 'hair_snowwhite', 'pink', 'princess-icon-apple.png',  name = 'Snow_White'),
                FairyTalePrincess(self, 200*scale, 'hair_cinderella','tan','princess-icon-shoe.png',     name = 'Cinderella'),
                FairyTalePrincess(self, 300*scale, 'hair_rapunzel',  'pink', 'princess-icon-brush.png',  name = 'Rapunzel'),
                FairyTalePrincess(self, 400*scale, 'hair_sleeping',  'pink','princess-icon-spindle.png', name = 'Sleeping_Beauty')
                        ]
        self.texts = [
                VerticalGameText("Yesterday's ball", p((100,200)), self),
                VerticalGameText("Tonight's ball", p((100,500)), self),
                    ]

    def update_all(self):
        if self.ball:
            if self.position[1] + (self.size[1]/2) < (self.ball.universe.height/2):
                self.speed +=2
            else:
                self.speed = 0
            self.position[1] += self.speed


class FairyTalePrincess():
    def __init__(self, frame, position_x, hair, skin, icon, name = None):
        skin_body       = 'skin_'+skin
        skin_arm        = 'arm_'+skin
        princess_directory  = 'data/images/princess/'
        ball_directory      = 'data/images/interface/ball/'
        self.frame      = frame
        self.file       = frame.ball.universe.file
        self.image      = obj_images.scale_image(pygame.Surface((200,200),pygame.SRCALPHA).convert_alpha())
        if name == 'Rapunzel':
            self.image.blit(obj_images.image(princess_directory+'hair_rapunzel_back'+'/stay/0.png'),(0,0))
        images          = [obj_images.image(princess_directory+item+'/stay/0.png')
                                for item in (skin_body,hair)]
        self.position   = [position_x, 200*scale]
        for img in images:
            self.image.blit(img, (0,0))
        self.symbol     =  obj_images.image(ball_directory+icon)
        self.symbolpos  = position_x + (self.image.get_width()/2) - (self.symbol.get_width()/2)
        self.pos        = [ self.frame.position[0]+self.position[0],
                            self.frame.position[1]+self.position[1]]
        name_lower = name.lower()
        cursor = self.frame.ball.universe.db_cursor
        row     = cursor.execute("SELECT * FROM "+name_lower+" WHERE id = (SELECT MAX(id) FROM "+name_lower+")").fetchone()
        self.image.blit(obj_images.image(princess_directory+row['skin']+'/stay/0.png'),     (0,0))
        self.image.blit(obj_images.image(princess_directory+row['face']+'/stay/0.png'),     (0,0))
        self.image.blit(obj_images.image(princess_directory+row['dress']+'/stay/0.png'),    (0,0))
        self.image.blit(obj_images.image(princess_directory+row['accessory']+'/stay/0.png'),(0,0))
        self.image.blit(obj_images.image(princess_directory+row['shoes']+'/stay/0.png'),    (0,0))
        self.image = pygame.transform.flip(self.image,1,0)

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0],
                           self.frame.position[1]+self.position[1]]


class StarBall():
    def __init__(self):
        self.images = obj_images.OneSided('data/images/interface/ball/star-score/')
        self.image = self.images.list[self.images.itnumber()]
        self.position = (10,1000)

    def update_all(self):
        self.image = self.images.list[self.images.itnumber()]


class GameText():
    def __init__(self,text,pos,frame,fonte='Domestic_Manners.ttf', font_size=20, color=(0,0,0),second_font = 'Chopin_Script.ttf'):
        self.frame      = frame
        self.font      = pygame.font.Font('data/fonts/'+fonte,font_size*scale)
        self.image      = self.font.render(text,1,color)
        self.position   = pos
        self.size       = self.image.get_size()
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]

    def update_all(self):
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]


class VerticalGameText(GameText):
    def __init__(self,text,pos,menu, fonte='Domestic_Manners.ttf',font_size = 30, color = (0,0,0)):
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.image = pygame.transform.rotate(self.image,90)


class Dancer():
    def __init__(self, position):
        self.images = obj_images.There_and_back_again('data/images/interface/ball/dancers/', exclude_border = True)
        self.image  = self.images.list[self.images.itnumber.next()]
        self.position = position
        self.images.number = random.randint(0,20)
        if random.randint(0,9) < 4:
            self.list = self.images.left
        else:
            self.list = self.images.right

    def update_all(self):
        self.image  = self.images.list[self.images.number]
        self.images.update_number()


class BallButton():
    def __init__(self,directory,position,level):
        self.level      = level
        self.images     = obj_images.Buttons(directory,5)
        self.image      = self.images.list[self.images.number]
        self.size       = self.image.get_size()
        self.position   = position
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect       = pygame.Rect(self.pos,self.size)

    def update_all(self):
        self.update_pos()
        self.click_detection()

    def update_pos(self):
        self.pos        = [(self.position[0]-(self.image.get_size()[0]/2)),
                           (self.position[1]-(self.image.get_size()[1])/2)]
        self.rect = pygame.Rect(self.pos,self.size)

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        self.rect = pygame.Rect(self.pos,self.size)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.images.list[self.images.itnumber.next()]
            if self.level.universe.click:
                self.level.BathhouseSt(goalpos = 5520*scale)
                self.level.universe.clock_pointer.count = 0
        else:
            if self.image != self.images.list[0]:
                self.image = self.images.list[self.images.itnumber.next()]
