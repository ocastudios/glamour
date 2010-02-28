# -*- coding: utf-8 -*-
import obj_images
import princess
import pygame
import drapes
import os
import db
import sqlite3
from pygame.locals import *


import gettext
t = gettext.translation('glamour', 'locale')
_ = t.ugettext

items          = ['texts', 'options', 'buttons']
name_taken      = False
interface_D     = 'data/images/interface/'
title_screen_D  = interface_D+'title_screen/'


pygame.mixer.music.load("data/sounds/music/menu.ogg")
pygame.mixer.music.play()

from settings import *

def p(positions):
    return [int(i*scale) for i in positions ]


class MenuScreen():
    color = [230,230,230]
    def __init__(self,universe,music=None):
        self.universe       = universe
        self.bar_side       = None
        self.bar_left       = obj_images.image(interface_D+'omni/left_bar/0.png')
        self.bar_right      = pygame.transform.flip(self.bar_left,1,0)
        self.bar            = self.bar_left
        self.bar_size       = self.bar.get_size()
        self.bar_position   = -self.bar_size[0]
        self.menu           = Menu(self,self)
        self.menu.main()
        self.speed          = 5*scale
        self.drapes         = []
        self.upper_drapes   = []
        self.STEP           = self.update_drape
        self.count          = 0
        self.action         = 'open'
        self.hoover_letter  = obj_images.image(title_screen_D+'selection_letter/0.png')
        self.hoover_letter_size = self.hoover_letter.get_size()
        self.hoover_large   = obj_images.image(title_screen_D+'selection_back_space/0.png')
        self.hoover_large_size = self.hoover_large.get_size()
        self.story_frames   = []
        self.drapes         = [drapes.Drape(0,'right'),drapes.Drape(710*scale,'left')]
        self.upper_drapes   = drapes.UperDrape()
        self.menu_list      = {}
        self.screen         = self.universe.screen_surface


#STEP SEQUENCE
## 1- update_drape
## 2- arrive_bar
## 3- update_menus


    def update_all(self):
        self.screen.fill(self.color)
        self.STEP(self.screen)
        self.count += 1

    def update_drape(self,surface):
        for drape in self.drapes:
            drape.action = self.action
            drape.update_all()
            surface.blit(drape.image,(drape.x,0))
        self.upper_drapes.action = self.action
        self.upper_drapes.update_all()
        surface.blit(self.upper_drapes.image,(0,self.upper_drapes.y))
        if self.upper_drapes.y < -self.upper_drapes.size_y+10:
            self.STEP = self.STEP_arrive_bar ## Change the STEP
            self.bar_side = 'left'
            del self.drapes

    def STEP_arrive_bar(self,surface):
        if self.menu.back_background:
            surface.blit(self.menu.back_background,(0,0))
        if self.bar_side:
            surface.blit(self.bar,(self.bar_position,0))
            if self.bar_side == 'left':
                if self.bar_position < 0:
                    self.bar_position += self.speed
                    if self.bar_position > -200*scale:
                        self.speed -= .5
                    else:
                        self.speed += .5
                else:
                    self.bar_position = 0
                    self.STEP = self.update_menus ## Change the STEP
            elif self.bar_side == 'right':
                if self.bar_position+(516*scale) > self.universe.width:
                    self.bar_position -= self.speed
                    if self.bar_position < ((self.universe.width-(300*scale))):
                        self.speed += (.5*scale)
                    else:
                        self.speed -= (.5*scale)
                else:
                    self.bar_position = (1440-516)*scale
                    self.STEP = self.update_menus ## Change the STEP

    def update_menus(self,surface):
        if self.menu.back_background:
            surface.blit(self.menu.back_background,(0,0))
        if self.menu.background:
            surface.blit(self.menu.background,self.menu.actual_position)
        if self.bar_side:
            surface.blit(self.bar,(self.bar_position,0))
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
        self.menu.update_all()
        if self.action == 'open':
            self.menu.action = self.action
        else:
            if not self.menu.go_back:
                if self.menu.actual_position[1]<1200*scale:
                    self.menu.action = 'close'
                else:
                    self.action = 'open'
                    self.STEP = self.close_bar ## Change the STEP
            else:
                if self.menu.actual_position[1]>-600*scale:
                    self.menu.action = 'close'
                else:
                    self.action = 'open'
                    self.STEP = self.close_bar
        if self.menu.princess:
            self.menu.princess.name.text = self.menu.princess.name.text.title()

    def close_bar(self,surface, call_bar = 'right'):
        width = self.universe.width
        if (-800*scale < self.bar_position <10*scale) or (width-self.bar_size[0] < self.bar_position < width +1):
            self.bar_position -= self.speed
            self.speed += 1*scale
        else:
            ####### STEP #######
            if call_bar:
                self.STEP = self.STEP_arrive_bar
                if call_bar == 'right':
                    self.bar_side   = "right"
                elif call_bar == 'left':
                    self.bar_side = "left"
            self.action = 'open'
            self.menu.next_menu()
        if self.menu.back_background:
            surface.blit(self.menu.back_background,(0,0))
        surface.blit(self.bar,(self.bar_position,0))


