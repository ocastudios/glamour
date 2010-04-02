# -*- coding: utf-8 -*-
import obj_images
import princess
import pygame
import drapes
import os
from pygame.locals import *


import gettext
t = gettext.translation('glamour', 'locale')
_ = t.ugettext

items          = ['texts', 'options', 'buttons']
name_taken = False
pygame.mixer.music.load("data/sounds/music/menu.ogg")
pygame.mixer.music.play()

class MenuScreen():
    color = [230,230,230]
    def __init__(self,universe,music=None):
        interface_dir = 'data/images/interface/'
        self.universe       = universe
        self.left_bar       = MenuBackground(interface_dir+'omni/left_bar/',[-800.,0],self)
        self.right_bar      = MenuBackground(interface_dir+'omni/left_bar/',[2000.,0],self,invert = True)
        self.bar            = self.left_bar
        self.menu           = Menu(self,'menu')
        self.menu.main()
        self.backgrounds    = [self.left_bar]
        self.speed          = 5.
        self.drapes         = []
        self.upper_drapes   = []
        self.STEP           = self.update_drape
        self.count          = 0
        self.action         = 'open'
        self.hoover_letter = pygame.image.load(interface_dir+'title_screen/selection_letter/0.png').convert_alpha()
        self.hoover_letter_size = self.hoover_letter.get_size()
        self.hoover_large  = pygame.image.load(interface_dir+'title_screen/selection_back_space/0.png').convert_alpha()
        self.hoover_large_size = self.hoover_large.get_size()
        self.story_frames = []
        self.drapes         = [drapes.Drape(0,'right'),drapes.Drape(710,'left')]
        self.upper_drapes = drapes.UperDrape()


    def update_all(self):
        self.universe.screen_surface.fill(self.color)
        self.STEP(self.universe.screen_surface)
        self.count += 1

    def update_drape(self,surface):
#        if self.count > 80:
        for drape in self.drapes:
                drape.action = self.action
                drape.update_all()
                surface.blit(drape.image,drape.position)
            ####### STEP #######
        self.upper_drapes.action = self.action
        self.upper_drapes.update_all()
        surface.blit(self.upper_drapes.image,self.upper_drapes.position)        
        if self.upper_drapes.position[1] < -self.upper_drapes.size[1]+10:
            self.STEP = self.STEP_arrive_bar
            self.bar = self.left_bar

    def STEP_arrive_bar(self,surface):
        if self.bar == self.left_bar:
            if self.left_bar.position[0] < 0:
                self.left_bar.position[0] += self.speed
                if self.left_bar.position[0] > -280:
                    self.speed -= .5
                else:
                    self.speed += .5
            else:
                self.left_bar.position[0] = 0
                ####### STEP #########
                self.STEP = self.update_menus
        elif self.bar == self.right_bar:
            if self.right_bar.position[0]+516 > self.universe.width:
                self.right_bar.position[0] -= self.speed
                if self.right_bar.position[0] < ((self.universe.width-300)):
                    self.speed += .5
                else:
                    self.speed -= .5
            else:
                self.right_bar.position[0] = (1440-516)
                ####### STEP #######
                self.STEP = self.update_menus
            if self.menu.background:
                surface.blit(self.menu.background,(0,0))
        if self.bar:
            surface.blit(self.bar.image,(self.bar.position[0],0))

    def update_menus(self,surface):
        self.menu.update_all()
        if self.action == 'open':
            self.menu.action = self.action
        else:
            if self.menu.actual_position[1]<1200:
                self.menu.action = 'close'
            else:
                self.action = 'open'
                ####### STEP #######
                self.STEP = self.close_bar
        if self.menu.background:
            surface.blit(self.menu.background,(0,0))
        for back in self.menu.backgrounds:
            back.update_all()
            surface.blit(back.image,self.menu.actual_position)
        if self.bar:
            surface.blit(self.bar.image,(self.bar.position[0],0))

        if self.menu.story:
            self.menu.story.update_all()
            [surface.blit(i,(0,0)) for i in self.menu.story.images if i]

        for item in items:
            exec("for i in self.menu."+item+":\n    i.update_all()\n    surface.blit(i.image,i.pos)")
        for i in self.menu.options:
            if i.__class__ == Letter and i.hoover:
                surface.blit(self.hoover_letter,(i.pos[0]-((self.hoover_letter_size[0]-i.size[0])/2),
                                                 i.pos[1]-((self.hoover_letter_size[1]-i.size[1])/2) ))
            if (i.__class__ == Spacebar or i.__class__ == Backspace) and i.hoover:
                surface.blit(self.hoover_large,(i.pos[0]-((self.hoover_large_size[0]-i.size[0])/2),
                                                i.pos[1]-((self.hoover_large_size[1]-i.size[1])/2) ))
        if self.menu.print_princess:
            self.menu.princess.update_all()
            [surface.blit(i,self.menu.princess.pos) for i in self.menu.princess.images if i]
        if self.menu.princess:
            self.menu.princess.name.text = self.menu.princess.name.text.title()

    def close_bar(self,surface, call_bar = 'right'):
        width = self.universe.width
        if (-800 < self.bar.position[0] <10) or (width-self.bar.size[0] < self.bar.position[0] < width +1):
            self.bar.position[0] -= self.speed
            self.speed += 1
        else:
            ####### STEP #######
            if call_bar:
                self.STEP = self.STEP_arrive_bar
                if call_bar == 'right':
                    self.bar = self.right_bar
                elif call_bar == 'left':
                    self.bar = self.left_bar
            self.universe.LEVEL = 'menu'
            self.action = 'open'
            self.menu.next_menu()
        if self.menu.background:
            surface.blit(self.menu.background,(0,0))
        surface.blit(self.bar.image,(self.bar.position[0],0))


