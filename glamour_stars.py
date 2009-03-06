from globals import *
from princess import *
from screen_surface import *


class Glamour_Stars():
    rotating = None
    def __init__(self,distance_center,fixed = False):
        self.fixed = fixed
        if self.rotating == None:
            self.rotating = obj_images.OneSided('data/images/interface/star/')
        self.image = self.rotating.list[0]
        self.distance_from_center = [distance_center[0],distance_center[1]]
        self.size = self.image.get_size()
        if self.fixed == False:
            self.pos = (universe.center_x+self.distance_from_center[0], Level_01.floor-self.size[1]-self.distance_from_center[1])
        else:
            self.pos = (200,60)
        self.alive = True
        self.rect = Rect(self.pos, self.size)
        self.dir = 'up'
        stars.append(self)
        Level_01.pointer.append(self)
        self.count ={'image':0}
    def move(self):
        if self.dir == 'up':
            self.distance_from_center[1]-= 10
            if self.distance_from_center[1] < 1:
                self.dir = 'down'
        else:
            self.distance_from_center[1]+=10
            if self.distance_from_center[1]> 300:
                self.dir = 'up'
        if self.alive == True:
            if self.rect.colliderect(princess.rect)==True:
                self.alive = False
                princess.glamour_points += 1
                princess.celebrate = 1
        #self.alive = False
        self.pos = (universe.center_x+self.distance_from_center[0], Level_01.floor-self.size[1]-self.distance_from_center[1])
        self.rect = Rect(self.pos, (200,200))
        self.update_images()



    def update_images(self):
        number_of_files = len(self.rotating.list)-2
                
        if self.count['image'] <= number_of_files:
            self.count['image']+=1
        else:                
            self.count['image']=0        
        self.image = self.rotating.list[self.count['image']]
