import os
import pygame
from settings import directory


def set_icon():
    pygame.display.set_icon(
        pygame.image.load(
            os.path.join(directory.interface, "favicon.png")
        ).convert_alpha()
    )
