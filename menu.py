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
#        self.music          = directory
        self.background     = pygame.image.load('data/images/interface/ball/ball-back.png').convert()
        self.itens          = []
    def instantiate_stuff(self):
        hello_everybody = GameText('Welcome to Glamour Game',(100,200),self,0)
        First_Oca_Game  = GameText('This is the very first of some pretty cool games of OCA STUDIOS',(100,300),self,1)
        Level_01_menu  = GameText('Press i button in order to play Stage I',(100,500),self,2)
        Level_02_menu  = GameText('Or e button to play Stage "E"',(100,600),self,3)
    def update_all(self,surface):
        for text in self.texts:
            text.update()
            surface.blit(text.blit_text,text.pos)
class GameText():
    def __init__(self,text,pos,menu,index,fonte='Domestic_Manners.ttf',size=40):
        self.text       = text
        self.index      = index
        self.pos        = pos
        self.font       = pygame.font.Font('data/fonts/'+fonte,size)
        self.blit_text  = self.font.render(self.text,1,(0,0,0))
        self.menu       = menu
        self.menu.texts.insert(self.index,self)
    def update(self):
        self.blit_text  = self.font.render(self.text,1,(0,0,0))
        self.menu.texts[self.index]=(self)
