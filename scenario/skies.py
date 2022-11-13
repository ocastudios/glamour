import utils
import pygame
import os
from pygame.locals import *
from settings import directory
from settings import *


class Sky:
    night_images = utils.img.OneSided(os.path.join(directory.skies, "night2"))

    def __init__(self, universe):
        self.universe = universe
        self.image = utils.img.image(
            os.path.join(directory.skies, "daytime", "daytime.png")
        )
        self.pos = (0, 0)
        self.night_image = None
        self.prev = None

    def render(self):
        if self.universe.level.clock[1].time in ("evening", "night", "ball"):
            self.night_image = self.night_images.list[self.night_images.number]
            if (
                self.universe.level.clock[1].count % 2 == 0
                and self.universe.level.clock[1].count != self.prev
            ):
                self.night_images.til_the_end()
                self.prev = self.universe.level.clock[1].count
        else:
            self.night_image = None
            self.night_images.number = 0
