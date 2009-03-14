import scenarios
import obj_images
import enemy
import skies
import globals
import floors
import clouds
import random
import moving_scenario
import glamour_stars
import princess
import panel
import pygame


class MainMenu():
    """This class is meant to create the menu of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the menus."""
    enemy_dir = 'data/images/enemies/'
    def __init__(self):
        self.texts          = []
        self.buttons        = []
        self.backgrounds    = []
#        self.music          = directory
        self.itens          = []
    def instantiate_stuff(self):
        newgame          = GameText('New Game',(540,300),self,0,size=40, color=(255,84,84))
        loadgame         = GameText('Load Game',(540,350),self,0,size=40, color=(255,84,84))
        playstory        = GameText('Play Story',(540,400),self,0,size=40, color=(255,84,84))
        chooselanguage   = GameText('Choose Language',(540,450),self,0,size=40, color=(255,84,84))
        hello_everybody  = GameText('Welcome to Glamour Game',(700,700),self,0)
        First_Oca_Game   = GameText('This is the very first of some pretty cool games of OCA STUDIOS',(700,750),self,1)
        Level_01_menu    = GameText('Press i button in order to play Stage I',(700,800),self,2)
        Level_02_menu    = GameText('Or e button to play Stage "E"',(700,850),self,3)
        selection_canvas = MenuBackground('data/images/interface/title_screen/selection_canvas/',(360,200),self,0)
        left_bar         = MenuBackground('data/images/interface/omni/left_bar/',(0,0),self,1)
        right_arrow      = MenuArrow('data/images/interface/title_screen/arrow_right/',(770,600),self,0)
        lef_arrow        = MenuArrow('data/images/interface/title_screen/arrow_right/',(530,600),self,0,invert = True)
    def update_all(self,surface):

        for back in self.backgrounds:
            back.update_all()
            surface.blit(back.image,back.position)
        for text in self.texts:
            text.update()
            surface.blit(text.blit_text,text.pos)
        for b in self.buttons:
            surface.blit(b.image,b.position) 
class GameText():
    def __init__(self,text,pos,menu,index,fonte='Domestic_Manners.ttf',size=20, color=(0,0,0)):
        self.text       = text
        self.index      = index
        self.pos        = pos
        self.font       = pygame.font.Font('data/fonts/'+fonte,size)
        self.color      = color
        self.blit_text  = self.font.render(self.text,1,self.color)
        self.menu       = menu
        self.menu.texts.insert(self.index,self)
    def update(self):
        self.blit_text  = self.font.render(self.text,1,self.color)
        self.menu.texts[self.index]=(self)
class MenuBackground():
    def __init__(self,directory,position,menu,index,invert = False):
        self.position   = position
        self.images     = obj_images.OneSided(directory)
        if invert == True:
            self.images.list = self.invert_images(self.images.list)

        self.image = self.images.list[self.images.number]
        self.index = index
        self.menu = menu
        self.insert_into_list()

    def insert_into_list(self):
        self.menu.backgrounds.insert(self.index,self)
    def update_all(self):
        self.set_image()
    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list
    def set_image(self):
        #choose list
        number_of_files = len(self.images.list)-2
        self.image = self.images.list[self.images.number]
        if self.images.number <= number_of_files:
            self.images.number +=1
        else:
            self.images.number = 0
class MenuArrow(MenuBackground):
    def insert_into_list(self):
        self.menu.buttons.insert(self.index,self)
