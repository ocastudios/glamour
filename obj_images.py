import os
import operator
import pygame
from itertools import *
from settings import *

### TODO include a function reset_image, so that it will be possible to restart the image number easily.

class TwoSided():
    jeringonca = False
    """This class identify and loads images from a given directory. It also invert the image so that it can be used in a game. It generates two lists of images: self.left and self.right. To use the images you will need to especify the image number between 0 and x, where x is the number of images in the directory.
The object generated has yet other optional atribute, which is: margin.
Margin is the alpha space between the image and the actual drawing. You may specify margin as a list in the following format: [up,left,down,right], i.e, clockwise.
Margin may be used to better program interaction during the game. Margin default to all zero."""
    def __init__(self,dir,margin=[0,0,0,0]):
        self.margin = margin
        self.left   = self.find_images(dir)
        self.right  = self.invert_images(self.left)
        self.number = 0
        self.lenght = len(self.left)
        if self.lenght>0:
            self.size   = self.left[0].get_size()
        self.itnumber = cycle(range(self.lenght))

    def find_images(self,dir):
        return [pygame.transform.smoothscale(i,(int(i.get_size()[0]*scale),int(i.get_size()[1]*scale))) for i in [pygame.image.load(dir+item).convert_alpha() for item in sorted(os.listdir(dir)) if ( item[-4:] == '.png' or item[-4:]== '.PNG')]]

    def invert_images(self,imglist):
        return [pygame.transform.flip(img,1,0) for img in imglist]

    def update_number(self):
        if self.number < self.lenght -1:
            self.number = operator.add(self.number,1)
        else:
            self.number = 0

    def til_the_end(self):
        if self.number < self.lenght -1:
            self.number = operator.add(self.number,1)
        else:
            self.number = self.lenght -1

class OneSided(TwoSided):
    def __init__(self,directory,margin = [0,0,0,0]):
        self.margin     = margin
        self.list       = self.left = self.find_images(directory)
        self.number     = 0
        self.size       = self.list[self.number].get_size()
        self.lenght     = len(self.list)
        self.itnumber   = cycle(range(self.lenght))


class There_and_back_again(TwoSided):
    def __init__(self,dir,margin=[0,0,0,0], exclude_border = False, second_dir = False, extra_part = False, second_extra_part = False):
        self.margin = margin
        preleft     = self.find_images(dir)

        if extra_part:
            extra = self.find_images(extra_part)
            for i,e in zip(preleft,extra):
                i.blit(e,(0,0))

        preright    = self.invert_images(preleft)
        posleft     = list(reversed(preleft))
        posright    = list(reversed(preright))

        if exclude_border:
            posleft     = posleft[1:-1]
            posright    = posright[1:-1]
        self.left   = self.list =   preleft + posleft
        self.right  =               preright + posright
        if second_dir:
            second_left = self.find_images(second_dir)
            if extra_part:
                second_extra = self.find_images(second_extra_part)
                for i,e in zip(second_left,second_extra):
                    i.blit(e,(0,0))

            second_right = self.invert_images(second_left)
            possecond_left = list(reversed(second_left))
            possecond_right= list(reversed(second_right))

            if exclude_border:
                possecond_left = possecond_left[1:-1]
                possecond_right = possecond_right[1:-1]

            self.left = self.list = self.left+ second_left+possecond_left
            self.right= self.right + second_right + possecond_right

        self.size   = self.left[0].get_size()
        self.lenght = len(self.left)
        self.number = 0
        self.itnumber = cycle(range(self.lenght))


class GrowingUngrowing(TwoSided):
    def __init__(self,directory,frames,margin=[0,0,0,0]):
        self.margin = margin
        self.list = self.left = self.find_images(directory)
        n_list = []
        for i in self.list:
            n_list.extend([pygame.transform.smoothscale(i,(i.get_width(),i.get_height()-(2*x))) for x in xrange(frames)])
        self.list.extend(n_list)
        self.list.extend(reversed(n_list))
        self.lenght = len(self.list)
        self.number = 0
        self.size = self.list[self.number].get_size()
        self.itnumber = cycle(range(self.lenght))


class Buttons(TwoSided):
    def __init__(self,directory,frames):
        self.list = self.left = self.find_images(directory)
        n_list = []
        for i in self.list:
            n_list.extend([pygame.transform.smoothscale(i,(i.get_width()+(2*x),i.get_height()+(2*x))) for x in xrange(frames)])
        self.list.extend(n_list)
        self.list.extend(reversed(n_list))
        self.lenght = len(self.list)
        self.number = 0
        self.size = self.list[self.number].get_size()
        self.itnumber = cycle(range(self.lenght))


class MultiPart():
    def __init__(self,ordered_directory_list,margin = [0,0,0,0]):
        def gcd(a, b):
          if b: return gcd(b, a % b)
          return a
        def least_common_multiple(nums): return reduce(lambda a, b: a * b / gcd(a, b), nums)

        def find_images(dir):
            return [pygame.transform.smoothscale(i,(int(i.get_size()[0]*scale),int(i.get_size()[1]*scale) )) for i in [pygame.image.load(dir+item).convert_alpha() for item in sorted(os.listdir(dir)) if ( item[-4:] == '.png' or item[-4:]== '.PNG')]]
        def invert_images(list):
            return [pygame.transform.flip(img,1,0) for img in list]


        ######### Building images ##########
        all_images = [find_images(dir) for dir in ordered_directory_list]
        image_size = all_images[0][0].get_size()
        lists_lenghts = [len(i) for i in all_images]
        lcm = least_common_multiple(lists_lenghts)
        all_images = [i*(lcm/len(i)) for i in all_images]
        self.images = [pygame.Surface(image_size, pygame.SRCALPHA).convert_alpha() for i in range(lcm)]
        for i in range(lcm):
            [self.images[i].blit(img_list[i],(0,0)) for img_list in all_images]


        self.margin = margin
        self.left   = self.images
        self.right  = invert_images(self.left)
        self.number = 0
        self.lenght = len(self.left)
        if self.lenght>0:
            self.size   = self.left[0].get_size()
        self.itnumber = cycle(range(self.lenght))


    def update_number(self):
        if self.number < self.lenght -1:
            self.number += 1
        else:
            self.number = 0

def image(directory):
    prep = pygame.image.load(directory).convert_alpha()
    return pygame.transform.smoothscale(prep,(int(prep.get_width()*scale),int(prep.get_height()*scale)))
def scale_image(prep):
    return pygame.transform.smoothscale(prep,(int(prep.get_width()*scale),int(prep.get_height()*scale)))