class Menu():
    def __init__(self,screen,level,position= [360,200],speed=2.):
        self.screen         = screen
        self.speed          = speed
        self.position       = position
        self.level          = level
        self.actual_position = [position[0],-600]
        self.selection_canvas = MenuBackground('data/images/interface/title_screen/selection_canvas/',self.actual_position,self)
        self.backgrounds    = [self.selection_canvas]
        self.size           = self.selection_canvas.image.get_size()
        self.action         = None
        self.next_menu      = self.select_princess
        self.print_princess = False
        self.princess       = None
        self.story          = None
        self.go_back        = False

    def main(self):
        self.background = None
        self.backgrounds= [self.selection_canvas]
        self.action = 'open'
        if not self.go_back:
            self.actual_position = [self.position[0],-600]

        else:
            self.actual_position = [self.position[0],1500]


        self.options = [ Options(_('New Game')  ,        (300,100), self, 'new_game', font_size=40, color=(255,84,84)),
                         Options(_('Load Game') ,       (300,180), self, 'load_game', font_size=40, color=(255,84,84)),
                         Options(_('Play Story'),      (300,260), self, 'play_story', font_size=40, color=(255,84,84)),
                         Options(_('Options')   , (300,340), self, 'choose_language', font_size=40, color=(255,84,84))]

        self.texts =    [
                         VerticalGameText(_('select one'),(120,200),self)
                        ]
        self.buttons = [ MenuArrow('data/images/interface/title_screen/arrow_right/',(410,450),self,self.NOTSETYET),
                         MenuArrow('data/images/interface/title_screen/arrow_right/',(200,450),self,self.NOTSETYET, invert = True)
                        ]

    def select_princess(self):
        self.backgrounds    = [self.selection_canvas]
        self.princess       = MenuPrincess(self)
        self.print_princess = True
        self.background = pygame.image.load('data/images/story/svg_bedroom.png').convert()
        self.action     = 'open'
        self.speed      = 0
        if not self.go_back:
            self.actual_position = [400,-600]
            print "go_back = False"
        else:
            self.actual_position = [400,300]
            print self.actual_position
            print "go_back = True"
        self.options    = []
        self.texts =    [GameText(_('Choose your'),(-200,200),self),
                         GameText(_('appearence...'),(-200,250),self),
                         GameText(_('skin tone'),(250,420),self),
                         GameText(_('previous'),(250,-40),self),
                         GameText(_('next'),(250,540),self)]

        D_TITLE_SCREEN = 'data/images/interface/title_screen/'
        self.buttons= [MenuArrow(D_TITLE_SCREEN+'arrow_right/',(380,430), self, self.change_princess,parameter = (1,'skin')),
                       MenuArrow(D_TITLE_SCREEN+'arrow_right/',(120,430), self, self.change_princess,parameter = (-1,'skin'), invert = True),
                       MenuArrow(D_TITLE_SCREEN+'arrow_up/',(250,-100),self,self.back_to_main),
                       MenuArrow(D_TITLE_SCREEN+'arrow_down/',(250,620),self,self.to_select_hair)]

    def select_hair(self):
        self.backgrounds    = [self.selection_canvas]
        self.action = 'open'
        self.speed = 0
        if not self.go_back:
            self.actual_position = [460,-600]
        else:
            self.actual_position[1] = [300]
            
