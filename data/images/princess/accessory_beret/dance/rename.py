#!/usr/bin/env python
import os
import re

directory = "/home/nelson/glamour/data/images/princess/accessory_beret/dance/"
extension = ".png"
separator = "([0-9]*)"

original = os.listdir(directory)
new = []

for i in original:
    if i[-4:] == extension:
        item = []
        for a in re.split(separator, i):
            try:
                a = int(a)
                item.append(a)
            except:
                item.append(a)
        new.append(item)
new.sort()

for i in new:
    item = ""
    for part in i:
        if part.__class__ == int:
            if part < 10:
                zeros = "000"
            elif part < 100:
                zeros = "00"
            elif part < 1000:
                zeros = "0"
            else:
                zeros = ""
            item += zeros
        item += str(part)
        original = ""
        for part in i:
            original += str(part)
    print(original)
    os.rename(directory + original, directory + item)
