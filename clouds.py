from globals import *

class Cloud():
    def __init__(self, p,level):
        self.pos = p
        self.images = ObjectImages('data/images/scenario/skies/nimbus/'+str(random.randint(0,3))+'/')
        self.image = self.images.left[0]
        self.deep = random.random()/2
        self.image_number = 0
        for i in level:
            i.clouds.insert(self.deep,self)
    def movement(self,dir,act):
        self.pos = (self.pos[0]-10*self.deep,self.pos[1])
        self.set_image
    def set_image(self):
        #choose list
        number_of_files = len(self.images.left)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = self.images.left[self.image_number]

