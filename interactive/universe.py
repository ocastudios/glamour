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
    def __init__(self, level=None, test=False):
        w = int(round(settings.resolution[0]))
        h = int(round(settings.resolution[1]))
        self.clock = pygame.time.Clock()
        self.milliseconds = 0.0
        self.subtick = 0.0
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
        self.test = test
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
        self.sub_tick = 0

    def update_all(self):
        self.sub_tick == 0 and self.pointer.update()
        self.sub_tick == 0 and self.level.update_all()
        self.level.subtick_update()
        if self.LEVEL == "menu" and self.level.__class__ != menu.Menu:
            self.define_level()
        if self.LEVEL == "game" and self.level.__class__ != stage.Stage:
            self.define_level()
        self.track_time()

    def track_time(self):
        milliseconds = pygame.time.get_ticks()
        self.sub_tick += milliseconds - (self.milliseconds or 0.0)
        if self.sub_tick > 1000 / self.fps:
            self.sub_tick = 0
        self.clock.tick()
        self.milliseconds = milliseconds

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
