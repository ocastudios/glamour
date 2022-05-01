import pygame
from pygame.locals import *
from sys import exit


left = (K_LEFT, K_a)
right = (K_RIGHT, K_d)
kiss = (K_LCTRL, K_s, K_DOWN)
jump = (K_SPACE,)
ok = (K_RETURN,)
up = (K_UP, K_w)
down = (K_DOWN, K_s)
celebrate = (K_y,)


def main_menu(universe):
    universe.click = False
    universe.action[0] = None
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key in up:
                universe.action[0] = "up"
            elif event.key in down:
                universe.action[0] = "down"
            elif event.key in left:
                universe.action[0] = "left"
            elif event.key in right:
                universe.action[0] = "right"
        elif event.type == KEYUP:
            if event.key in (
                K_a,
                K_b,
                K_c,
                K_d,
                K_e,
                K_f,
                K_g,
                K_h,
                K_i,
                K_j,
                K_k,
                K_l,
                K_m,
                K_n,
                K_o,
                K_p,
                K_q,
                K_r,
                K_s,
                K_t,
                K_u,
                K_v,
                K_w,
                K_x,
                K_y,
                K_z,
                K_BACKSPACE,
                K_SPACE,
            ):
                universe.action[0] = pygame.key.name(event.key)
            if event.key == K_RETURN:
                universe.click = True
        elif event.type == MOUSEBUTTONUP:
            universe.click = True
    pygame.event.clear()


def stage(universe):
    if universe.level.princesses[0].inside or universe.level.paused:
        inside(universe)
    else:
        outside(universe)


def outside(universe):
    pointersize = None
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if (
                    not universe.level.paused
                    and not universe.level.princesses[0].inside
                    and not universe.level.ball
                ):
                    universe.level.pause.status = "inside"
                    universe.level.paused = True
            if event.key in left:
                universe.dir = "left"
                universe.action[1] = "walk"
            if event.key in right:
                universe.dir = "right"
                universe.action[1] = "walk"
            if event.key in kiss:
                universe.action[0] = "kiss"
            if event.key in jump:
                universe.action[0] = "jump"
            if event.key in ok:
                universe.action[0] = "OK"
            if event.key in up:
                if not universe.level.princesses[0].jump:
                    universe.action[0] = "open_door"
            if event.key == K_y:
                universe.action[0] = "celebrate"
        elif event.type == KEYUP:
            universe.action[0] = None
            if universe.level.princesses[0]:
                universe.level.princesses[0].doonce = False
            if (
                universe.dir == "left"
                and event.key in left
                    or (universe.dir == "right" and event.key in right)
            ):
                universe.action[1] = "stay"
        elif event.type == USEREVENT:
            pygame.mixer.music.queue(universe.level.music)
        elif event.type == MOUSEMOTION:
            pointersize = pointersize or universe.pointer.size
            universe.pointer.pos = (
                universe.pointer.mouse_pos[0] - (pointersize[0] / 2),
                universe.pointer.mouse_pos[1] - (pointersize[1] / 2),
            )
        universe.click = event.type == MOUSEBUTTONUP
        if universe.action[1] == "walk" and universe.action[0] == "open_door":
            universe.action[0] = None
        pygame.event.clear()


def inside(universe):
    pointersize = None
    universe.action[1] = "stay"
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        universe.click = True if event.type == MOUSEBUTTONUP else False
        if event.type == KEYUP:
            universe.action[0] = None
            if event.key in left:
                universe.dir = "left"
                universe.action[1] = "walk"
            if event.key in right:
                universe.dir = "right"
                universe.action[1] = "walk"
            if event.key in (K_LCTRL, K_SPACE, K_RETURN):
                universe.click = True
            if event.key in (K_UP, K_DOWN):
                universe.click = True
        elif event.type == USEREVENT:
            pygame.mixer.music.queue(universe.level.music)
        elif event.type == MOUSEMOTION:
            pointersize = pointersize or universe.pointer.size
            universe.pointer.pos = (
                universe.pointer.mouse_pos[0] - (pointersize[0] / 2),
                universe.pointer.mouse_pos[1] - (pointersize[1] / 2),
            )
    pygame.event.clear()
