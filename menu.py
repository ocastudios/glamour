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

    def update_all(self):
        self.universe.screen_surface.fill(self.color)
        self.STEP(self.universe.screen_surface)
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
            else:                                   self.speed += .5
        else:
            self.left_bar.position[0] = 0
            ####### STEP #########
            self.STEP = self.update_menus
        surface.blit(self.left_bar.image,(self.left_bar.position[0],0))

    def update_right_bar(self,surface):
        self.bar = self.right_bar
        if self.right_bar.position[0]+516 > self.universe.width:
            self.right_bar.position[0] -= self.speed
            if self.right_bar.position[0] < ((self.universe.width-300)):   self.speed += .5
            else:                           self.speed -= .5
        else:
            self.right_bar.position[0] = (1440-516)
            ####### STEP #######
            self.STEP = self.update_menus

        if self.menu.background:
            surface.blit(self.menu.background,(0,0))
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
            self.menu.select_princess()
        surface.blit(self.left_bar.image,(self.left_bar.position[0],0))


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
                self.STEP = self.close_left_bar
        if self.menu.background:
            surface.blit(self.menu.background,(0,0))


        for back in self.menu.backgrounds:
            back.update_all()
            surface.blit(back.image,self.menu.actual_position)

        surface.blit(self.bar.image,(self.bar.position[0],0))


        for item in [self.menu.texts, self.menu.options, self.menu.buttons]:
            for i in item:
                i.update_all()
                surface.blit(i.image,i.pos)
        if self.menu.princess:
            self.menu.princess.update_all()
            for i in self.menu.princess.images:
                surface.blit(i,self.menu.princess.pos)
        for i in self.menu.options:
            i.click_detection()




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
        self.princess = None
        self.background = None
        self.action = 'open'
        self.actual_position = [self.position[0],-600]
        self.options = [ Options('New Game',        (300,100), self, 0, font_size=40, color=(255,84,84)),
                         Options('Load Game',       (300,180), self, 0, font_size=40, color=(255,84,84)),
                         Options('Play Story',      (300,260), self, 0, font_size=40, color=(255,84,84)),
                         Options('Choose Language', (300,340), self, 0, font_size=40, color=(255,84,84))]

        self.texts =    [GameText('Welcome to Glamour Game',(400,550),self,1),
                         GameText('This is the very first of some pretty cool games of OCA STUDIOS',(400,600),self,2),
                         GameText('Press i button in order to play Stage I',(400,650),self,3),
                         GameText('Or e button to play Stage "E"',(400,700),self,4),
                         VerticalGameText('select one',(120,200),self,5,font_size = 40)
                        ]
        self.buttons = [ MenuArrow('data/images/interface/title_screen/arrow_right/',(400,400),self,0,self.NOTSETYET),
                         MenuArrow('data/images/interface/title_screen/arrow_right/',(160,400),self,0,self.NOTSETYET, invert = True)
                        ]

    def select_princess(self):
        self.princess = MenuPrincess(self)
        self.background = pygame.image.load('data/images/story/svg_bedroom.png').convert()
        self.action     = 'open'
        self.speed      = 0
        self.actual_position = [500,-600]
        self.options    = []

        self.texts =    [GameText('Choose your',(-200,200),self,1,font_size = 40),
                         GameText('appearence...',(-200,250),self,2,font_size = 40),
                         GameText('skin tone',(250,420),self,3,font_size = 40),
                         GameText('previous',(250,-40),self,4,font_size = 40),
                         GameText('next',(250,540),self,5,font_size = 40)]

        D_TITLE_SCREEN = 'data/images/interface/title_screen/'
        self.buttons= [MenuArrow(D_TITLE_SCREEN+'arrow_right/',(360,400), self, 0, self.change_princess,parameter = (1,'skin')),
                       MenuArrow(D_TITLE_SCREEN+'arrow_right/',(100,400), self, 0, self.change_princess,parameter = (-1,'skin'), invert = True),
                       MenuArrow(D_TITLE_SCREEN+'arrow_up/',(200,-130),self,0,self.NOTSETYET),
                       MenuArrow(D_TITLE_SCREEN+'arrow_down/',(200,570),self,0,self.NOTSETYET)]

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


    ### Buttons functions ###
    def change_princess(self,list):#list of: int,part
        self.princess.numbers[list[1]] += list[0]
        if self.princess.numbers[list[1]] < 0:
            self.princess.numbers[list[1]] = 2
        elif self.princess.numbers[list[1]] > 2:
            self.princess.numbers[list[1]] = 0
        print self.princess.numbers[list[1]]
    def NOTSETYET():
        pass

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
    def __init__(self,directory,position,menu,index,function,parameter = None,invert = False,):
        self.position   = position
        self.menu = menu
        self.images     = obj_images.OneSided(directory)
        if invert == True:
            self.images.list = self.invert_images(self.images.list)
        self.image = self.images.list[self.images.number]
        self.index = index
        self.pos        = [self.menu.actual_position[0]+self.position[0],
                           self.menu.actual_position[1]+self.position[1]]
        self.size = self.image.get_size()
        self.rect = Rect(self.pos,self.size)
        self.function = function
        self.parameter = parameter

    def update_all(self):
        self.set_image()
        self.update_pos()
        self.click_detection()
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
    def click_detection(self):
        self.rect = Rect(self.pos,self.size)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.menu.screen.universe.click:
                self.function(self.parameter)


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
        self.image      = self.fontA
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]

class VerticalGameText(GameText):
    def __init__(self,text,pos,menu,index,fonte='Domestic_Manners.ttf',font_size = 20, color = (0,0,0)):
        GameText.__init__(self,text,pos,menu,index,fonte,font_size,color)
        self.fontA = pygame.transform.rotate(self.fontA,90)
        self.fontB = pygame.transform.rotate(self.fontB,90)


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
    def __init__(self,menu):
        dir = 'data/images/princess/'
        self.menu = menu
        self.skin = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in ('skin_pink','skin_tan','skin_black')]
        self.arm  = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in ('arm_pink','arm_tan','arm_black')]
        self.hair = [pygame.image.load(dir+i+'/stay/0.png').convert_alpha() for i in ('hair_rapunzel','hair_yellow','hair_cinderella')]
        self.numbers = {'skin':1,'hair':1}
        self.images = [ self.skin[self.numbers['skin']],
                        pygame.image.load(dir+'face_simple/stay/0.png').convert_alpha(),
                        self.hair[self.numbers['hair']],
                        pygame.image.load(dir+'shoes_slipper/stay/0.png').convert_alpha(),
                        pygame.image.load(dir+'dress_plain/stay/0.png').convert_alpha(),
                        self.arm[self.numbers['skin']]
                        ]
        self.size = self.skin[0].get_size()
        self.position = (250,250)
        self.name = 'Nome'
        self.pos = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]
    def update_all(self):
        self.images[0]  = self.skin[self.numbers['skin']]
        self.images[2]  = self.hair[self.numbers['hair']]
        self.images[5]  = self.arm[self.numbers['skin']]
        self.pos        = [self.menu.actual_position[0]+self.position[0]-(self.size[0]/2),
                           self.menu.actual_position[1]+self.position[1]-(self.size[1]/2)]


