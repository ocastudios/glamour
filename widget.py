import pygame
import random
import os
import obj_images
from settings import *


class Button():
    def __init__(self,dirtxt,position, level,function,parameter = None,invert = False,fonte='Domestic_Manners.ttf', second_font = 'Chopin_Script.ttf', font_size=40, color=(0,0,0)):
        """Creates a clickable button
        
        dirtxt: if image button than directory, if text button, than text.
        function: a button function is necessary.
        parameter: a string or tuple with the needed parameters for the button function.
        fonte, font_size and color: only useful to image buttons.
        """
        self.level = level
        self.font_size  = int(font_size*scale)
        try:
            os.listdir(dirtxt)
            self.type_of_button = 'image'
        except:
            self.type_of_button = 'text'
        if self.type_of_button == 'image':
            self.images     = obj_images.Buttons(dirtxt,5)
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
        if self.type_of_button == 'text':
            font_size  = int(font_size*scale)
            font       = fonte
            self.text       = dirtxt
            self.color      = color
            self.fontA      = pygame.font.Font(main_dir+'/data/fonts/'+fonte,self.font_size)
            self.fontB      = pygame.font.Font('data/fonts/'+second_font,self.font_size+(self.font_size/2))
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
        self.size       = self.image.get_size()
        try:
            self.pos        = [self.level.actual_position[0]+self.position[0]-(self.size[0]/2),
                               self.level.actual_position[1]+self.position[1]-(self.size[1]/2)]
        except:
            pass
        self.rect       = pygame.Rect(self.pos,self.size)
        self.click_detection()

    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list

    def click_detection(self):
        if  (self.level.game_mouse.type == 1 and self.rect.colliderect(self.level.game_mouse.rect)) or (self.level.game_mouse.type == 2 and self.rect.collidepoint(self.level.mouse_pos)):
            try:
                self.image = self.list_of_images[self.images.itnumber.next()]
            except:
                pass
            if self.type_of_button=="text":
                self.image = self.fontB.render(self.text,1,self.color)
            if self.level.universe.click:
                if self.parameter:
                    if self.parameter.__class__ in (tuple, list):
                        exec("self.function("+str(self.parameter)[1:-1]+")")
                else:
                    self.function()
        else:
            if self.image != self.list_of_images[0]:
                try:
                    self.image = self.images.list[self.images.itnumber.next()]
                except: pass
            if self.type_of_button=="text":
                self.image = self.fontA.render(self.text,1,self.color)



