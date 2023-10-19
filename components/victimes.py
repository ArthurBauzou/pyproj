import random as rd
import math
from os.path import join as pjoin
import json

path = "C:/Users/poulp/Desktop/formation simplon/pyproj_01/data/scream.json"
with open(path, 'r', encoding='utf-8') as jf:
    data = json.load(jf)
    scr_text = data['scream_commentary']
    const= data['const']

MAX_T = const['max_tolerance']
MIN_T = const['min_tolerance']

class Victim:

    def __init__(self, name) -> None:
        self.name = name
        self.max_tolerance = rd.choice(range(MIN_T,MAX_T))
        self.tolerance = self.max_tolerance
        self.scream_sound = rd.choice(['a', 'o', 'u', 'i'])
        self.scream_mod = rd.choice(['h', 'y', 'g'])
        self.scream_is_weird = rd.choice([True, False])
        self.scream_number = 0

    def hit(self, value):
        self.tolerance -= value
        message = self.name
        scream = None
        if self.tolerance < 0 :
            # self.scream(abs(self.tolerance))
            message += f' {scr_text[0]}'
            scream = f' {self.scream(abs(self.tolerance)+8)}'
            self.tolerance = self.max_tolerance
        else:
            # calculer la proportion de l’endurance maximale ramenée à 4
            x = math.ceil((self.tolerance/MAX_T)*4)
            message += f' {scr_text[x]}'

        return message, scream
    
    def scream(self, intensity):
        scream = ''
        for i in range(int(intensity)):
            if (i%3 == 0 and self.scream_is_weird) or i >= intensity-2 :
                scream += self.scream_mod
            else:
                scream += self.scream_sound

        scream += f' {"!"*(intensity//5)} '
        self.scream_number += 1
        return scream