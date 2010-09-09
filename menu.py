# -*- coding: utf-8 -*-
import obj_images
import princess
import pygame
import drapes
import os
import mousepointer
import db
import sqlite3
import widget
from pygame.locals import *


import gettext
t = gettext.translation('glamour', 'locale')
_ = t.ugettext

items          = ['texts', 'options', 'buttons']
name_taken      = False
interface_D     = 'data/images/interface/'
title_screen_D  = interface_D+'title_screen/'

print "Initiating menu music."
pygame.mixer.music.load("data/sounds/music/menu.ogg")
pygame.mixer.music.play()

from settings import *

def p(positions):
    return [int(i*scale) for i in positions ]

class MenuScreen():
    color = [230,230,230]
    def __init__(self,universe):
        print "Creating MenuScreen"
        self.universe       = universe
        self.bar_side       = None
        self.bar_left       = obj_images.image(interface_D+'omni/left_bar/0.png')
        self.bar_right      = pygame.transform.flip(self.bar_left,1,0)
        self.bar            = self.bar_left
        self.bar_size       = self.bar.get_size()
        self.bar_position   = -self.bar_size[0]
        self.menu           = Menu(self)
        self.menu.main()
        self.speed          = 5*scale
        self.STEP           = self.update_drape
        self.count          = 0
        self.action         = 'open'
        self.hoover_letter  = obj_images.image(title_screen_D+'selection_letter/0.png')
        self.hoover_letter_size = self.hoover_letter.get_size()
        self.hoover_large   = obj_images.image(title_screen_D+'selection_back_space/0.png')
        self.hoover_large_size = self.hoover_large.get_size()
        self.story_frames   = []
        self.drapes         = drapes.Drape()
        self.upper_drapes   = drapes.UperDrape()
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
        self.drapes.action=self.action
        self.drapes.update_all()
        surface.blit(self.drapes.image,(0,0))
        self.upper_drapes.action = self.action
        self.upper_drapes.update_all()
        surface.blit(self.upper_drapes.image,(0,self.upper_drapes.y))
        if self.upper_drapes.y < -self.upper_drapes.size_y+10:
            self.STEP = self.STEP_arrive_bar ## Change the STEP
            self.bar_side = 'left'
            del self.drapes
            del self.upper_drapes

    def STEP_arrive_bar(self,surface):
        if self.menu.back_background:
            surface.blit(self.menu.back_background,(0,0))
        if self.bar_side:
            surface.blit(self.bar,(self.bar_position,0))
            if self.bar_side == 'left':
                if self.bar_position < 0:
                    self.bar_position += self.speed
                    if self.bar_position > int(-200*scale):
                        self.speed -= .5
                    else:
                        self.speed += .5
                else:
                    self.bar_position = 0
                    self.STEP = self.update_menus ## Change the STEP
            elif self.bar_side == 'right':
                if self.bar_position <10:
                    self.bar_position =  2000*scale
                if self.bar_position+(516*scale) > self.universe.width:
                    self.bar_position -= self.speed
                    if self.bar_position < int((self.universe.width-(300*scale))):
                        self.speed += (.5*scale)
                    else:
                        self.speed -= (.5*scale)
                else:
                    self.bar_position = int((1440-516)*scale)
                    self.STEP = self.update_menus ## Change the STEP

    def update_menus(self,surface):
        if self.menu.back_background:
            surface.blit(self.menu.back_background,(0,0))
        if self.menu.background:
            surface.blit(self.menu.background,self.menu.position)
        if self.bar_side:
            surface.blit(self.bar,(self.bar_position,0))
        if self.menu.story:
            self.menu.story.update_all()
            [surface.blit(i,(0,0)) for i in self.menu.story.images if i]


        for item in items:
            exec("for i in self.menu."+item+":\n    i.update_all()\n    surface.blit(i.image,i.pos)")
        for i in self.menu.options:
            if i.__class__ == widget.Letter and i.hoover:
                surface.blit(self.hoover_letter,(i.pos[0]-((self.hoover_letter_size[0]-i.size[0])/2),
                                                 i.pos[1]-((self.hoover_letter_size[1]-i.size[1])/2) ))
            if (i.__class__ == widget.Key) and i.hoover:
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
                if self.menu.position[1]<1200*scale:
                    self.menu.action = 'close'
                else:
                    self.action = 'open'
                    self.STEP = self.close_bar ## Change the STEP
            else:
                if self.menu.position[1]>-600*scale:
                    self.menu.action = 'close'
                else:
                    self.action = 'open'
                    self.STEP = self.close_bar
        if self.menu.princess:
            self.menu.princess.name.text = self.menu.princess.name.text.title()

        if self.menu.credits:
            surface.blit(self.menu.credits.background,self.menu.credits.pos)
