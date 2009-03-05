from globals import *

class Cloud():
    def __init__(self, p,level):
        self.pos = p
        nimbus = []
        try:
            if nimbus1 != False and nimbus2 != False and nimbus3 != False:
                pass
        except: 
            nimbus1 = ObjectImages_OneSided('data/images/scenario/skies/nimbus/1/')
            nimbus2 = ObjectImages_OneSided('data/images/scenario/skies/nimbus/2/')
            nimbus3 = ObjectImages_OneSided('data/images/scenario/skies/nimbus/3/')
            nimbus.append(nimbus1)
            nimbus.append(nimbus2)
            nimbus.append(nimbus3)
        self.images = nimbus[random.randint(0,2)]
        self.image = self.images.list[0]
        self.deep = random.random()/2
        self.image_number = 0
        for i in level:
            i.clouds.insert(self.deep,self)
    def movement(self,dir,act):
        self.pos = (self.pos[0]-10*self.deep,self.pos[1])
        self.set_image
    def set_image(self):
        #choose list
        number_of_files = len(self.images.list)-2
        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0
        self.image = self.images.list[self.image_number]

