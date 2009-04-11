import globals
import os
import pygame

### TODO include a function update_image, so that it will no longer be necessary to repeat the code in every object.
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
        self.size   = self.left[0].get_size()

    def find_images(self,dir):
        return [pygame.image.load(dir+item).convert_alpha() for item in sorted(os.listdir(dir)) if item[-4:]=='.png']

    def invert_images(self,list):
        return [pygame.transform.flip(img,1,0) for img in list]

    def update_number(self):
        if self.number < len(self.left)-1:
            self.number +=1
        else:
            self.number = 0


class OneSided(TwoSided):
    def __init__(self,directory,margin = [0,0,0,0]):
        self.margin = margin
        self.list = self.find_images(directory)
        self.number = 0
        self.size = self.list[self.number].get_size()
    def update_number(self):
        if self.number < len(self.list)-1:
            self.number +=1
        else:
            self.number = 0
class There_and_back_again(TwoSided):
    def __init__(self,dir,margin=[0,0,0,0]):
        self.margin = margin
        preleft     = self.find_images(dir)
        preright    = self.invert_images(preleft)
        posleft     = list(reversed(preleft))
        posright    = list(reversed(preright))

        self.left   = preleft + posleft
        self.right  = preright + posright
        self.size   = self.left[0].get_size()
