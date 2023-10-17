import random as rd

class Victim:
    def __init__(self, name) -> None:
        self.name = name
        self.max_tolerance = rd.choice(range(50,70))
        self.tolerance = self.max_tolerance
        self.scream_sound = rd.choice(['a', 'o', 'u', 'i'])
        self.scream_mod = rd.choice(['h', 'y', 'g'])
        self.scream_is_weird = rd.choice([True, False])

    def hit(self, value):
        self.tolerance -= value
        message = self.name
        if self.tolerance < 0 :
            self.scream(abs(self.tolerance))
            message += ' hurle de douleur'
            self.tolerance = self.max_tolerance
        elif self.tolerance < 15 :
            message += ' va bientot craquer'
        elif self.tolerance < 30 :
            message += ' a très mal mais reste digne'
        elif self.tolerance < 55 :
            message += ' grimace d’inconfort'
        else :
            message += ' s’en fout'

        print(message)
    
    def scream(self, intensity):
        scream = ''
        for i in range(int(intensity)):
            if (i%3 == 0 and self.scream_is_weird) or i >= intensity-2 :
                scream += self.scream_mod
            else:
                scream += self.scream_sound

        scream += f' {"!"*(intensity//5)} '
        print(scream)