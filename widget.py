import pygame
import random
import os
import obj_images
from settings import *


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



