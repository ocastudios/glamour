import pygame
import utils
import random
import settings
from settings import directory
import interactive.messages as messages
import interface.widget     as widget 
import os


p = settings.p
j = os.path.join
fairy_dir = j(directory.interface, 'fairy_tips')

class Fairy():
    """This class defines the tip fairy, who helps the princess during the game."""
    paths = (
            ((14, 22),     (28, 44),      (52, 68),      (57, 80), 
             (75, 98),     (85, 110),     (97, 118),     (111, 132), 
             (119, 138),   (124, 142),    (132, 148),    (144, 156), 
             (162, 168),   (182, 178),    (206, 190),    (226, 202), 
             (255, 214),   (279, 224),    (301, 230),    (325, 236), 
             (349, 244),   (373, 246),    (397, 246),    (423, 244), 
             (449, 244),   (477, 240),    (499, 240),    (521, 234), 
             (547, 228),   (575, 222),    (601, 214),    (625, 206), 
             (651, 195),   (675, 185),    (697, 173),    (729, 165), 
             (755, 157),   (783, 147),    (804, 141),    (830, 131), 
             (856, 127),   (882, 123),    (910, 121),    (938, 125), 
             (969, 133),   (995, 139),    (1019, 155),   (1037, 169), 
             (1047, 185),  (1058, 201),   (1068, 223),   (1072, 245), 
             (1071, 267),  (1065, 285),   (1061, 303),   (1053, 319), 
             (1037, 332),  (1016, 354),   (988, 370),    (960, 378), 
             (938, 388),   (912, 392),    (888, 394),    (858, 396), 
             (830, 404),   (806, 410),    (784, 420),    (756, 434), 
             (734, 448),   (717, 465),    (701, 489),    (699, 513), 
             (696, 533),   (694, 557),    (708, 585),    (718, 601), 
             (737, 619),   (759, 637),    (779, 651),    (809, 663), 
             (836, 671),   (858, 675),    (878, 677),    (898, 675), 
             (918, 675),   (938, 685),    (964, 695),    (984, 703), 
             (1008, 710),  (1030, 714),   (1054, 716),   (1077, 716), 
             (1105, 715),  (1133, 714),   (1159, 710),   (1191, 703), 
             (1200, 700)
            ),
            (
            (765, 0),      (762, 8),      (758, 14),     (756, 26), 
            (756, 30),     (758, 38),     (767, 50),     (783, 60), 
            (803, 68),     (827, 74),     (850, 80),     (886, 88), 
            (914, 96),     (925, 110),    (929, 126),    (929, 138), 
            (922, 162),    (915, 188),    (897, 206),    (881, 220), 
            (866, 235),    (836, 247),    (790, 263),    (742, 275), 
            (686, 287),    (632, 299),    (602, 303),    (578, 305), 
            (555, 311),    (527, 315),    (497, 319),    (469, 325), 
            (443, 331),    (413, 339),    (375, 351),    (343, 367), 
            (318, 387),    (294, 411),    (281, 439),    (278, 474), 
            (279, 510),    (292, 546),    (310, 580),    (331, 606), 
            (354, 630),    (380, 650),    (409, 675),    (437, 687), 
            (472, 705),    (502, 719),    (535, 731),    (571, 743), 
            (611, 753),    (652, 759),    (696, 763),    (730, 765), 
            (770, 765),    (808, 763),    (850, 759),    (896, 741), 
            (934, 727),    (963, 707),    (993, 691),    (1018, 666), 
            (1050, 642),   (1073, 616),   (1097, 586),   (1116, 556), 
            (1133, 526),   (1146, 488),   (1150, 452),   (1143, 419), 
            (1130, 385),   (1109, 359),   (1091, 337),   (1064, 319), 
            (1036, 305),   (1001, 291),   (971, 287),   (937, 281), 
            (901, 281),    (861, 285),    (829, 291),    (795, 299), 
            (771, 313),    (746, 335),    (722, 361),    (705, 389), 
            (685, 413),    (682, 445),    (677, 470),    (678, 506), 
            (676, 538),    (687, 568),    (706, 584),    (730, 600), 
            (743, 622),    (771, 646),    (804, 656),    (834, 666), 
            (881, 676),    (913, 686),    (956, 696),    (992, 700), 
            (1030, 701),   (1064, 702),   (1096, 703),   (1129, 704), 
            (1161, 705),   (1195, 706),   (1200, 707),   (1200, 708), 
            (1200, 709),   (1200, 710)
            ),
            (
            (1440,  42),   (1426,  46),   (1410,  51),   (1392,  57), 
            (1376,  61),   (1356,  69),   (1334,  75),   (1314,  77), 
            (1286,  80),   (1266,  86),   (1246,  86),   (1222,  92), 
            (1198,  99),   (1176, 101),   (1156, 103),   (1134, 103), 
            (1110, 101),   (1090, 101),   (1070, 104),   (1056, 98), 
            (1032, 92),    (1006, 88),    (988, 82),    (970, 76), 
            (949, 70),     (933, 63),     (911, 55),     (889, 45), 
            (871, 33),     (851, 27),     (827, 21),     (807, 15), 
            (783, 12),     (763, 8),     (742, 6),     (722, 4), 
            (698, 0),      (678, 0),      (654, 7),      (634, 17), 
            (617, 33),     (593, 41),     (571, 42),     (555, 36), 
            (538, 26),     (516, 16),     (494, 4),     (466, 6), 
            (446, 8),      (430, 5),      (412, 0),      (382, 0), 
            (350, 5),      (310, 10),      (266, 14),      (224, 22), 
            (196, 35),     (166, 51),     (132, 73),     (111, 98), 
            (93, 120),     (85, 146),     (71, 178),     (64, 210), 
            (62, 239),     (73, 273),     (95, 301),     (113, 327), 
            (143, 346),    (170, 364),    (208, 378),    (244, 378), 
            (276, 371),    (306, 357),    (336, 339),    (369, 316), 
            (399, 290),    (427, 270),    (465, 241),    (499, 221), 
            (532, 199),    (566, 176),    (594, 166),    (630, 162), 
            (658, 157),    (696, 147),    (740, 143),    (782, 144), 
            (822, 146),    (866, 139),    (906, 143),    (942, 153), 
            (985, 165),    (1015, 176),    (1047, 190),    (1075, 204), 
            (1097, 228),   (1120, 252),   (1138, 274),   (1150, 306), 
            (1165, 330),   (1167, 362),   (1163, 400),   (1154, 430), 
            (1138, 465),   (1110, 497),   (1079, 544),   (1047, 580), 
            (1020, 606),   (982, 637),   (944, 661),   (906, 682), 
            (870, 700),    (831, 716),    (803, 721),    (778, 721), 
            (762, 721),    (744, 717),    (724, 705),    (702, 691), 
            (690, 671),    (679, 637),    (685, 597),    (697, 567), 
            (704, 543),    (722, 510),    (738, 474),    (761, 436), 
            (783, 403),    (801, 377),    (828, 353),    (858, 336), 
            (886, 328),    (920, 316),    (960, 313),    (996, 309), 
            (1036, 311),   (1068, 319),   (1103, 326),   (1137, 332), 
            (1161, 340),   (1191, 360),   (1217, 380),   (1242, 395), 
            (1260, 415),   (1280, 441),   (1304, 465),   (1327, 491), 
            (1315, 517),   (1300, 530),   (1290, 550),   (1280, 570), 
            (1270, 590),   (1260, 610),   (1240, 630),   (1220, 655), 
            (1210, 680),   (1205, 690),   (1200, 700))
            )
    whistle     = pygame.mixer.Sound(j(directory.sounds,'story','frames','s03.ogg'))
    music       = j(directory.music,'1stSnowfall.ogg')
    def __init__(self, pos, level,margin=p([10,10,10,10]),dirty=False):
        self.size               = p((10,10))
        self.level              = level
        self.universe           = self.level.universe
        self.center_distance    = pos
        self.pos                =  p([-200,600])
        self.lists_of_images = {
                        'mouth_speak':      utils.img.TwoSided(j(fairy_dir,'fairy_speak'),margin),
                        'mouth_smile':      utils.img.There_and_back_again(j(fairy_dir,'fairy_smile'),margin),

                        'eyes_eyes':        utils.img.There_and_back_again(j(fairy_dir,'fairy_eyes'),margin),
                        'eyes_blink':       utils.img.There_and_back_again(j(fairy_dir,'fairy_blink'),margin),

                        'wings_wings':      utils.img.TwoSided(j(fairy_dir,'fairy_wings'),margin),
                        'wings_fly':        utils.img.TwoSided(j(fairy_dir,'fairy_fly_wings'),margin),

                        'body_fly':         utils.img.There_and_back_again(j(fairy_dir,'fairy_fly'),margin),
                        'body_stand_right': utils.img.There_and_back_again(j(fairy_dir,'fairy_stand_right'),margin),
                        'body_stand_left' : utils.img.There_and_back_again(j(fairy_dir,'fairy_stand_left'),margin)
                    }
        self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
        self.parts      = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
        self.size       = self.parts[1].get_size()
        self.image      = pygame.Surface(self.size,pygame.SRCALPHA).convert_alpha()
