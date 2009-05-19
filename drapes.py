import obj_images

class Drape():
    images = None
    def __init__(self,index,side):
        if side == 'right':
            self.side = ('right','left')
        else:
            self.side = ('left','right')
        self.images = self.images or obj_images.TwoSided('data/images/interface/omni/drapes/drapes/')
        self.action = 'stay'
        self.speed = 0
        self.image_number = 0
        self.image = self.images.left[self.image_number]
        self.size = self.image.get_size()
        self.position = ((index*116)-3,0)
    def update_all(self):
        self.update_pos()
    def update_pos(self):
        if self.side[0]== 'left':
            order = ('open','close')
        else:
            order = ('close','open')
        if self.action == order[0]:
            if self.speed < 30:
                self.speed += 2
        elif self.action == order[1]:
            if self.speed > -30:
                self.speed -= 2
        else:
            self.speed = 0
        self.position = (self.position[0]+self.speed,0)
        if self.speed != 0:
            exec('self.image = self.images.'+self.side[0]+'[self.image_number]')
            if self.image_number < len(self.images.left)-1:
                if self.speed >= 0:
                    self.image_number = int(self.speed*.2)
                else:
                    self.image_number = -int(self.speed*.2)
            else:
                self.image_number = len(self.images.left)-1
class UperDrape():
    def __init__(self,index):
        self.images = obj_images.OneSided('data/images/interface/omni/drapes/upper_drapes/')
        self.image  = self.images.list[self.images.number]
        self.position = ((index*110),0)
        self.action = 'stay'
        self.size = self.image.get_size()
    def update_all(self):
        self.image  = self.images.list[self.images.number]
        if self.action == 'open':
            self.position = (self.position[0],self.position[1]-3)
        if self.position[1] < -self.size[1]:
            self.position = (self.position[0],-self.size[1])
