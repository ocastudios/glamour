import os
import pygame
import re
import itertools
import settings
from settings import p
from settings import directory
from functools import reduce

### TODO include a function reset_image, so that it will be possible to restart the image number easily.


class TwoSided:
    """This class identify and loads images from a given directory. It also invert the image so that it can be used in a game. It generates two lists of images: self.left and self.right. To use the images you will need to especify the image number between 0 and x, where x is the number of images in the directory.
    The object generated has yet other optional atribute, which is: margin.
    Margin is the alpha space between the image and the actual drawing. You may specify margin as a list in the following format: [up,left,down,right], i.e, clockwise.
    Margin may be used to better program interaction during the game. Margin default to all zero."""

    def __init__(self, d, margin=[0, 0, 0, 0]):
        self.margin = margin
        self.left = find_images(d)
        self.right = invert_images(self.left)
        self.number = 0
        self.lenght = len(self.left)
        if self.lenght > 0:
            self.size = self.left[0].get_size()
        self.itnumber = itertools.cycle(list(range(self.lenght)))

    def update_number(self, backwards=False):
        if not backwards:
            if self.number < self.lenght - 1:
                self.number += 1
            else:
                self.number = 0
        else:
            if self.number > 0:
                self.number -= 1
            else:
                self.number = self.lenght - 1

    def til_the_end(self):
        if self.number < self.lenght - 1:
            self.number += 1
        else:
            self.number = self.lenght - 1


class OneSided(TwoSided):
    def __init__(self, d, margin=[0, 0, 0, 0]):
        self.margin = margin
        self.list = self.left = find_images(d)
        self.number = 0
        self.size = self.list[0].get_size()
        self.lenght = len(self.list)
        self.itnumber = itertools.cycle(list(range(self.lenght)))


class There_and_back_again(TwoSided):
    def __init__(
        self,
        d,
        margin=[0, 0, 0, 0],
        exclude_border=False,
        second_dir=False,
        extra_part=False,
        second_extra_part=False,
    ):
        self.margin = margin
        preleft = find_images(d)
        if extra_part:
            extra = find_images(extra_part)
            for i, e in zip(preleft, extra):
                i.blit(e, (0, 0))
        posleft = list(reversed(preleft))
        if exclude_border:
            posleft = posleft[1:-1]
        self.left = self.list = preleft + posleft
        if second_dir:
            second_left = find_images(second_dir)
            if extra_part:
                second_extra = find_images(second_extra_part)
                for i, e in zip(second_left, second_extra):
                    i.blit(e, (0, 0))
            second_right = invert_images(second_left)
            possecond_left = list(reversed(second_left))
            if exclude_border:
                possecond_left = possecond_left[1:-1]
            self.left = self.list = self.left + second_left + possecond_left
        self.right = invert_images(self.left)
        self.size = self.left[0].get_size()
        self.lenght = len(self.left)
        self.number = 0
        self.itnumber = itertools.cycle(list(range(self.lenght)))


class GrowingUngrowing(TwoSided):
    def __init__(self, d, frames, margin=[0, 0, 0, 0]):
        self.margin = margin
        self.list = self.left = find_images(d)
        n_list = [
            pygame.transform.smoothscale(i, (i.get_width(), i.get_height() - (2 * x)))
            for x in range(frames)
            for i in self.list
        ]
        self.list.extend(n_list)
        self.list.extend(reversed(n_list))
        del n_list
        self.lenght = len(self.list)
        self.number = 0
        self.size = self.list[self.number].get_size()
        self.itnumber = itertools.cycle(list(range(self.lenght)))


class Buttons(GrowingUngrowing):
    def __init__(self, d, frames):
        self.list = self.left = find_images(d)
        n_list = [
            pygame.transform.smoothscale(
                i, (i.get_width() + (2 * x), i.get_height() + (2 * x))
            )
            for x in range(frames)
            for i in self.list
        ]
        self.list.extend(n_list)
        self.list.extend(reversed(n_list))
        del n_list
        self.lenght = len(self.list)
        self.number = 0
        self.size = self.list[self.number].get_size()
        self.itnumber = itertools.cycle(list(range(self.lenght)))