#        self.goalpos    = p([1200,700])
        self.direction  = "left"
        self.action     = self.explain
        self.count      = 0
        self.wand       = utils.img.TwoSided(j(fairy_dir,'fairy_wand'),margin)
        self.enchant    = utils.img.TwoSided(j(fairy_dir,'fairy_enchant'),margin)
        self.spark      = utils.img.OneSided(j(fairy_dir,'spark'),margin)
        self.actual_path       = random.randint(0,2)
        self.path_number = 0
        self.max_path_number = len(self.paths[self.actual_path])-1
        self.reached_goal = False

    def update_all(self):
        for key,value in self.lists_of_images.items():
            value.update_number()
        self.action()

    def wait(self):
        pass

    def explain(self):
        self.select_images()
        self.image = self.update_image()
        if not self.reached_goal:
            self.fly_to_goal()
        else:
            if self.pos[0]>(self.universe.width/2):
                self.direction = "left"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
            else:
                self.direction = "right"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']

    def select_images(self):
        if self.direction == "left":
            self.parts = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
        else:
            self.parts = [self.lists_of_images[i].right[self.lists_of_images[i].number] for i in self.images_strings]

    def update_image(self):
        image = pygame.Surface(self.size,pygame.SRCALPHA).convert_alpha()
        for i in self.parts:
            if i:
                image.blit(i,(0,0))
        return image

    def fly_to_goal(self):
        old_pos = self.pos
        self.pos = p(self.paths[self.actual_path][self.path_number])
        if self.path_number < self.max_path_number:
            self.path_number +=1
        self.images_strings = ["wings_fly","body_fly"]
        if old_pos[0] > self.pos[0]:
            self.direction = "left"
        else:
            self.direction = "right"



