
from globals import *


### Sky is not working. Got to fix this. This code may be of help:
#Each image gets a fainter alpha. Then in your particle
#loop, you pick one of the pregenerated images.
#particleImages = []
#for i in range(16):
#    newImage = originalImage.convert_alpha()
#    factor = 1.0 - (i / 16.0)
#    factor = Numeric.array(factor * 255, Numeric.UInt8)
#    pygame.surfarray.pixels_alpha(newImage)[:]
#    particleImages.append(newImage)
#    int(round(particle.decay / particle.life))
#Then in your rendering loop...
#for particle in particleEmitter.particles:
#    frame = int(particle.decay / particle.life * 15.0)
#    image = particleImages[frame]
#    pos = image.get_rect(center=(particle.x, particle.y)
#    self.fieldSurface.blit(image, pos)


night_back = pygame.image.load('data/images/scenario/skies/night_back/night_back.png').convert_alpha()
night_front = pygame.image.load('data/images/scenario/skies/night_front/night_front.png').convert_alpha()

class Sky():
    def __init__(self, background,level,clock_pointer):
        directory = 'data/images/scenario/skies/'
        self.background = pygame.image.load(background).convert()
        self.count = 0
        self.count = (clock_pointer.count-120)
        self.night_back = ObjectImages_OneSided(directory+'night_back/')
        self.night_front = ObjectImages_OneSided(directory+'night_front/')
        
        count = 1
        for i in range(25):
            back = self.get_transparent(self.night_back.list[0], 10*count)
            self.night_back.list.append(back)
            front = self.get_transparent(self.night_front.list[0], 10*count)
            self.night_front.list.append(front)
            count += 5
        self.image_number = 0
        self.night_back_image = self.night_back.list[self.image_number]
        self.night_front_image = self.night_front.list[self.image_number]
        self.max_image_number = len(self.night_back.list)-1
        for i in level:
            i.sky.insert(0,self)
    def set_light(self,clock_pointer):
        if clock_pointer.time == ('morning' or 'day'):
            self.back_image = self.night_back.list[0]
            self.front_image = self.night_front.list[0]
        else:
            self.image_number += 1
            if self.image_number >self.max_image_number:
                self.image_number = 0
            self.back_image = self.night_back.list[self.image_number]
            self.front_image = self.night_front.list[self.image_number]

    def get_transparent(self,image,factor):
        new_image = image
        alpha = pygame.surfarray.pixels_alpha(new_image)
        pygame.surfarray.pixels_alpha(new_image)[...] = uint8(alpha + factor)
        del alpha
        return new_image
            
#class Night():
#    def __init__(self,level,directory):
#        self.back_images = ObjectImages_OneSided(directory+'back')
#        self.front_images = ObjectImages_OneSided(directory+'front')

#        self.image_number = 0
#        self.back_image = self.back_images[self.image_number]
#        self.front_image = self.front_images[self.image_number]
#        for l in level:
#            level.night.append(self)
#    def update_image(self):
#        self.image_number += 1
#        if self.image_number > len(self.back_images):
#            self.image_number = 0
#        self.back_image = self.back_images[self.image_number]
#        self.front_image = self.font_images[self.image_number]
