# -*- coding: utf-8 -*-
import pygame
import random
import interface.random_names as random_names
import os
import utils.obj_images as obj_images
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
            self.list_of_images = self.images.list
        if self.type_of_button == 'text':
            font_size  = int(font_size*scale)
            font       = fonte
            self.text       = dirtxt
            self.color      = color
            self.fontA      = pygame.font.Font(main_dir+'/data/fonts/'+fonte,self.font_size)
            self.fontB      = pygame.font.Font('data/fonts/'+second_font,self.font_size+(self.font_size/3))
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
            self.pos        = [self.level.position[0]+self.position[0]-(self.size[0]/2),
                               self.level.position[1]+self.position[1]-(self.size[1]/2)]
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


class GameText():
    def __init__(self,text,pos,frame,fonte='Domestic_Manners.ttf', font_size=40, color=(83,0,0),second_font = 'Chopin_Script.ttf',var = False, rotate = None, box = None):
        font_size  = int(font_size*scale)
        self.font       = fonte
        self.frame      = frame
        try:
            self.frame_pos = self.frame.position
        except:
            self.frame_pos = 0,0
        self.text       = text
        self.color      = color
        self.fontA      = pygame.font.Font(main_dir+'/data/fonts/'+fonte,font_size)
        self.fontB      = pygame.font.Font(main_dir+'/data/fonts/'+second_font,font_size+(font_size/3))
        self.position   = pos
        if box:
            self.box    = pygame.Surface(p(box), pygame.SRCALPHA).convert_alpha()
            self.adjusting_fonts()
            self.image  = self.box
            self.size       = self.image.get_size()
            self.pos        = [self.position[0]-(self.size[0]/2),
                               self.position[1]-(self.size[1]/2)]


        else:
            self.image      = self.fontA.render(self.text,1,self.color)
            if rotate:
                try:
                    self.image = pygame.transform.rotate(self.image,rotate)
                except:
                    print "the rotate parameter must be a number"
            self.size       = self.image.get_size()
            self.pos        = [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
                               self.frame_pos[1]+self.position[1]-(self.size[1]/2)]


        self.variable_text = var
        self.text_box   = self.size[0]*.8,self.size[1]*.8

    def update_all(self):
        try:
            self.frame_pos = self.frame.position
        except:
            pass
        self.pos        = [self.frame_pos[0]+self.position[0]-(self.size[0]/2),
                           self.frame_pos[1]+self.position[1]-(self.size[1]/2)]
        if self.variable_text:
            self.image = self.fontA.render(self.text,1,self.color)

    def adjusting_fonts(self):
#        print "Adjusting text: "+u(str(self.text))
        fix_x       = int(0*scale)
        fix_y       = int(0*scale)
        font_object = self.fontA
        box = self.box
        text_box    = self.box.get_size()
        text_list = self.text.split()
        number_of_words = len(text_list)
        count = 0
        height = fix_y
        first = True
        line = ""
        line_break  = False
        while count < number_of_words:
            line        += text_list[count]
            line_size   = font_object.size(line)
            line_pos = int((text_box[0]+fix_x-line_size[0])/2)
            if line_size[0] < text_box[0]:
                if count+1 < number_of_words:
                    temporary_line = line + ' '+ text_list[count+1]
                    if font_object.size(temporary_line)[0] >= text_box[0]:
                        line_image = font_object.render(line,1, self.color)
                        height += int((line_size[1]*.8))
                        box.blit(line_image, (line_pos,height))
                        line = ""
                    else:
                        line += ' '
                elif count+1 == number_of_words:
                    height += int((line_size[1]*.8))
                    box.blit(font_object.render(line, 1, self.color), (line_pos,height))
            else:
                line = text_list[count]
                height += int(line_size[1]*.8) #If line height is perfect it does not seem that it is the same text
            count += 1



class Letter(GameText):
    hoover = False
    def __init__(self,text,pos,frame,hoover_size,fonte='Domestic_Manners.ttf',font_size=20, color=(83,0,0)):
        font_size = int(font_size*scale)
        GameText.__init__(self,text,pos,frame,fonte,font_size,color)
        self.hoover_size = hoover_size
        self.size = p((30,30))
        
        self.rect = (self.pos,self.size)

    def update_all(self):
        self.size       = self.image.get_size()
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = pygame.Rect(self.pos,self.size)
        self.type       = type
        self.click_detection()

    def click_detection(self):
        if -.5< self.frame.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hoover = True
####################################### BUTTON ACTION ########################################
                if self.frame.screen.universe.click:
                    self.frame.princess.name.text += self.text
            else:
                self.hoover = False


class Key(GameText):
    hoover = False
    def __init__(self,text,pos,frame,key_type):
        GameText.__init__(self,text,pos,frame,fonte='GentesqueRegular.otf',font_size=30, color=(83,0,0))
        self.key = key_type


    def update_all(self):
        self.size       = self.image.get_size()
        self.pos        = [self.frame.position[0]+self.position[0]-(self.size[0]/2),
                           self.frame.position[1]+self.position[1]-(self.size[1]/2)]
        self.rect       = pygame.Rect(self.pos,self.size)
        self.click_detection()

    def click_detection(self):
        if -.5< self.frame.speed < .5:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.hoover = True
                if self.frame.screen.universe.click:
                    if   self.key == 'Spacebar':
                        self.frame.princess.name.text += ' '
                    elif self.key == 'Backspace':
                        self.frame.princess.name.text = self.frame.princess.name.text[:-1]
                    elif self.key == 'Cleanup':
                        self.frame.princess.name.text = ""
                    elif self.key == 'Random':
                        self.frame.princess.name.text = random.choice(random_names.names)
            else:
                self.hoover = False



