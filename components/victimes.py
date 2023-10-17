import random as rd

class Victim:
    def __init__(self, name) -> None:
        self.name = name
        self.max_tolerance = rd.choice(range(80,120))
        self.tolerance = self.max_tolerance
        self.scream_sound = rd.choice(['a', 'o', 'u'])
        self.scream_mod = rd.choice(['h', 'y'])
        self.scream_is_weird = rd.choice([True, False])

    def hurt(self, value):
        self.tolerance -= value
        if self.tolerance < 0 :
            self.scream(abs(self.tolerance))
            self.tolerance = self.max_tolerance
    
    def scream(self, intensity):
        scream = ''
        for i in range(int(intensity)):
            scream += self.scream_sound