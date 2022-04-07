# -*- coding: utf-8 -*-

import interactive.princess as princess
import os
import datetime
import pygame
import settings
import database
from settings import scale
from settings import directory


def save_file(
    universe,
    hairback=None,
    skin=None,
    face=None,
    hair=None,
    shoes=None,
    dress=None,
    arm=None,
    armdress=None,
    accessory=None,
    past_ball=None,
    great_past_ball=None,
    position=None,
    Ball=None,
):
    Princess = universe.stage.princesses[0]
    # avoid errors in case there are no saved files
    try:
        os.mkdir(os.path.join(directory.saves, Princess.name))
    except:
        pass
    save_thumbnail(universe)
    dir = os.path.join(directory.saves, Princess.name)
    day = datetime.datetime.today()
    if dress == "dress_yellow":
        armdress = "sleeve_yellow"
    elif dress == "dress_red":
        armdress = "sleeve_red"
    elif dress == "dress_kimono":
        armdress = "sleeve_kimono"
    elif dress == "dress_indian":
        armdress = "sleeve_indian"
    else:
        armdress = "None"
    hair_backs = [
        "hair_black",
        "hair_brown",
        "hair_rastafari",
        "hair_rapunzel",
        "hair_red",
        "hair_braid_and_tail",
    ]
    if hair in hair_backs:
        hairback = hair + "_back"
    else:
        hairback = "None"
    database.update.princess_garment(
        universe,
        Princess,
        hairback,
        skin,
        arm,
        face,
        hair,
        shoes,
        dress,
        armdress,
        accessory,
    )
    print("Save Database saved ")
    return os.path.join(directory.saves, Princess.name, Princess.name + ".glamour")


def save_thumbnail(universe):
    Princess = universe.stage.princesses[0]
    thumbnail = pygame.transform.flip(
        pygame.transform.smoothscale(Princess.stay_img.left[0], (100, 100)), 1, 0
    )
    pygame.image.save(
        thumbnail, os.path.join(directory.saves, Princess.name, "thumbnail.PNG")
    )