class Message():
    button = None
    def __init__(self, level, message = "Oops! I just forgot what I had to say... One of us should have a conversation with the programmer."):
        self.message    = message
        self.level      = level
        self.universe   = universe = self.level.universe
        self.image      = utils.img.image(j(fairy_dir,'balloon','0.png'))
        self.size       = self.image.get_size()
        self.pos        = ((universe.width - self.size[0])/2, universe.height - self.size[1])
        self.text_box   = self.size[0]*.8,self.size[1]*.8
        self.font_size  = p(14)
        self.text_font  = pygame.font.Font(j(directory.fonts,'FreeSans.ttf'),int(round(self.font_size+(self.font_size/2))))
        self.color      = (0,0,0,0)
        self.image.blit(self.adjusting_fonts(), self.pos)
        self.button     = self.button or widget.Button(directory.button_ok,(1200,800),self.level,self.end_message)
        self.level.fae.append(self.button)

    def update_all(self):
        pass

    def end_message(self):
        self.level.fairy = 'done'
        self.level.fae[1].path_number = 0
        self.level.fae[1].pos =  p([-200,600])
        self.level.fae.remove(self.button)

    def adjusting_fonts(self):
        fix_x       = p(150)
        fix_y       = p(40)
        font_object = self.text_font
        text_box    = self.text_box
        image = self.image
        text_list = self.message.split()
        number_of_words = len(text_list)
        count = 0
        height = fix_y
        first = True
        line = ""
        line_break  = False
        while count < number_of_words:
            line        += text_list[count]
            line_size   = font_object.size(line)
            line_pos = int((text_box[0]+fix_x-line_size[0])/2)
            if line_size[0] < text_box[0]:
                if count+1 < number_of_words:
                    temporary_line = line + ' '+ text_list[count+1]
                    if font_object.size(temporary_line)[0] >= text_box[0]:
                        line_image = font_object.render(line,1, self.color)
                        height += int((line_size[1]*.8))
                        image.blit(font_object.render(line, 1, self.color), (line_pos,height))
                        line = ""
                    else:
                        line += ' '
                elif count+1 == number_of_words:
                    height += int((line_size[1]*.8))
                    image.blit(font_object.render(line, 1, self.color), (line_pos,height))
            else:
                line = text_list[count]
                height += int(line_size[1]*.8) #If line height is perfect it does not seem that it is the same text
            count += 1
        return image
