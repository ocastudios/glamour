import pygame
class Universe():
    def __init__(self,w,h):
        self.gravity = 3
        self.center_x = -3400
        self.center_y = 0
        self.floor = self.height = h
        self.width = w
        self.speed = 0
    def movement(self,dir):
        max_speed = 10
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed< -max_speed:
            self.speed = -max_speed
        self.center_x += self.speed
        if self.center_x > 0:
            self.speed = 0
            self.center_x = 0
        if self.center_x < -5430:
            self.speed = 0
            self.center_x = -5430
#        self.center_x += self.speed