#            [surface.blit(i.image,i.pos) for i in self.menu.credits.images if i]
            self.menu.credits.update_all()

    def close_bar(self,surface, call_bar = 'right'):
        width = 1440*scale
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
    selection_canvas = obj_images.image(title_screen_D+'selection_canvas/0.png')
    def __init__(self,screen,position= [360,200]):
        print "Creating main menu"
        position = [position[0]*scale,position[1]*scale]
        self.universe       = screen.universe
        self.screen         = screen
        self.speed          = 2*scale
        self.goal_pos       = position
        self.position= [position[0],-600*scale]
        self.background     = self.selection_canvas
        self.size           = self.background.get_size()
        self.action         = None
        self.next_menu      = self.select_princess
        self.print_princess = False
        self.princess       = None
        self.story          = None
        self.credits        = None
        self.go_back        = False
        self.back_background= None
        self.mouse_positions= []
        self.selector = 0
        self.game_mouse     = mousepointer.MousePointer(self, type = 2)
        self.mouse_pos      = pygame.mouse.get_pos()



    def main(self):
        self.print_princess = False
        self.background     = self.selection_canvas
        self.back_background = None
        self.action = 'open'
        if not self.go_back:
            self.position[1] = -600*scale
        else:
            self.position    = [450*scale,1000*scale]
        opt = ((_('New Game'),100,self.new_game),(_('Load Game'),180,self.load_game),(_('Play Story'),260,self.play_story),(_('Credits'),340,self.play_credits))
        self.options = [ widget.Button(i[0], (300,i[1]), self, i[2], font_size=40,color = (255,84,84)) for i in opt]
        self.texts =   [ widget.GameText(_('select one'),p((65,250)),self, rotate=90)]
        self.buttons = [ widget.Button(title_screen_D+'arrow_right/',(410,450),self,self.NOTSETYET),
                         widget.Button(title_screen_D+'arrow_right/',(200,450),self,self.NOTSETYET, invert = True)]

    def reset_menu(self, background = None, action = None, options = [], texts = [], buttons = []):
        self.story          = None
        self.credits        = None
        self.screen.story_frames = []
        self.background     = self.selection_canvas
        if background:
            self.back_background    = obj_images.image(background)
        self.action         = action
        self.speed          = 0
        if not self.go_back:
            print "Going Forward"
            self.position = [450*scale,-600*scale]
        else:
            print "Going Back"
            self.position = [450*scale,1000*scale]
        self.options        = options
        self.texts          = texts
        self.buttons        = buttons

    def select_princess(self):
        self.screen.bar = self.screen.bar_right
        self.princess       = MenuPrincess(self)
        self.print_princess = True
        txt=[(_('Choose your'),[-200,200]),(_('appearence...'),[-200,250]),(_('skin tone'),[250,420]),(_('previous'),[250,90]),(_('next'),[250,520])]
        self.reset_menu(
            background  = 'data/images/story/svg_bedroom.png',
            action      = 'open',
            texts = [widget.GameText(_(i[0]),p(i[1]),self) for i in txt],
            buttons     =  [widget.Button(title_screen_D+i[0],i[1],self,i[2], parameter = i[3], invert = i[4]) for i in
                    (["arrow_right/",(380,430),self.change_princess,[(1,'skin')],False],
                     ["arrow_right/",(120,430),self.change_princess,[(-1,'skin')],True],
                     ["arrow_up/"   ,(250,-5),self.back_to_main,None,False],
                     ["arrow_down/"  ,(250,620),self.to_select_hair,None,False])]
                    )

    def select_hair(self):
        txt = [(_('Choose your'), (-200,200)), (_('appearence...'),(-200,250)), (_('hair style'),(250,420)), (_('previous'),(250,90)), (_('next'),(250,520))]
        self.print_princess = True
        self.reset_menu(
                action  = 'open',
                texts   =  [widget.GameText(_(i[0]),p(i[1]),self) for i in txt],
                buttons = [widget.Button(title_screen_D+i[0],i[1],self,i[2], parameter = i[3], invert = i[4]) for i in
                        (['arrow_right/',(380,430),self.change_princess,[(1,'hair')],False],
                         ['arrow_right/',(120,430),self.change_princess,[(-1,'hair')],True],
                         ['arrow_up/'   ,(250,-5),self.back_to_select_princess,None,False],
                         ['arrow_down/' ,(250,620),self.to_name_your_princess,None,False])])


    def name_your_princess(self):
        s = scale
        self.print_princess = False
        opt = [widget.Letter(i[0],i[1],self, self.screen.hoover_letter_size, 'GentesqueRegular.otf', 40) for i in zip(
                map(chr,xrange(97,123)),
                zip([x for n in xrange(9) for x in xrange(int(100*s),int(422*s),int(40*s))],
                    [n for n in xrange(int(200*s),int(352*s),int(50*s)) for x in xrange(9)]))] 
        opt.extend([widget.Key(_('< back'),       (140*scale,350*scale)  ,self, 'Backspace'),
                    widget.Key(_('space >'),      (360*scale,350*scale)  ,self, 'Spacebar'),
                    widget.Key(_('clean up [  ]'),(140*scale,400*scale)  ,self, 'Cleanup'),
                    widget.Key(_('random   ???'), (360*scale,400*scale)  ,self, 'Random')
           ])

        buttom_list = [widget.Button(title_screen_D+i[0],i[1],self,i[2],parameter=i[3],invert=i[4]) for i in (
                         ['button_ok/',   (250,620), self.start_game,    None,False],
                         ['arrow_up/'   ,(250,-5),self.back_to_select_hair,None,False],
                        )]
        if name_taken:
            txts = [    widget.GameText(_('Sorry, This name is taken.'),p((-100,-150)),self),
                        widget.GameText(_('Please, choose another one'),p((-100,-50)),self),
                        widget.GameText(_('_ _ _ _ _ _ _'),p((230,130)),self),
                        self.princess.name
                    ]
            buttom_list.extend([widget.Button('or Overwrite it.',(-100,620), self, self.start_game, parameter=[False,True]) ])
        else:
            txts =[     widget.GameText(_('... and your name.'),p((-200,200)),self),
                        widget.GameText('_ _ _ _ _ _ _', p((230,130)),self),
                        self.princess.name]
        self.reset_menu(action  = 'open', options = opt, texts = txts, buttons = buttom_list)

    def update_all(self):
        self.game_mouse.update()
        self.mouse_pos  = self.game_mouse.mouse_pos
        self.mouse_positions = [i.rect.center for i in self.options+self.buttons]
        keyboard = self.screen.universe.action[0]
        if keyboard:
            if keyboard in ("up","left"):
                self.selector -=1
                if self.selector <0:
                    self.selector = len(self.mouse_positions)-1
            elif keyboard in ("down","right"):
                self.selector +=1
                if self.selector > len(self.mouse_positions)-1:
                    self.selector = 0
            pygame.mouse.set_pos(self.mouse_positions[self.selector])
        self.position[1] += self.speed

        if '_ _ _ _ _ _ _' in [i.text for i in self.texts]:
            if keyboard in ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"):
                self.princess.name.text += keyboard
            if keyboard == 'space':
                self.princess.name.text += ' '
            if keyboard == 'backspace':
                self.princess.name.text = self.princess.name.text[:-1]

        if self.action == 'open':
            if self.position[1] != self.goal_pos[1]:
                #Breaks
                if self.goal_pos[1]+(70*scale) > self.position[1] > self.goal_pos[1]-70*scale:
                    if self.speed > 0:
                        self.speed -= self.speed*.25
                    elif self.speed < 0:
                        self.speed += -self.speed*.25
                elif self.position[1] < self.goal_pos[1]:
                    if self.position[1] < self.goal_pos[1] - 50*scale:
                        self.speed+=2*scale
                else:
                    if self.position[1] > self.goal_pos[1] + 50*scale:
                        self.speed-=2*scale
        elif self.action == 'close':
            if not self.go_back:
                if self.speed < 85*scale:
                    self.speed += 2*scale
            else:
                if self.speed > -85*scale:
                    self.speed -= 2*scale
        self.universe.screen_surface.blit(self.game_mouse.image,self.game_mouse.pos)

    ### Buttons functions ###
    def back_to_main(self):
        self.story          = None
        self.credits        = None
        self.screen.story_frames = []
        self.go_back = True
        self.next_menu = self.main
        self.screen.action = 'close'

    def back_to_select_princess(self):
        self.go_back = True
        self.next_menu = self.select_princess
        self.screen.action = 'close'

    def back_to_select_hair(self):
        self.go_back = True
        self.next_menu = self.select_hair
        self.screen.action = 'close'

    def new_game(self):
        self.go_back = False
        self.next_menu = self.select_princess
        self.screen.action = 'close'

    def load_game(self):
        self.go_back = False
        self.next_menu = self.select_saved_game
        self.screen.action = 'close'

    def play_story(self):
        self.go_back = False
        self.next_menu = self.watching_story
        self.screen.action = 'close'

    def play_credits(self):
