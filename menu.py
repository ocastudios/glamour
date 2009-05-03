import scenarios
import obj_images
import enemy
import skies
import floors
import clouds
import random
import moving_scenario
import glamour_stars
import princess
import panel
import pygame
import drapes
from pygame.locals import *

class MenuScreen():
    def __init__(self,universe,music=None,color=[230,230,230]):
        self.universe       = universe
        self.color          = color
        self.music          = music
        self.left_bar       = MenuBackground('data/images/interface/omni/left_bar/',[-800.,0],self,1)
        self.right_bar      = MenuBackground('data/images/interface/omni/left_bar/',[2000.,0],self,1,invert = True)
        self.bar            = self.left_bar

        self.menu = Menu(self,'menu')
        self.menu.main()

        self.backgrounds    = [self.left_bar]

        self.speed          = 5.
        self.drapes         = []
        self.upper_drapes   = []
        self.STEP           = self.update_drape
        self.count          = 0
        self.action         = 'open'
        for i in range(13):
            if i <= 5:      self.drapes.append(drapes.Drape(i,'right'))
            else:           self.drapes.append(drapes.Drape(i,'left'))
        for i in range(14):
            self.upper_drapes.append(drapes.UperDrape(i))

    def update_all(self,surface):
        surface.fill(self.color)
        self.STEP(surface)
        self.count += 1

    def update_drape(self,surface):
        for drape in self.drapes+self.upper_drapes:
            if self.count > 80:
                drape.action = self.action
            drape.update_all()
            surface.blit(drape.image,drape.position)

            ####### STEP #########
            if drape.position[1] < -drape.size[1]+100:
                self.STEP = self.update_left_bar

    def update_left_bar(self,surface):
        self.bar = self.left_bar
        if self.left_bar.position[0] < 0:
            self.left_bar.position[0] += self.speed
            if self.left_bar.position[0] > -280:    self.speed -= .5
            else:                           self.speed += .5
        else:
            self.left_bar.position[0] = 0
            ####### STEP #########
            self.STEP = self.update_menus
        surface.blit(self.left_bar.image,(self.left_bar.position[0],0))

    def update_right_bar(self,surface):
        self.bar = self.right_bar
        if self.right_bar.position[0]+516 > 1440:
            self.right_bar.position[0] -= self.speed
            if self.right_bar.position[0] < 1160:   self.speed += .5
            else:                           self.speed -= .5
        else:
            self.right_bar.position[0] = (1440-516)
            ####### STEP #######
            self.STEP = self.update_menus
        surface.blit(self.right_bar.image,(self.right_bar.position[0],0))

    def close_left_bar(self,surface):
        if self.left_bar.position[0] > -800:
            self.left_bar.position[0] -= self.speed
            self.speed += 1
        else:
            ####### STEP #######
            self.STEP = self.update_right_bar
            self.universe.level = 'choose_princess'
            self.action = 'open'
        surface.blit(self.left_bar.image,(self.left_bar.position[0],0))


    def update_menus(self,surface):
        if self.action == 'open':
            self.menu.action = self.action
        else:
            if self.menu.actual_position[1]<1200:
                self.menu.action = 'close'
            else:
                self.menu.select_princess()
                self.action = 'open'
                ####### STEP #######
                self.STEP = self.close_left_bar
        self.menu.update_all()

        for back in self.menu.backgrounds:
            back.update_all()
            surface.blit(back.image,self.menu.actual_position)
        surface.blit(self.bar.image,(self.bar.position[0],0))


        for item in [self.menu.texts, self.menu.options, self.menu.buttons]:
            for i in item:
                i.update_all()
                surface.blit(i.image,i.pos)