#        self.actual_position = [460,-600]
        self.options    = []
        self.texts =    [GameText(_('Choose your'),(-200,200),self),
                         GameText(_('appearence...'),(-200,250),self),
                         GameText(_('hair style'),(250,420),self),
                         GameText(_('previous'),(250,-40),self),
                         GameText(_('next'),(250,540),self)]

        D_TITLE_SCREEN = 'data/images/interface/title_screen/'
        self.buttons= [MenuArrow(D_TITLE_SCREEN+'arrow_right/',(380,430), self, self.change_princess,parameter = (1,'hair')),
                       MenuArrow(D_TITLE_SCREEN+'arrow_right/',(120,430), self, self.change_princess,parameter = (-1,'hair'), invert = True),
                       MenuArrow(D_TITLE_SCREEN+'arrow_up/',(250,-100),self,self.back_to_select_princess),
                       MenuArrow(D_TITLE_SCREEN+'arrow_down/',(250,620),self,self.to_name_your_princess)]

    def name_your_princess(self):
        self.backgrounds    = [self.selection_canvas]
        self.print_princess = False
        self.action     = 'open'
        self.speed      = 0
        if not self.go_back:
            self.actual_position = [460,-600]
        else:
            self.actual_position[1] = [300]
#        self.actual_position = [460,-600]
        lowercase       = map(chr,xrange(97,123))
        positions       = [(i,a) for (i,a) in zip([x for n in xrange(9) for x in xrange(100,421,40)],
                                                  [n for n in xrange(200,351,50) for x in xrange(9)]   )]
        self.options    =   [Letter(i[0],i[1],self, self.screen.hoover_letter_size,
                            fonte = 'FreeSerif.ttf', font_size=40)
                            for i in zip(lowercase,positions)]
        self.options.extend([Backspace(_('< back'),  (140,350)  ,self,self.NOTSETYET,fonte = 'FreeSerif.ttf',font_size=30),
                             Spacebar(_('space >'), (360,350)  ,self,self.NOTSETYET,fonte = 'FreeSerif.ttf',font_size=30),
                             Options(_('done'),    (245,545)   ,self,'start_game',font_size=30)
                            ])
        if name_taken:
            self.texts = [  GameText(_('Sorry, This name is taken.'),(-200,200),self),
                            GameText(_('Please, choose another one'),(-200,250),self),
                            GameText('_ _ _ _ _ _ _', (230,130),self)
                        ]
        else:
            self.texts =    [GameText(_('... and your name'),(-200,200),self),
                            GameText('_ _ _ _ _ _ _', (230,130),self),
                            self.princess.name]
        title_dir = 'data/images/interface/title_screen/'
        self.buttons= [MenuArrow(title_dir+'arrow_right/',(360,400), self, self.change_princess,parameter = (1,'skin')),
                       MenuArrow(title_dir+'arrow_right/',(100,400), self, self.change_princess,parameter = (-1,'skin'), invert = True),
                       MenuArrow(title_dir+'button_ok/',(200,570),self,self.start_game)]

    def update_all(self):
        self.actual_position[1] += self.speed

        if self.action == 'open':
            if self.actual_position[1] != self.position[1]:
                #Breaks
                if self.position[1]+70 > self.actual_position[1] > self.position[1]-70:
                    if self.speed > 0:
                        self.speed -= self.speed*.15
                    elif self.speed < 0:
                        self.speed += -self.speed*.15

                elif self.actual_position[1] < self.position[1]:
                    if self.actual_position[1] < self.position[1] - 50:
                        self.speed += 2
                else:
                    if self.actual_position[1] > self.position[1] + 50:
                        self.speed -= 2

        elif self.action == 'close':
            if not self.go_back:
                if self.speed <85:
                    self.speed += 2
            else:
                if self.speed >-85:
                    self.speed -= 2

    ### Buttons functions ###
    def back_to_main(self):
        self.go_back = True
        self.next_menu = self.main
        self.screen.universe.LEVEL = 'close'

    def back_to_select_princess(self):
        self.go_back = True
        self.next_menu = self.select_princess
        self.screen.universe.LEVEL = 'close'

    def new_game(self):
        self.go_back = False
        self.next_menu = self.select_princess
        self.screen.universe.LEVEL = 'close'

    def load_game(self):
        self.go_back = False
        self.screen.universe.LEVEL = 'close'

    def play_story(self):
        self.go_back = False
        self.screen.universe.LEVEL = 'close'

    def choose_language(self):
        pass

    def start_game(self, using_saved_game=False):
        pygame.mixer.music.fadeout(4000)
        global name_taken
        if not using_saved_game:
            try:
                os.mkdir(self.screen.universe.main_dir+'/data/saves/'+self.princess.name.text)
                new_file = open('data/saves/' + self.princess.name.text + '/' + self.princess.name.text + '.glamour', 'w')
                new_file.write(
                            'name '+ str(self.princess.name.text) + '\n'
                            'center_distance 5220'+'\n'
                            'hairback      '+str(self.princess.hairs_back[self.princess.numbers['hair']])+' 0'+'\n'
                            'skin           '+self.princess.skins[self.princess.numbers['skin']]+' 1'+'\n'
                            'face           face_simple 2'+'\n'
                            'hair           '+self.princess.hairs[self.princess.numbers['hair']]+' 3'+'\n'
                            'shoes          shoes_slipper 4'+'\n'
                            'dress          dress_plain 5'+'\n'
                            'arm            '+self.princess.arms[self.princess.numbers['skin']]+' 6'+'\n'
                            'armdress      None 7'+'\n'
                            'accessory      accessory_ribbon 8'+'\n'
                            'dirt           0'+'\n'
                            '#Points'+'\n'
                            'points 0'+'\n'
                            '#Level'+'\n'
                            'level level'+'\n'
                            )
                new_file.close()
                self.screen.universe.LEVEL= 'start'
                self.screen.universe.file = open('data/saves/'+self.princess.name.text+'/'+self.princess.name.text+'.glamour')
                name_taken = False
            except:
                name_taken = True
                self.to_name_your_princess()
        else:
            self.screen.universe.LEVEL = 'start'
            self.screen.universe.file = using_saved_game

    def change_princess(self,list):#list of: int,part
        if list[1] == "hair":
            number = 4
        elif list[1] == 'skin':
            number = 2
        self.princess.numbers[list[1]] += list[0]
        if self.princess.numbers[list[1]] < 0:
            self.princess.numbers[list[1]] = number
        elif self.princess.numbers[list[1]] > number:
            self.princess.numbers[list[1]] = 0

