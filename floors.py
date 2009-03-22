
import globals
import obj_images



class Floor():
    images = None

    def __init__(self,index,dir,level,height={'all':186}):
        self.level = level
        if self.images == None:
            self.images = obj_images.OneSided(dir)
        self.image_list = self.images.list
        self.image = self.image_list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = (self.size[0]*(index))
        level.floor_image.insert(index,self)
        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1])
    def update_all(self):
        self.update_pos()
    def update_pos(self):
        self.images.update_number()
        self.image = self.image_list[self.images.number]
        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1])
class Water(Floor):
    height = 70
    nx   = range(70,100)
    tide = nx+list(reversed(nx))
    iterat = iter(tide)
    speed = [3,1]
    direction = 'up'
    def __init__(self,index,dir,level,height={'all':186}):
        self.level = level
        if self.images == None:
            self.images = obj_images.OneSided(dir)
        self.image_list = self.images.list
        self.image = self.image_list[self.images.number]
        self.size = self.image.get_size()
        self.center_distance = 2100+(self.size[0]*index)
        level.floor_image.insert(index,self)
        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.height)
    def update_pos(self):
        self.center_distance += self.speed[0]
        self.images.update_number()
        self.image = self.image_list[self.images.number]
        if self.direction == 'up':
            self.height += self.speed[1]
        else:
            self.height -= self.speed[1]
        if self.height > 100:
            self.direction = 'down'
        if self.height < 90:
            self.direction = 'up'

        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.height)
        if self.pos[0] > 1440:
            self.center_distance -= 1440+(self.size[0]*2)
        if self.pos[0] < -self.size[0]:
            self.center_distance += 1440+(self.size[0]*2)
class Water2(Water):
    height = 63
    direction = 'down'
    speed = [6,1]
    def update_pos(self):
        self.center_distance += self.speed[0]
        self.images.update_number()
        self.image = self.image_list[self.images.number]

        if self.direction == 'up':
            self.height += self.speed[1]
        else:
            self.height -= self.speed[1]
        if self.height > 80:
            self.direction = 'down'
        if self.height < 70:
            self.direction = 'up'

        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.height)
        if self.pos[0] > 1440:
            self.center_distance -= 1440+(self.size[0]*2)
        if self.pos[0] < -self.size[0]:
            self.center_distance += 1440+(self.size[0]*2)

class Bridge():
    def __init__(self,directory,index,level,main=True):
        if main == True:    self.images = obj_images.OneSided(directory+'bridge/')
        else:               self.images = obj_images.OneSided(directory) 

        if main == True:
            self.left_bank = Bridge(str(directory)+'left_bank/',index-1,level,main = False)
            self.right_bank= Bridge(str(directory)+'right_bank/',index+1,level,main = False)

        self.image_number = 0
        self.image = self.images.list[0]
        self.size = self.image.get_size()

        if main == True:    self.center_distance = (400*(index))-400
        else:               self.center_distance = (400*(index))

        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1])
        if main == True:
            del level.floor_image[index]
            level.floor_image.insert(0,self)
        else:
            level.floor_image[index]= self

    def update_pos(self):
        self.image_number += 1
        if self.image_number > len(self.images.list)-1:
            self.image_number = 0
        self.image = self.images.list[self.image_number]
        
        self.pos = (self.level.universe.center_x+(self.center_distance),self.level.universe.floor-self.size[1])
