import obj_images


class Drapes():
    images = None
    def __init__(self):
        self.images or self.images =  obj_images.There_and_back_again('data/images/interface/omni/drapes/')
        self.position = range(0,1440,12)
        self.pos_y = range(12)
        for i in self.pos_y:
            i = 0
        self.position = zip(self.pos,self.pos_y)
    def update_all(self):
        self.images.update_number()
    def close(self):
        for c in range(12):
            for i in self.position[1]:
                i += 1
            for i in self.position[2]:
                i -= 1
