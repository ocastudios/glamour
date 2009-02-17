from pygame import *
import pygame

def jump(self,height):
    if self.pos[1]+self.size[1] >= universe.floor:
        touching_floor = True
    else:
        touching_floor = False
        
    try:
        if pressed == False:
            for event in pygame.event.get():            
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.jump < 30:
                        self.pos = (self.pos[0],self.pos[1]-height)
                        self.jump +=1
                        pressed = True
    except:
        pressed = False
    
    
    if event.type == KEYUP:
        if event.key == K_SPACE:
            pressed = False
            self.jump = 0
            



        if princess.doonce == False:
            if act[0]!= 'jump':
                self.jump = 0
            if self.pos[1]+self.size[1] == universe.floor and self.jump == 0:
                if act[0]== 'jump':
                    self.jump = 1





        if self.jump > 0 and self.jump <20:
            self.pos = (self.pos[0],self.pos[1]-15)
            self.jump +=1
            for part in self.parts:
                part.update_image(once = True, reset = True)