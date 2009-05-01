import princess
import obj_images
from pygame.locals import *

class Glamour_Stars():
    rotating = None
    def __init__(self,distance_center,level,fixed = False):
        self.level = level
        self.fixed = fixed
        if self.rotating == None:
            self.rotating = obj_images.OneSided('data/images/interface/star/')
        self.image = self.rotating.list[0]
        self.center_distance = [distance_center[0],distance_center[1]]
        self.size = self.image.get_size()
        if self.fixed == False:
            self.pos = (self.level.universe.center_x+self.center_distance[0], level.floor-self.size[1]-self.center_distance[1])
        else:
            self.pos = (200,60)
        self.alive = True
        self.rect = Rect(self.pos, self.size)
        self.dir = 'up'
        self.count ={'image':0}

    def move(self,level,princess):
        if self.dir == 'up':
            self.center_distance[1] -= 10
            if self.center_distance[1] < 1:
                self.dir = 'down'
        else:
            self.center_distance[1]+=10
            if self.center_distance[1]> 300:
                self.dir = 'up'
        if self.alive == True:
            if self.rect.colliderect(princess.rect)==True:
                self.alive = False
                princess.glamour_points += 1
                princess.celebrate = 1
        #self.alive = False
        self.pos = (self.level.universe.center_x+self.center_distance[0],level.floor-self.size[1]-self.center_distance[1])
        self.rect = Rect(self.pos, (200,200))
        self.update_images()

    def update_images(self):
        number_of_files = len(self.rotating.list)-2
        if self.count['image'] <= number_of_files:
            self.count['image']+=1
        else:                
            self.count['image']=0        
        self.image = self.rotating.list[self.count['image']]
