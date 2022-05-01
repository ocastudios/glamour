# -*- coding: utf-8 -*-
import pygame
import os
import interface.menu as menu
import interface.mousepointer as mousepointer
import settings
import utils
from settings import directory
import interactive.stage as stage


class Universe:
    def __init__(self, level=None):
        w = int(round(settings.resolution[0]))
        h = int(round(settings.resolution[1]))
        self.clock = pygame.time.Clock()
        self.center_x = int(-3400 * settings.scale)
        self.center_y = 0
        self.floor = self.height = h
        self.width = w
        self.speed = 0
        self.LEVEL = "menu"
        self.action = [None, "stay", "open"]
        self.dir = "right"
        self.click = False
        self.file = None
        self.fps = 40  # fps is altered by stage and menu in their initialization
        self.run_level = True
        self.db = None
        self.db_cursor = None
        try:
            del self.screen_surface
        except AttributeError:
            pass
        if settings.active_full:
            self.screen_surface = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        else:
            self.screen_surface = pygame.display.set_mode((w, h))
        self.screen_surface.blit(
            utils.img.image(os.path.join(directory.drapes, "drape000.png")), (0, 0)
        )
        self.screen_surface.blit(
            utils.img.image(os.path.join(directory.upper_drapes, "upper.png")), (0, 0)
        )
        pygame.display.flip()
        ## Interface ##
        self.stage = None
        if not level:
            self.menu = menu.Menu(self)
            self.level = self.menu
            self.level.main()
        else:
            self.menu = level
            self.level = level
        self.pointer = mousepointer.MousePointer(self, type=2)

    def update_all(self):
        self.pointer.update()
        self.level.update_all()
        if self.LEVEL == "menu" and self.level.__class__ != menu.Menu:
            self.define_level()
        if self.LEVEL == "game":
            if self.level.__class__ != stage.Stage:
                self.define_level()

    def define_level(self):
        if self.LEVEL == "game":
            if not self.level or self.level.__class__ != stage.Stage:
                self.fps = 20
                self.action = [None, "stay", None]
                self.pointer.images = self.pointer.images_big
                self.stage = self.stage or stage.Stage(self)
                self.level = self.stage
                self.level.paused = False
                self.stage.BathhouseSt(goalpos=round(5220 * settings.scale))

        elif self.LEVEL == "menu":
            if not self.level or self.level.__class__ != menu.Menu:
                self.fps = 40
                self.action = ["open", "stay", "open"]
                self.pointer.images = self.pointer.images_small
                self.level = self.menu
                self.level.vertical_bar["side"] = "left"
                self.level.main()

    def movement(self, dir):
        max_speed = round(14 * settings.scale)
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed < -max_speed:
            self.speed = -max_speed
        self.center_x += self.speed
        if self.center_x > 0:
            self.speed = 0
            self.center_x = 0
        if self.center_x - self.width < -(self.level.size):
            self.speed = 0
            self.center_x = -(self.level.size) + self.width