class Menu():
    def __init__(self,screen,level,position= [360,200],speed=2.):
        self.screen         = screen
        self.speed          = speed
        self.position       = position
        self.level          = level
        self.actual_position= [position[0],-600]
        self.selection_canvas = MenuBackground('data/images/interface/title_screen/selection_canvas/',self.actual_position,self,0)
        self.backgrounds    = [self.selection_canvas]
        self.itens          = []
        self.size           = self.selection_canvas.image.get_size()
        self.rect           = Rect(self.position,self.size)
        self.action         = None



    def main(self):
        self.action = 'open'
        self.actual_position = [self.position[0],-600]
        self.options = [ Options('New Game',        (300,100), self, 0, font_size=40, color=(255,84,84)),
                         Options('Load Game',       (300,180), self, 0, font_size=40, color=(255,84,84)),
                         Options('Play Story',      (300,260), self, 0, font_size=40, color=(255,84,84)),
                         Options('Choose Language', (300,340), self, 0, font_size=40, color=(255,84,84))]

        self.texts =    [GameText('Welcome to Glamour Game',(400,550),self,1),
                         GameText('This is the very first of some pretty cool games of OCA STUDIOS',(400,600),self,2),
                         GameText('Press i button in order to play Stage I',(400,650),self,3),
                         GameText('Or e button to play Stage "E"',(400,700),self,4)]
        self.buttons = [ MenuArrow('data/images/interface/title_screen/arrow_right/',(400,400),self,0),
                         MenuArrow('data/images/interface/title_screen/arrow_right/',(160,400),self,0,invert = True)]

    def select_princess(self):
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = [500,-600]
        self.options    = [Options('skintone',        (300,100), self, 0, font_size=40, color=(255,84,84))]

        self.texts =    [GameText(' A ',(400,550),self,1),
                         GameText('to Glamour Game',(400,550),self,2),
                         GameText('This is the very first of some pretty cool games of OCA STUDIOS',(400,600),self,3),
                         GameText('Press i  in order to play Stage I',(400,650),self,4),
                         GameText('Or e button to play Stage "E"',(400,700),self,5)]

        self.buttons    = [ MenuArrow('data/images/interface/title_screen/arrow_right/',(400,400),self,0),
                            MenuArrow('data/images/interface/title_screen/arrow_right/',(160,400),self,0,invert = True)
                         ]

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
                    if self.actual_position[1] < self.position[1] - 50: self.speed += 2
                else:
                    if self.actual_position[1] > self.position[1] + 50: self.speed -= 3


        elif self.action == 'close':
            if self.speed <85:
                self.speed += 2

        self.rect           = Rect(self.position,self.size)


class MenuBackground():

    def __init__(self,directory,position,menu,index,invert = False):
        self.position   = position
        self.images     = obj_images.OneSided(directory)
        if invert == True:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]
        self.index = index
        self.menu = menu



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

        self.image = self.images.list[self.images.number]
        self.images.update_number()

class MenuArrow():
    def __init__(self,directory,position,menu,index,invert = False):
        self.position   = position
        self.menu = menu
        self.images     = obj_images.OneSided(directory)
        if invert == True:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]
        self.index = index
        self.pos        = [self.menu.actual_position[0]+self.position[0],
                           self.menu.actual_position[1]+self.position[1]]


    def update_all(self):
        self.set_image()
        self.update_pos()


    def update_pos(self):
        self.pos  = [self.menu.actual_position[0]+self.position[0],
                     self.menu.actual_position[1]+self.position[1]]


    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list


    def set_image(self):
        #choose list
        number_of_files = len(self.images.list)-2
        self.image      = self.images.list[self.images.number]
        if self.images.number <= number_of_files:
            self.images.number +=1
        else:
            self.images.number = 0


class GameText():
    def __init__(self,text,pos,menu,index,fonte='Domestic_Manners.ttf',font_size=20, color=(0,0,0)):
        self.font_size  = font_size
        self.menu       = menu
        self.text       = text
        self.index      = index
        self.color      = color
        self.fontA      = pygame.font.Font('data/fonts/'+fonte,font_size).render(self.text,1,self.color)
        self.fontB      = pygame.font.Font('data/fonts/'+fonte,50).render(self.text,1,self.color)
        self.image      = self.fontA
        self.position   = pos
        self.size       = self.image.get_size()
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = Rect(self.pos,self.size)

    def update_all(self):
#        self.image  = self.font.render(self.text,1,self.color)
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]



class Options(GameText):
    hover = False
    def update_all(self):
        self.size       = self.image.get_size()
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = Rect(self.pos,self.size)
        self.click_detection()


    def click_detection(self):
        if -.5< self.menu.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.image = self.fontB
####################################### BUTTON ACTION ########################################
                if pygame.mouse.get_pressed() == (1,0,0):
                    self.menu.level = 'dress_st'

            else:
                self.image = self.fontA
class MenuPrincess():
    def __init__():
        self.hair = [pygame.image.load('data/images/princess/'+s+'/stay/0.png').convert_alpha() for s in ['skin_pink','skin_black','skin_tan']
                    ]
        self.skin = [
                    ]
        self.arm  = [
                    ]
        self.name = []
    
    