####### To funcitons TODO: substitute this function #######
    def to_name_your_princess(self,param = None):
        self.next_menu = self.name_your_princess
        self.screen.universe.LEVEL = 'close'

    def to_select_hair(self,param):
        self.next_menu = self.select_hair
        self.screen.universe.LEVEL = 'close'

    def select_saved_game(self):
        directory = "data/saves/"
        saved_games = []
        for i in os.listdir(directory):
            try:
                files = os.listdir(directory+i)
                if 'thumbnail.PNG' in files:
                    saved_games.extend([{
                                    'name':i,
                                    'file': directory+i+'/'+i+'.glamour'
                                        }])
                else:
                    _('The '+i+' file is not well formed. The thumbnail was probably not saved. The saved file will not work without a thumbnail. Please, check this out in '+ directory+'/'+i)
            except:
                pass
        self.background = pygame.image.load('data/images/story/svg_bedroom.png').convert()
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = [500,-600]
        self.options    = []
        self.texts =    [GameText(_('Have you already saved a game?'),(50,-150),self),
                         GameText(_('Then choose your saved princess'),(50,-100),self)]
        ypos = 150
        xpos = 150
        self.buttons = []
        for i in saved_games:
            self.buttons.extend([MenuArrow(directory+i['name']+'/',(xpos,ypos),self, self.start_game, parameter=(i['file']))])
            self.texts.extend([GameText(i['name'],(xpos+100,ypos),self, font_size = 30)])
            ypos+=100
            if ypos > 550:
                ypos = 100
                xpos += 200

    def watching_story(self):
        title_dir = 'data/images/interface/title_screen/'
        self.story = Story_Frame(self)
        self.background = pygame.image.load('data/images/story/background/background.png').convert()
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = [500,-600]
        self.options    = []
        self.buttons= [MenuArrow(title_dir+'arrow_right/',(360,400), self, self.story.next_frame),
                       MenuArrow(title_dir+'arrow_right/',(100,400), self, self.story.past_frame, invert = True)]
        self.texts =   self.story.texts
        ypos = 150
        xpos = 150

    def NOTSETYET(self):
        pass