#        self.go_back = False
#        self.next_menu = self.watching_credits
        self.credits = Credits(self)

    def choose_language(self):
        pass

    def start_game(self, using_saved_game=False, start_anyway= False):
        pygame.mixer.music.fadeout(4000)
        if self.princess and self.princess.name.text == "":
            self.princess.name.text = "              "
        global name_taken
        if not using_saved_game:
            try:
                self.create_files()
                self.screen.universe.LEVEL= 'start'
                name_taken = False
            except Exception as  (errno, strerror):
                print "Maybe this name already existed"
                print strerror
                if errno == 17 and start_anyway:
                    self.remove_save_directory(self.princess.name.text)
                    self.create_files()
                    self.screen.universe.LEVEL= 'start'
                else:
                    name_taken = True
                    self.to_name_your_princess()
        else:
            print "Using saved game "+ using_saved_game
            print "Connecting to Database"
            db.connect_db(using_saved_game, self.screen.universe)
            self.screen.universe.LEVEL = 'start'

    def create_files(self,):
        print "Starting a New Save"
        new_dir = main_dir+'/data/saves/'+self.princess.name.text
        os.mkdir(new_dir)
        print "Directory Created"
        db.create_save_db(
                new_dir+'/'+self.princess.name.text+'.db',
                name = self.princess.name.text,
                hairback = self.princess.hairs_back[self.princess.numbers['hair']],
                skin = self.princess.skins[self.princess.numbers['skin']],
                hair = self.princess.hairs[self.princess.numbers['hair']],
                arm = self.princess.arms[self.princess.numbers['skin']],
                universe = self.screen.universe)
        print "Database Created"

    def change_princess(self,list):#list of: int,part
        if list[1] == "hair":
            number = 4
        elif list[1] == 'skin':
            number = 2
        self.princess.numbers[list[1]] += list[0]
        if   self.princess.numbers[list[1]] < 0:
             self.princess.numbers[list[1]] = number
        elif self.princess.numbers[list[1]] > number:
             self.princess.numbers[list[1]] = 0

    def to_name_your_princess(self):
        self.go_back = False
        self.next_menu = self.name_your_princess
        self.screen.action = 'close'

    def to_select_hair(self):
        self.go_back = False
        self.next_menu = self.select_hair
        self.screen.action = 'close'

    def select_saved_game(self):
        print "Let's select a saved princess"
        self.screen.bar = self.screen.bar_right
        directory = main_dir+"/data/saves/"
        saved_games = []
        print "searching for saved games"
        for i in os.listdir(directory):
            try:
                D = directory+i+'/'
                files = os.listdir(D)
                if 'thumbnail.PNG' in files:
                    saved_games.extend([{'name':i, 'file': directory+i+'/'+i+'.db'}])
                    print "Saved game found:\n"+str([{'name':i, 'file': directory+i+'/'+i+'.db'}])
                else:
                    print _('The '+i+' file is not well formed. The thumbnail was probably not saved. The saved file will not work without a thumbnail. Please, check this out in '+ directory+i)
                    for f in files:
                        file_to_remove = D+f
                        print "Removing "+file_to_remove
                        os.remove(file_to_remove)
                    print "removing directory "+D
                    os.rmdir(D)
            except:
                pass
        self.back_background = obj_images.image('data/images/story/svg_bedroom.png')
        white_mask           = pygame.Surface(self.back_background.get_size(),pygame.SRCALPHA).convert_alpha()
        white_mask.fill((255,255,255,150))
        self.back_background.blit(white_mask,(0,0))
        self.background = None
        self.action     = 'open'
        self.speed      = 0
        self.position = [100*scale,-600*scale]
        self.options    = [widget.Button(_('Or go back to Main Menu'), (245,500),self,self.back_to_main,font_size=40)]
        self.texts =    [widget.GameText(_('Have you already saved a game?'),p((250,-150)),self),
                         widget.GameText(_('Then choose your saved princess:'),p((250,-100)),self)]
        ypos = 0
        xpos = 0
        self.buttons = []
        for i in saved_games:
            self.buttons.extend([widget.Button(directory+i['name']+'/',(xpos,ypos),self, self.start_game, parameter=([i['file']]))])
            self.options.extend([
                                 widget.Button(i['name'],  (xpos+100,ypos), self,self.start_game, font_size=30, parameter=([i['file']])),
                                 widget.Button(_('erase'), (xpos+300,ypos) ,self,self.remove_save_directory,font_size=30, parameter=[i['name']])
                                ])
            ypos+=self.buttons[0].size[1]
            if ypos > 250:
                ypos = 0
                xpos += 400*scale

    def watching_story(self):
        print "Let's watch the story"
        title_dir = main_dir+'/data/images/interface/title_screen/'
        self.screen.bar = self.screen.bar_right
        self.story = Story_Frame(self)
        print "Loading story background"
        self.back_background = obj_images.image(main_dir+'/data/images/story/background/background.png')
        self.action     = 'open'
        self.speed      = 0
        self.position = [450*scale,-600*scale]
        self.options    = []
        self.buttons= [widget.Button(title_dir+'arrow_right/',(340,510), self, self.story.next_frame),
                       widget.Button(title_dir+'arrow_right/',(250,510), self, self.story.past_frame, invert = True)]
        self.texts =   self.story.texts

