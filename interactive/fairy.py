import pygame
import utils.obj_images     as obj_images
from pygame.locals import *
import random
from settings import *
import interactive.messages as messages
import interface.widget     as widget 
import os

directory = os.getcwd()+'/data/images/interface/fairy_tips'

def p(positions):
    return [int(i*scale) for i in positions ]

class Fairy():
    """This class defines the tip fairy, who helps the princess during the game."""
    directory = 'data/images/interface/fairy_tips'
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        self.size               = p((10,10))
        self.level              = level
        self.universe           = self.level.universe
        self.center_distance    = pos
        self.pos                =  p([-200,600])
        self.lists_of_images = {
                        'mouth_speak':      obj_images.TwoSided(self.directory+'/fairy_speak/',margin),
                        'mouth_smile':      obj_images.There_and_back_again(self.directory+'/fairy_smile/',margin),

                        'eyes_eyes':        obj_images.There_and_back_again(self.directory+'/fairy_eyes/',margin),
                        'eyes_blink':       obj_images.There_and_back_again(self.directory+'/fairy_blink/',margin),

                        'wings_wings':      obj_images.TwoSided(self.directory+'/fairy_wings/',margin),
                        'wings_fly':        obj_images.TwoSided(self.directory+'/fairy_fly_wings/',margin),

                        'body_fly':         obj_images.There_and_back_again(self.directory+'/fairy_fly/',margin),
                        'body_stand_right': obj_images.There_and_back_again(self.directory+'/fairy_stand_right/',margin),
                        'body_stand_left' : obj_images.There_and_back_again(self.directory+'/fairy_stand_left/',margin)
                    }
#        self.ballon     = obj_images.OneSided(self.directory+'/balloon/',(0,0,0,0))
        self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
        self.parts      = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
        self.size       = self.parts[1].get_size()
        self.image      = pygame.Surface(self.size,SRCALPHA).convert_alpha()
        self.goalpos    = p([1200,700])
        self.direction  = "left"
        self.action     = self.explain
        self.count      = 0
        self.wand       = obj_images.TwoSided(self.directory+'/fairy_wand/',margin)
        self.enchant    = obj_images.TwoSided(self.directory+'/fairy_enchant/',margin)
        self.spark      = obj_images.OneSided(self.directory+'/spark/',margin)
        self.music  = main_dir+'/data/sounds/music/1stSnowfall.ogg'

    def update_all(self):
        for key,value in self.lists_of_images.items():
            value.update_number()
        self.action()
#        if self.count > 300:
#            self.level.fairy = 'done'
#            self.count = 0
#            self.pos = p([-100,600])

    def wait(self):
        pass

    def explain(self):
#        self.count += 1
        self.select_images()
        self.image = self.update_image()
        if self.pos != self.goalpos:
            self.fly_to_goal()
        else:
            if self.pos[0]>(self.universe.width/2):
                self.direction = "left"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
            else:
                self.direction = "right"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']

    def select_images(self):
        if self.direction == "left":
            self.parts = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
        else:
            self.parts = [self.lists_of_images[i].right[self.lists_of_images[i].number] for i in self.images_strings]

    def update_image(self):
        image = pygame.Surface(self.size,SRCALPHA).convert_alpha()
        for i in self.parts:
            if i:
                image.blit(i,(0,0))
        return image

    def fly_to_goal(self):
        speed = int(15*scale)
        self.images_strings = ["wings_fly","body_fly"]
        if self.pos[0] > self.goalpos[0]+5:
            self.direction = "left"
            self.pos[0] -= speed
        elif self.pos[0]<self.goalpos[0]-5:
            self.direction = "right"
            self.pos[0] += speed


class Message():
    def __init__(self, level, message = "Oops! I just forgot what I had to say... One of us should have a conversation with the programmer."):
        self.message    = message
        self.level      = level
        self.universe   = universe = self.level.universe
        self.image      = obj_images.image(directory+'/balloon/0.png')
        self.size       = self.image.get_size()
        self.pos        = ((universe.width - self.size[0])/2, universe.height - self.size[1])
        self.text_box   = self.size[0]*.8,self.size[1]*.8
        self.font_size  = 16*scale
        self.text_font       = pygame.font.Font('data/fonts/FreeSans.ttf',self.font_size+(self.font_size/2))
        self.color      = (0,0,0,0)
        self.image.blit(self.adjusting_fonts(), self.pos)
        self.button     = widget.Button('data/images/interface/title_screen/button_ok/',(1200,800),self.level,self.end_message)
        self.level.fae.append(self.button)


    def update_all(self):
        pass

    def end_message(self):
        self.level.fairy = 'done'
        self.level.fae.remove(self.button)

    def adjusting_fonts(self):
        fix_x       = int(150*scale)
        fix_y       = int(40*scale)
        font_object = self.text_font
        text_box    = self.text_box
        image = self.image
        text_list = self.message.split()
        number_of_words = len(text_list)
        count = 0
        height = fix_y
        first = True
        line = ""
        line_break  = False
#        self.line_image      = font_object.render(self.message,1,self.color)
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
                        image.blit(font_object.render(line, 1, self.color), (line_pos,height))
                        line = ""
                    else:
                        line += ' '
                elif count+1 == number_of_words:
                    height += int((line_size[1]*.8))
                    image.blit(font_object.render(line, 1, self.color), (line_pos,height))
            else:
                line = text_list[count]
                height += int(line_size[1]*.8) #If line height is perfect it does not seem that it is the same text
            count += 1
        return image