class MultiPart:
    def __init__(
        self, ordered_directory_list, margin=[0, 0, 0, 0], loading=None, onesided=False
    ):
        def gcd(a, b):
            if b:
                return gcd(b, a % b)
            return a

        def least_common_multiple(nums):
            return reduce(lambda a, b: int(a * b / gcd(a, b)), nums)

        def count_png(d):
            count = 0
            for i in os.listdir(d):
                if i[-4:] == ".png" or i[-4:] == ".PNG":
                    count += 1
            return count

        lists_lenghts = [count_png(i) for i in ordered_directory_list]
        lcm = least_common_multiple(lists_lenghts)

        base_images = find_images(ordered_directory_list[0])
        base_images = base_images * int(lcm / count_png(ordered_directory_list[0]))
        image_size = base_images[0].get_size()
        self.images = [
            pygame.Surface(image_size, pygame.SRCALPHA).convert_alpha()
            for i in range(lcm)
        ]
        for i in range(lcm):
            self.images[i].blit(base_images[i], (0, 0))
        if loading:
            loading()

        for img_list in ordered_directory_list[1:]:
            images = find_images(img_list)
            images = images * int(lcm / count_png(img_list))
            for i in range(lcm):
                self.images[i].blit(images[i], (0, 0))
            if loading:
                loading()

        self.margin = margin
        self.left = self.images
        if loading:
            loading()
        if not onesided:
            self.right = invert_images(self.left)
        else:
            self.right = None
        if loading:
            loading()
        self.number = 0
        self.lenght = len(self.left)
        if self.lenght > 0:
            self.size = self.left[0].get_size()
        self.itnumber = itertools.cycle(list(range(self.lenght)))
        if loading:
            loading()

    def update_number(self, backwards=False):
        if not backwards:
            if self.number < self.lenght - 1:
                self.number += 1
            else:
                self.number = 0
        else:
            if self.number > 0:
                self.number -= 1
            else:
                self.number = self.lenght - 1


class Ad_hoc:
    def __init__(self, left_images, right_images, margin=[0, 0, 0, 0]):
        self.margin = margin
        self.left = left_images
        self.right = right_images
        self.number = 0
        self.lenght = len(self.left)
        if self.lenght > 0:
            self.size = self.left[0].get_size()
        self.itnumber = itertools.cycle(list(range(self.lenght)))

    def update_number(self, backwards=False):
        if not backwards:
            if self.number < self.lenght - 1:
                self.number += 1
            else:
                self.number = 0
        else:
            if self.number > 0:
                self.number -= 1
            else:
                self.number = self.lenght - 1

    def til_the_end(self):
        if self.number < self.lenght - 1:
            self.number += 1
        else:
            self.number = self.lenght - 1


def image(path, invert=False, alpha=True):
    if not re.search(directory.main, path) \
            and not re.search(directory.homedir, path):
        path = os.path.join(directory.main, path)
    if alpha:
        prep = pygame.image.load(path).convert_alpha()
    else:
        prep = pygame.image.load(path).convert()
    if invert is True:
        prep = pygame.transform.flip(prep, 1, 0)
    prep_size = prep.get_size()
    size = (
        int(round(prep_size[0] * settings.scale)),
        int(round(prep_size[1] * settings.scale)),
    )
    return pygame.transform.smoothscale(prep, size)


def scale_image(prep, invert=False):
    prep_size = prep.get_size()
    size = (
        int(round(prep_size[0] * settings.scale)),
        int(round(prep_size[1] * settings.scale)),
    )
    if invert:
        return pygame.transform.flip(
            pygame.transform.smoothscale(prep, size), 1, 0)
    else:
        return pygame.transform.smoothscale(prep, size)


def find_images(d, can_yield=False):
    if not re.search(directory.main, d) \
            and not re.search(directory.homedir, d):
        d = os.path.join(directory.main, d)
    return [
        image(os.path.join(d, item))
        for item in sorted(os.listdir(d))
        if (item.endswith(".png") or item.endswith(".PNG"))
    ]


def invert_images(imglist):
    return [pygame.transform.flip(img, 1, 0) for img in imglist]
