import obj_images


class Drapes():
    images = None
    def __init__(self,index):
        self.images or self.images =  obj_images.There_and_back_again('data/images/interface/omni/drapes/')
        self.position = (index*12,0)
        self.action = 'stay'
        self.speed = 0
    def update_all(self):
        self.images.update_number()
        self.update_pos()
    def update_pos(self):
        self.position = sel.position(self.position+self.speed,0)
        if self.action == 'open':
            self.speed += 1
        elif self.action == 'close':
            self.speed -= 1
        else:
            self.speed = 0