class MenuBackground():
    def __init__(self,directory,position,menu,invert = False):
        self.position   = position
        self.images     = obj_images.OneSided(directory)
        if invert:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]
        self.menu = menu
        self.size = self.image.get_size()

    def update_all(self):
        pass
#        self.set_image()

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def set_image(self):
        self.image = self.images.list[self.images.number]
        self.images.update_number()

class MenuArrow():
    def __init__(self,directory,position,menu,function,parameter = None,invert = False,):
        self.menu = menu
        self.images     = obj_images.Buttons(directory,5)
        if invert:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]
        self.size = self.image.get_size()
        self.position = position
        self.pos        = [self.menu.actual_position[0]+(self.position[0]-(self.image.get_size()[0]/2)),
                           self.menu.actual_position[1]+(self.position[1]-(self.image.get_size()[1])/2)]
        self.rect = Rect(self.pos,self.size)
        self.function = function
        self.parameter = parameter

    def update_all(self):
        self.update_pos()
        self.click_detection()

    def update_pos(self):
        self.pos  = [self.menu.actual_position[0]+(self.position[0]-(self.image.get_size()[0]/2)),
                     self.menu.actual_position[1]+(self.position[1]-(self.image.get_size()[1]/2))]
        self.rect = Rect(self.pos,self.size)

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        self.rect = Rect(self.pos,self.size)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.images.list[self.images.itnumber.next()]
            if self.menu.screen.universe.click:
                try:
                    self.function(self.parameter)
                except:
                    self.function()
        else:
            if self.image != self.images.list[0]:
                self.image = self.images.list[self.images.itnumber.next()]


class GameText():
    def __init__(self,text,pos,menu,fonte='Domestic_Manners.ttf', font_size=40, color=(0,0,0),second_font = 'Chopin_Script.ttf',var = False):
        self.font_size  = font_size
        self.font       = fonte
        self.menu       = menu
        self.text       = text
        self.color      = color
        self.fontA      = pygame.font.Font('data/fonts/'+fonte,font_size)
        self.fontB      = pygame.font.Font('data/fonts/'+second_font,font_size+(font_size/2))
        self.image      = self.fontA.render(self.text,1,self.color)
        self.position   = pos
        self.size       = self.image.get_size()
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = Rect(self.pos,self.size)
        self.variable_text = var

    def update_all(self):
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
        if self.variable_text:
            self.image = self.fontA.render(self.text,1,self.color)


class VerticalGameText(GameText):
    def __init__(self,text,pos,menu,fonte='Domestic_Manners.ttf',font_size = 40, color = (0,0,0)):
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.image = pygame.transform.rotate(self.image,90)

class Options(GameText):
    hoover = False
    def __init__(self,text,pos,menu,function,fonte='Domestic_Manners.ttf',font_size=20, color=(0,0,0)):
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.function = function

    def update_all(self):
        self.size       = self.image.get_size()
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = Rect(self.pos,self.size)
        self.type       = type
        self.click_detection()

    def click_detection(self):
        function = self.function
        if -.5< self.menu.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.image = self.fontB.render(self.text,1,self.color)
########################### BUTTON ACTION ############################
                if pygame.mouse.get_pressed() == (1,0,0):
                    exec('self.menu.'+function+'()')
            else:
                self.image = self.fontA.render(self.text,1,self.color)


class Letter(Options):
    def __init__(self,text,pos,menu,hoover_size,fonte='Domestic_Manners.ttf',font_size=20, color=(0,0,0)):
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.hoover_size = hoover_size
        self.size = 30,30
        self.rect = (self.pos,self.size)

    def click_detection(self):
        if -.5< self.menu.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hoover = True
