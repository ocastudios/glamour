import os
import pygame

import settings
from settings import p
from settings import directory
from settings.directory import j


def in_box(font_name, font_size, box, image, message, margin, alignment="center"):
    font_size = p(font_size)
    font = pygame.font.Font(
        j(directory.fonts, font_name), int(round(font_size + (font_size / 2)))
    )
    text_list = message.split()
    number_of_words = len(text_list)
    count = 0
    height = p(margin["top"])
    first = True
    line = ""
    line_break = False
    color = (0, 0, 0, 0)
    while count < number_of_words:
        line += text_list[count]
        line_size = font.size(line)
        line_pos = globals()[alignment](box, margin, line_size)
        if line_size[0] < box[0]:
            if count + 1 < number_of_words:
                temporary_line = line + " " + text_list[count + 1]
                if font.size(temporary_line)[0] >= box[0]:
                    line_image = font.render(line, 1, color)
                    height += int(round(line_size[1] * 0.8))
                    image.blit(font.render(line, 1, color), (line_pos, height))
                    line = ""
                else:
                    line += " "
            elif count + 1 == number_of_words:
                height += int((line_size[1] * 0.8))
                image.blit(font.render(line, 1, color), (line_pos, height))
        else:
            line = text_list[count]
            height += int(
                line_size[1] * 0.8
            )  # If line height is perfect it does not seem that it is the same text
        count += 1
    return image


def center(box, margin, line_size):
    return int(
        round((box[0] + p(margin["left"]) + p(margin["right"]) - line_size[0]) / 2)
    )


def left(box, margin, line_size=None):
    return p(margin["left"])


def right(box, margin, line_size):
    return p(box[0] - margin["right"])
