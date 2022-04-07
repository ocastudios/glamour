import utils
from settings import directory
import pygame
import os


class MousePointer:
    def __init__(self, universe, type=1):
        self.images_small = utils.img.OneSided(
            os.path.join(directory.interface, "mouse-icon", "pointer2")
        )
        self.images_big = utils.img.OneSided(
            os.path.join(directory.interface, "mouse-icon", "pointer")
        )
        self.universe = universe
        self.mouse_pos = pygame.mouse.get_pos()
        if type == 2:
            self.type = 2
            self.images = self.images_small
            self.image = self.images.list[self.images.number]
            self.size = self.image.get_size()
            self.pos = self.mouse_pos
        else:
            self.type = 1
            self.images = self.images_big
            self.image = self.images.list[self.images.number]
            self.size = self.image.get_size()
            self.pos = (
                self.mouse_pos[0] + (self.size[0] / 2),
                self.mouse_pos[1] + (self.size[1] / 2),
            )
        pygame.event.clear()
        self.rect = pygame.Rect(self.pos, self.size)

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        number_of_files = len(self.images.list) - 2
        self.image = self.images.list[self.images.number]
        self.images.update_number()
        if self.type == 1:
            self.pos = (
                self.mouse_pos[0] + (self.size[0] / 2),
                self.mouse_pos[1] + (self.size[1] / 2),
            )
        else:
            self.pos = self.mouse_pos
        self.rect = pygame.Rect(self.pos, self.size)

    def update_all(self):
        pass