####################################### BUTTON ACTION ########################################
                if self.menu.screen.universe.click:
                    self.menu.princess.name.text += self.text
            else:
                self.hoover = False


class Spacebar(Options):
    def click_detection(self):
        if -.5< self.menu.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hoover = True
####################################### BUTTON ACTION ########################################
                if self.menu.screen.universe.click:
                    self.menu.princess.name.text += ' '
            else:
                self.hoover = False


class Backspace(Options):
    def click_detection(self):
        if -.5< self.menu.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hoover = True
####################################### BUTTON ACTION ########################################
                if self.menu.screen.universe.click:
                    self.menu.princess.name.text = self.menu.princess.name.text[:-1]
            else:
                self.hoover = False

class MenuPrincess():
    def __init__(self,menu,thumbnail=None):
        dir = 'data/images/princess/'
        self.menu = menu
        if not thumbnail:
            self.skins = ('skin_pink','skin_black','skin_tan')
            self.arms  = ('arm_pink','arm_black','arm_tan')
            self.hairs = ('hair_yellow', 'hair_short', 'hair_brown', 'hair_rastafari', 'hair_red')
            self.hairs_back= (None, None, 'hair_brown_back', 'hair_rastafari_back','hair_red_back')
            self.skin = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in self.skins]
            self.arm  = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in self.arms]
            self.hair = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in self.hairs]
            self.hairback = [None,
                             None,
                             pygame.image.load(dir+self.hairs_back[2]+'/stay/0.png').convert_alpha(),
                             pygame.image.load(dir+self.hairs_back[3]+'/stay/0.png').convert_alpha(),
                             pygame.image.load(dir+self.hairs_back[4]+'/stay/0.png').convert_alpha()]
            self.numbers = {'skin':1,'hair':1}
            self.images = [ self.hairback[self.numbers['hair']],
                            self.skin[self.numbers['skin']],
                            pygame.image.load(dir+'face_simple/stay/0.png').convert_alpha(),
                            self.hair[self.numbers['hair']],
                            pygame.image.load(dir+'shoes_slipper/stay/0.png').convert_alpha(),
                            pygame.image.load(dir+'dress_plain/stay/0.png').convert_alpha(),
                            self.arm[self.numbers['skin']]
                            ]
            self.size = self.skin[0].get_size()
        else:
            self.images = pygame.image.load(thumbnail).convert_alpha()
        self.position = (250,250)
        self.name = GameText('maddeline',(170,120),self.menu,var = True)
        self.pos = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]

    def update_all(self):
        self.images[0]  = self.hairback[self.numbers['hair']]
        self.images[1]  = self.skin[self.numbers['skin']]
        self.images[3]  = self.hair[self.numbers['hair']]
        self.images[6]  = self.arm[self.numbers['skin']]
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]


class Story_Frame():
    def __init__(self, menu):
        directory = 'data/images/story/frames/'
        self.menu = menu
        image_frames = sorted(os.listdir(directory))
        sound_frames = sorted(os.listdir('data/sounds/story/frames/'))
        self.channel = pygame.mixer.Channel(0)
        self.available_images   = [pygame.image.load(directory+i).convert_alpha() for i in image_frames]
        self.available_sounds   = [pygame.mixer.Sound('data/sounds/story/frames/'+i) for i in sound_frames]
        self.flip_sound = pygame.mixer.Sound('data/sounds/story/sflip.ogg')
        self.frame_number   = 0
        self.texts =    [GameText(_('Use the arrows to go'),(230,150),self.menu,font_size = 25),
                         GameText(_('forward and backward'),(230,200),self.menu,font_size = 25),
                         GameText(_('And "Ok" for the menu.'),(230,250),self.menu,font_size = 25)]
    def update_all(self):
        self.images = [self.available_images[i] for i in range(0,self.frame_number)]

    def next_frame(self):
        self.channel.play(self.flip_sound)
        self.channel.queue(self.available_sounds[self.frame_number])
        self.frame_number += 1
        if self.frame_number:
            self.menu.screen.bar = None
            self.menu.texts = []
            self.menu.backgrounds = []

    def past_frame(self):
        self.channel.play(self.flip_sound)
        self.frame_number -= 1
        if self.frame_number == 0:
            self.menu.screen.bar = self.menu.screen.right_bar
            self.menu.texts = self.texts
            self.menu.backgrounds    = [self.menu.selection_canvas]