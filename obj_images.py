import globals
import os
import pygame
### TODO Incorporate the variables image_number and size to the obj_images atributes, for their not atributes of the object, but of the images of the object and this will simplify a lot the code.
### TODO include a function update_image, so that it will no longer be necessary to repeat the code in every object.
### TODO include a function reset_image, so that it will be possible to restart the image number easily.

try:
    import Numeric
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError, "Numeric and Surfarray are required."

class TwoSided():
    jeringonca = False
    """This class identify and loads images from a given directory. It also invert the image so that it can be used in a game. It generates two lists of images: self.left and self.right. To use the images you will need to especify the image number between 0 and x, where x is the number of images in the directory.
The object generated has yet other optional atribute, which is: margin.
Margin is the alpha space between the image and the actual drawing. You may specify margin as a list in the following format: [up,left,down,right], i.e, clockwise.
Margin may be used to better program interaction during the game. Margin default to all zero."""
    def __init__(self,dir,margin=[0,0,0,0]):
        self.margin = margin
        self.left = self.find_images(dir)
        self.right = self.invert_images(self.left)
        self.number = 0

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
class OneSided(TwoSided):
    def __init__(self,directory,margin = [0,0,0,0]):
        self.margin = margin
        self.list = self.find_images(directory)
        self.number = 0
        self.size = self.list[self.number].get_size()
class There_and_back_again(TwoSided):
    def __init__(self,dir,margin=[0,0,0,0]):
        self.margin = margin
        preleft = self.find_images(dir)
        preright = self.invert_images(preleft)
        posleft = list(reversed(preleft))
        posright = list(reversed(preright))
        self.left = preleft + posleft
        self.right = preright + posright
