import os
import pygame
from pygame.locals import *

class ObjectImages():
    """This class identify and loads images from a given directory. It also invert the image so that it can be used in a game. It generates two lists of images: self.left and self.right. To use the images you will need to especify the image number between 0 and x, where x is the number of images in the directory.
The object generated has yet other optional atribute, which is: margin.
Margin is the alpha space between the image and the actual drawing. You may specify margin as a list in the following format: [up,left,down,right], i.e, clockwise.
Margin may be used to better program interaction during the game. Margin default to all zero."""
    def __init__(self,dir,margin=[0,0,0,0]):
        self.margin = margin
        self.left = self.find_images(dir)
        self.right = self.invert_images(self.left)        
    def find_images(self,dir):
        list_of_images = []
        images = []
        for item in os.listdir(dir):
            list_of_images.append(item)
        list_of_images.sort()
        for item in list_of_images:
            try:
                img = pygame.image.load(dir+item).convert_alpha()    
                images.append(img)
            except:
                list_of_images.remove(item)
                print 'couldnt load image in:'+str(dir)+str(item)
        return images    
    def invert_images(self,list):
        inv_list=[]
        for img in list:
            inv = pygame.transform.flip(img,1,0)
            inv_list.append(inv)
        return inv_list
class ObjectImages_OneSided(ObjectImages):
    def __init__(self,directory,margin = [0,0,0,0]):
        self.margin = margin
        self.list = self.find_images(directory)