#    def watching_credits(self):
#        print "Let's watch the credits"
#        title_dir = main_dir+'/data/images/interface/title_screen/'
#        self.screen.bar = None
#        self.credits = Credits(self)
#        print "Loading credits background"
##        self.back_background = obj_images.image(main_dir+'/data/images/story/background/background.png')
#        self.action     = 'open'
#        self.speed      = 0
#        self.position = [450*scale,-600*scale]
#        self.options    = []
#        self.buttons= []
##        self.texts =   []

    def remove_save_directory(self, save_name):
        for root, dirs, files in os.walk(main_dir+'/data/saves/'+save_name+'/', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(main_dir+'/data/saves/'+save_name+'/')
        self.select_saved_game()

    def NOTSETYET(self):
        pass


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
        self.goal_pos = (250*scale,250*scale)
        self.name = widget.GameText('maddeline',(170*scale,120*scale),self.menu,var = True)
        self.pos = [self.menu.position[0]+self.goal_pos[0]-(self.size[0]/2),
                           self.menu.position[1]+self.goal_pos[1]-(self.size[1]/2)]

    def update_all(self):
        self.images[0]  = self.hairback[self.numbers['hair']]
        self.images[1]  = self.skin[self.numbers['skin']]
        self.images[3]  = self.hair[self.numbers['hair']]
        self.images[6]  = self.arm[self.numbers['skin']]
        self.pos        = [self.menu.position[0]+self.goal_pos[0]-(self.size[0]/2),
                           self.menu.position[1]+self.goal_pos[1]-(self.size[1]/2)]


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
        self.texts =    [widget.GameText(_('Use the arrows to go'),(220,150),self.menu,font_size = 25),
                         widget.GameText(_('forward and backward'),(220,200),self.menu,font_size = 25)]

    def update_all(self):
        self.images = [self.available_images[i] for i in range(0,self.frame_number)]

    def next_frame(self):
        self.channel.play(self.flip_sound)
        if self.frame_number >= len(self.available_images):
            self.menu.back_to_main()
        else:
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
        if self.frame_number == -1:
            self.menu.back_to_main()


class Credits():
    def __init__(self,menu):
        self.background = obj_images.image(main_dir+'/data/images/credits/fundo.png')
        self.menu       = menu
        self.pos        = p((0,100))
        developers = [
                ('isac',     main_dir+'/data/images/credits/isacvale.png'   ,(433,840)),
                ('ndvo',     main_dir+'/data/images/credits/ndvo.png'       ,(265,631)),
                ('raquel',   main_dir+'/data/images/credits/raquel.png'     ,(986,631)),
                ('sergio',   main_dir+'/data/images/credits/sergio.png'     ,(810,840))
                            ]
        rendered_texts      = [
                ('cilda&sara',  main_dir+'/data/images/credits/text_cilda_e_sara.png'   ,(590,462)),
                ('isac&sergio', main_dir+'/data/images/credits/text_isac_e_sergio.png'  ,(614,950)),
                ('ndvo',        main_dir+'/data/images/credits/text_ndvo.png'           ,(415,790)),
                ('ndvo&isac',   main_dir+'/data/images/credits/text_ndvo_e_isac.png'    ,(601,1200)),
                ('ocastudios',  main_dir+'/data/images/credits/text_ocastudios.png'     ,(514,1251)),
                ('raquel',      main_dir+'/data/images/credits/text_raquel.png'         ,(841,790))
                            ]
        texts_chopin = [
            ('in loving memory of'  ,(713,436),44,(0,0,0,255)),
            ('and'                  ,(701,520),24,(0,0,0,255)),
            ('Credits'              ,(693,711),75,(0,0,0,255)),
            ('Programming'          ,(485,769),34,(0,0,0,255)),
            ('Support'              ,(934,769),34,(0,0,0,255)),
            ('Design'               ,(682,930),34,(0,0,0,255)),
            ('Music',                (704,1400),54,(0,0,0,255)),
            ('first snowfall',       (583,1448),44,(128,0,0,255)),
            ('endless blue',         (650,1489),44,(128,0,0,255)),
            ('celtic cappricio',     (762,1530),44,(128,0,0,255)),
            ('the bee',              (488,1572),44,(128,0,0,255)),
            ("lonesome man's dance", (684,1612),44,(128,0,0,255)),
            ('dragon dance',         (754,1657),44,(128,0,0,255)),
            ('ship of fools',        (829,1695),44,(128,0,0,255)),
            ('sword fight',          (684,1733),44,(128,0,0,255)),
            ('the foggy dew',        (615,1778),44,(128,0,0,255)),
            ('revolution on resoluti on', (828,1820),44,(128,0,0,255)),
            ('twilight on mountain', (907,1858),44,(128,0,0,255)),
            ('brian boru 2',         (770,1899),44,(128,0,0,255)),
            ('ignition',             (830,1934),44,(128,0,0,255)),
            ('first snowfall',       (750,1975),44,(128,0,0,255)),
            ('cocci ci tini cocci',  (780,2012),44,(128,0,0,255)),
            ('first snowfall',       (826,2053),44,(128,0,0,255)),
            ('waltz wedley',         (972,2100),44,(128,0,0,255))
           ]
        texts_gentesque = [
            ('All python & pygame code, written in gedit (really!).',(501,841),16,(180,60)),
            ('Bureaucracy and et ceteras',(909,837),16,(110,60)),
            ('Almost all Inkscape, with a touch of Blender and Gimp.', (704,1027),16,(200,60)),
            ('based on the homonimous board game by',(699,1179),22,None),
            ('available at',        (703,1237),22,None),
            ('introduction',        (427,1458),14,None),
            ('by Torley on Piano',  (754,1458),14,None),
            ('menu',                (540,1499),14,None),
            ('by Armolithae',       (800,1499),14,None),
            ('bathhouse st',        (588,1540),14,None),
            ('by armolithae',       (938,1540),14,None),
            ('dress st',            (400,1582),14,None),
            ('by Ceili Moss',       (600,1582),14,None),
            ("shoe's st",           (500,1622),14,None),
            ("by Ceili Moss",       (900,1622),14,None),
            ('accessory st.',       (600,1667),14,None),
            ('by Butterfly Tea',    (920,1667),14,None),
            ('make-up st.',         (700,1705),14,None),
            ('by Ceili Moss',       (961,1705),14,None),
            ('schnauzer',           (550,1743),14,None),
            ('by Armolithae',       (821,1743),14,None),
            ('carriage',            (470,1788),14,None),
            ('by Ceili Moss',       (760,1788),14,None),
            ('old lady',            (610,1830),14,None),
            ('by Torly on Piano',   (1080,1830),14,None),
            ('viking',              (720,1868),14,None),
            ('by Armolithae',       (1100,1868),14,None),
            ('butterffly',          (620,1909),14,None),
            ('by Adragante',        (920,1899),14,None),
            ('hawk',                (750,1944),14,None),
            ('by Armolithae',       (950,1944),14,None),
            ('birdie',              (600,1985),14,None),
            ('by Torley on Piano',  (950,1985),14,None),
            ('fabrizio',            (600,2022),14,None),
            ('by Picari',           (960,2022),14,None),
            ('zoo',                 (700,2063),14,None),
            ('by Torley on Piano',  (980,2063),14,None),
            ('ball',                (831,2110),14,None),
            ('by strauss',          (1095,2110),14,None),
            ('Sad and unfortunate legal mambo jambo',(830,2290),14,None),
            ("All programming and art are public domain, released so by us, their authors.",(800,2335),14,None),
            ("The musics, however, comes in a variety of free licenses. They can be used and altered, even commercially, but credit MUST be given. Special thanks to www.jamendo.com, from where most of our music came.",(850,2375),14,(720,90)),
            ("( If you are an author and want your music out of this game, contact us and we'll promptly remove it. )",(800,2385),13,None),
            ("And then there are the fonts: Gentesque, by Paulo Silva, is in OpenFont License while Chopin Script, by Diogene, is in Public Domain (hurray!).",(830,2415),13,(720,60)),
            ("If you are a developer of free content, please consider the limitations the varying \"free licenses\" impose on derivative works. Tons (or better yet, Teras) of cultural content, as images, music and fonts that are \"free\" are quite unuseable due to legal and procedural restraints (we just cannot give credit to every bit of data we'll use). \"Free for personnal use, but not commercial\", \"free for use, but not to alter\" and/or \"free for use, but not to distribute\" hinders freedom, and equals \"free as in beer, not as in speech\". Giving credit to a music used is fair and doable, but not to the recording of step sounds, for example, or other minuscule but necessary files. Please help us spread and create upon your work by releasing it either in public domain or in GPL - avoid semi-free, non-standard and multiple-standard licenses. These just end up torturing developers with pages of sad and unfortunate license disclaimers... such as this.",(900,2525),13,(720,220)),
            ("want to congratulate or complain? do it to glamour@ocastudios.com", (1000,2540),14,None)
           ]
        self.images = developers+rendered_texts
        self.texts = [ widget.GameText(i[0],p(i[1]),self,fonte='Chopin_Script.ttf', font_size=i[2], color=i[3]) for i in texts_chopin]+[
                       widget.GameText(i[0],p(i[1]),self,fonte='GentesqueRegular.otf', font_size=i[2], color=(0,0,0,255),box = i[3]) for i in texts_gentesque]
        for i in self.images:
            print i
            self.background.blit(obj_images.image(i[1]),p(i[2]))
        for i in self.texts:
            self.background.blit(i.image,i.pos)


    def update_all(self):
        if self.pos[1] > -(3020*scale):
            self.pos[1]-=(1*scale)
        else:
            self.pos[1] = 1000*scale
            self.menu.credits = None