class Menu():
    def __init__(self,screen,level,position= [360,200]):
        position = [position[0]*scale,position[1]*scale]
        self.screen         = screen
        self.speed          = 2*scale
        self.position       = position
        self.level          = level
        self.actual_position = [position[0],-600*scale]
        self.background     = obj_images.image(title_screen_D+'selection_canvas/0.png')
        self.size           = self.background.get_size()
        self.action         = None
        self.next_menu      = self.select_princess
        self.print_princess = False
        self.princess       = None
        self.story          = None
        self.go_back        = False
        self.back_background= None

    def main(self):
        self.back_background = None
        self.action = 'open'
        if not self.go_back:
            self.actual_position = [self.position[0],-600*scale]
        else:
            self.actual_position = [self.position[0],1500*scale]
        opt = (('New Game',100,'new_game'),('Load Game',180,'load_game'),('Play Story',260,'play_story'),('Options',340,'choose_language'))
        self.options = [ Options(_(i[0]), p((300,i[1])), self, i[2], font_size=40,color = (255,84,84)) for i in opt]
        self.level.menu_list={'New Game':p((310,105)),'Load Game':p((310,185)),'Play Story':p((310,265)),'Options':p((310,345))}
        self.texts =   [VerticalGameText(_('select one'),p((120,200)),self)]
        self.buttons = [ MenuArrow(title_screen_D+'arrow_right/',p((410,450)),self,self.NOTSETYET),
                         MenuArrow(title_screen_D+'arrow_right/',p((200,450)),self,self.NOTSETYET, invert = True)]

    def reset_menu(self, background = None, action = None, options = [], texts = [], buttons = []):
        if background:
            self.back_background    = obj_images.image(background)
        self.action         = action
        self.speed          = 0
        if not self.go_back:
            print "Going Forward"
            self.actual_position = [450*scale,-600*scale]
        else:
            print "Going Back"
            self.actual_position = [450*scale,300*scale]
        self.options        = options
        self.texts          = texts
        self.buttons        = buttons


    def select_princess(self):
        self.screen.bar = self.screen.bar_right
        self.screen.bar_position =  2000*scale
        self.princess       = MenuPrincess(self)
        self.print_princess = True
        txt=[('Choose your',[-200,200]),('appearence...',[-200,250]),('skin tone',[250,420]),('previous',[250,-40]),('next',[250,540])]
        self.reset_menu(
            background  = 'data/images/story/svg_bedroom.png',
            action      = 'open',
            texts = [GameText(_(i[0]),p(i[1]),self) for i in txt],
            buttons     =  [MenuArrow(title_screen_D+i[0],p(i[1]),self,i[2], parameter = i[3], invert = i[4]) for i in
                    (["arrow_right/",(380,430),self.change_princess,(1,'skin'),False],
                     ["arrow_right/",(120,430),self.change_princess,(-1,'skin'),True],
                     ["arrow_up/"   ,(250,-100),self.back_to_main,None,False],
                     ["arrow_down/"  ,(250,620),self.to_select_hair,None,False])]
                    )

    def select_hair(self):
        self.reset_menu(
                action  = 'open',
                texts   =  [GameText(_(i[0]),p(i[1]),self) for i in (
                    ('Choose your', (-200,200)),
                    ('appearence...',(-200,250)),
                    ('hair style',(250,420)),
                    ('previous',(250,-40)),
                    ('next',(250,540)))],
                buttons = [MenuArrow(title_screen_D+i[0],p(i[1]),self,i[2], parameter = i[3], invert = i[4]) for i in
                        (['arrow_right/',(380,430),self.change_princess,(1,'hair'),False],
                         ['arrow_right/',(120,430),self.change_princess,(-1,'hair'),True],
                         ['arrow_up/'   ,(250,-100),self.back_to_select_princess,None,False],
                         ['arrow_down/' ,(250,620),self.to_name_your_princess,None,False])])


    def name_your_princess(self):
        s = scale
        self.print_princess = False
        opt = [Letter(i[0],i[1],self, self.screen.hoover_letter_size, 'FreeSerif.ttf', 40) for i in zip(
                map(chr,xrange(97,123)),
                zip([x for n in xrange(9) for x in xrange(int(100*s),int(422*s),int(40*s))],
                    [n for n in xrange(int(200*s),int(352*s),int(50*s)) for x in xrange(9)]))] 
        opt.extend([Backspace(_('< back'),  (140*scale,350*scale)  ,self,self.NOTSETYET,fonte = 'FreeSerif.ttf',font_size=30),
            Spacebar(_('space >'),  (360*scale,350*scale)  ,self,self.NOTSETYET,fonte = 'FreeSerif.ttf',font_size=30),
            Options(_('done'),      (245*scale,500*scale)  ,self,'start_game',font_size=30)
           ])
        if name_taken:
            txts = [GameText(_(i[0]),p(i[1]),self) for i in (('Sorry, This name is taken.',(-200,200)),('Please, choose another one',(-200,250)),('_ _ _ _ _ _ _', (230,130)))]
        else:
            txts =[GameText(_('... and your name'),p((-200,200)),self), GameText('_ _ _ _ _ _ _', p((230,130)),self), self.princess.name]
        self.reset_menu(action  = 'open', options = opt, texts = txts,
                buttons = [MenuArrow(title_screen_D+i[0],p(i[1]),self,i[2],parameter=i[3],invert=i[4]) for i in (
                        ('arrow_right/',(360,400), self.change_princess,(1,'skin'),  False),
                        ('arrow_right/',(100,400), self.change_princess,(-1,'skin'), True),
                        ('button_ok/',  (200,600), self.start_game,    None,False))])

    def update_all(self):
        self.actual_position[1] += self.speed
        if self.action == 'open':
            if self.actual_position[1] != self.position[1]:
                #Breaks
                if self.position[1]+(70*scale) > self.actual_position[1] > self.position[1]-70*scale:
                    if self.speed > 0:
                        self.speed -= self.speed*.15*scale
                    elif self.speed < 0:
                        self.speed += -self.speed*.15*scale

                elif self.actual_position[1] < self.position[1]:
                    if self.actual_position[1] < self.position[1] - 50*scale:
                        self.speed += 2*scale
                else:
                    if self.actual_position[1] > self.position[1] + 50*scale:
                        self.speed -= 2*scale
        elif self.action == 'close':
            if not self.go_back:
                if self.speed < 85*scale:
                    self.speed += 2*scale
            else:
                if self.speed > -85*scale:
                    self.speed -= 2*scale

    ### Buttons functions ###
    def back_to_main(self):
        self.go_back = True
        self.next_menu = self.main
        self.screen.action = 'close'

    def back_to_select_princess(self):
        self.go_back = True
        self.next_menu = self.select_princess
        self.screen.action = 'close'

    def new_game(self):
        self.go_back = False
        self.next_menu = self.select_princess
        self.screen.action = 'close'

    def load_game(self):
        self.go_back = False        self.next_menu = self.select_saved_game
        self.screen.action = 'close'

    def play_story(self):
        self.go_back = False        self.next_menu = self.watching_story
        self.screen.action = 'close'

    def choose_language(self):
        pass

    def start_game(self, using_saved_game=False):
        pygame.mixer.music.fadeout(4000)
        global name_taken
        if not using_saved_game:
            try:
                print "criar diretorio"
                new_dir = self.screen.universe.main_dir+'/data/saves/'+self.princess.name.text
                os.mkdir(new_dir)
                db.create_save_db(new_dir+'/'+self.princess.name.text+'.db', self.princess.name.text)
                new_file = open(new_dir + '/' + self.princess.name.text + '.glamour', 'w')
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
                            'past_ball          None \n'
                            'great_past_ball    None\n'
                            'BathhouseSt    Bird Butterfly\n'
                            'DressSt        Bird\n'
                            'AccessorySt    Schnauzer\n'
                            'MakeupSt       OldLady\n'
                            'ShoesSt        FootBoy\n'
                            'Cinderella Accessory shades\n'
                            'Cinderella Dress red\n'
                            'Cinderella Shoes crystal\n'
                            'Cinderella Makeup eyeshades\n'
                            'Snow_White Accessory purse\n'
                            'Snow_White Dress yellow\n'
                            'Snow_White Shoes red\n'
                            'Snow_White Makeup eyelids\n'
                            'Sleeping_Beauty Accessory crown\n'
                            'Sleeping_Beauty Dress plain\n'
                            'Sleeping_Beauty Shoes slipper\n'
                            'Sleeping_Beauty Makeup simple\n'
                            'Rapunzel Accessory ribbon\n'
                            'Rapunzel Dress yellow\n'
                            'Rapunzel Shoes white\n'
                            'Rapunzel Makeup eyelids\n'
                            'Events '
                            )
                new_file.close()
                self.screen.universe.LEVEL= 'start'
                self.screen.universe.file = 'data/saves/'+self.princess.name.text+'/'+self.princess.name.text+'.glamour'
                name_taken = False
            except Exception, e:
                print "Maybe this name already existed"
                print str(e)
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

    def to_name_your_princess(self,param = None):
        self.go_back = False
        self.next_menu = self.name_your_princess
        self.screen.action = 'close'

    def to_select_hair(self,param):
        self.go_back = False
        self.next_menu = self.select_hair
        self.screen.action = 'close'

    def select_saved_game(self):
        self.screen.bar = self.screen.bar_right
        directory = "data/saves/"
        saved_games = []
        for i in os.listdir(directory):
            try:
                files = os.listdir(directory+i)
                if 'thumbnail.PNG' in files:
                    saved_games.extend([{'name':i, 'file': directory+i+'/'+i+'.glamour'}])
                else:
                    print _('The '+i+' file is not well formed. The thumbnail was probably not saved. The saved file will not work without a thumbnail. Please, check this out in '+ directory+i)
                    for f in files:
                        file_to_remove = os.getcwd()+'/'+directory+i+'/'+f
                        print "Removing "+file_to_remove
                        os.rm(file_to_remove)
                    print "removing directory "+directory+i
                    os.rmdir(os.getcwd()+'/'+directory+i+'/')
            except:
                pass
        self.back_background = obj_images.image('data/images/story/svg_bedroom.png')
        white_mask           = pygame.Surface(self.back_background.get_size(),pygame.SRCALPHA).convert_alpha()
        white_mask.fill((255,255,255,150))
        self.back_background.blit(white_mask,(0,0))
        self.background = None
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = [100*scale,-600*scale]
        self.options    = []
        self.texts =    [GameText(_('Have you already saved a game?'),p((250,-150)),self),
                         GameText(_('Then choose your saved princess'),p((250,-100)),self)]
        ypos = 0
        xpos = 0
        self.buttons = []
        for i in saved_games:
            self.buttons.extend([MenuArrow(directory+i['name']+'/',(xpos,ypos),self, self.start_game, parameter=(i['file']))])
            self.texts.extend([GameText(i['name'],(xpos+100,ypos),self, font_size = int(30))])
            ypos+=self.buttons[0].size[1]
            if ypos > 250:
                ypos = 0
                xpos += 400*scale

    def watching_story(self):
        title_dir = 'data/images/interface/title_screen/'
        self.screen.bar = self.screen.bar_right
        self.screen.bar_position =  2000*scale
        self.story = Story_Frame(self)
        self.back_background = obj_images.scale_image(pygame.image.load('data/images/story/background/background.png').convert())
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = p([500,-600])
        self.options    = []
        self.buttons= [MenuArrow(title_dir+'arrow_right/',p((360,400)), self, self.story.next_frame),
                       MenuArrow(title_dir+'arrow_right/',p((100,400)), self, self.story.past_frame, invert = True)]
        self.texts =   self.story.texts
        ypos = 150
        xpos = 150

    def NOTSETYET(self):
        pass


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
        return [pygame.transform.flip(img,1,0) for img in list]

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
        self.font_size  = int(font_size*scale)
        self.font       = fonte
        self.menu       = menu
        self.text       = text
        self.color      = color
        self.fontA      = pygame.font.Font('data/fonts/'+fonte,self.font_size)
        self.fontB      = pygame.font.Font('data/fonts/'+second_font,self.font_size+(self.font_size/2))
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
        font_size = int(font_size*scale)
        GameText.__init__(self,text,pos,menu,fonte,font_size,color)
        self.hoover_size = hoover_size
        self.size = p((30,30))
        
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
            self.skin = [obj_images.image(dir+i+'/stay/0.png') for i in self.skins]
            self.arm  = [obj_images.image(dir+i+'/stay/0.png') for i in self.arms]
            self.hair = [obj_images.image(dir+i+'/stay/0.png') for i in self.hairs]
            self.hairback = [None,
                             None,
                             obj_images.image(dir+self.hairs_back[2]+'/stay/0.png'),
                             obj_images.image(dir+self.hairs_back[3]+'/stay/0.png'),
                             obj_images.image(dir+self.hairs_back[4]+'/stay/0.png')]
            self.numbers = {'skin':1,'hair':1}
            self.images = [ self.hairback[self.numbers['hair']],
                            self.skin[self.numbers['skin']],
                            obj_images.image(dir+'face_simple/stay/0.png'),
                            self.hair[self.numbers['hair']],
                            obj_images.image(dir+'shoes_slipper/stay/0.png'),
                            obj_images.image(dir+'dress_plain/stay/0.png'),
                            self.arm[self.numbers['skin']]
                            ]
            self.size = self.skin[0].get_size()
        else:
            self.images = obj_images.image(thumbnail)
        self.position = (250*scale,250*scale)
        self.name = GameText('maddeline',(170*scale,120*scale),self.menu,var = True)
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
        self.available_images   = [obj_images.image(directory+i) for i in image_frames]
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
            self.menu.screen.bar_side = None
            self.menu.texts = []
            self.menu.backgrounds = []
            self.menu.background = None

    def past_frame(self):
        self.channel.play(self.flip_sound)
        self.frame_number -= 1
        if self.frame_number == 0:
            self.menu.screen.bar_side = 'right'
            self.menu.texts = self.texts
            self.menu.background = obj_images.image(title_screen_D+'selection_canvas/0.png')
