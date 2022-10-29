import os
import pygame
from settings import directory

pygame.display.init()
pygame.display.set_caption("Glamour - OcaStudios")

os.environ["SDL_VIDEO_CENTERED"] = "1"


def splash():
    """ Displays the splash screen """
    introdir = os.path.join(directory.data, "images", "intro", "quanti")
    splash = [
        pygame.image.load(os.path.join(introdir, i)).convert(32)
        for i in sorted(os.listdir(introdir))
    ]
    splash_size = splash[0].get_size()
    splash_surface = pygame.display.set_mode(splash_size)  # , pygame.NOFRAME)
    pygame.display.set_icon(
        pygame.image.load(
            os.path.join(directory.interface, "favicon.png")
        ).convert_alpha()
    )
    tempclock = pygame.time.Clock()
    for i in splash:
        splash_surface.blit(i, (0, 0))
        pygame.display.flip()
        tempclock.tick(40)
