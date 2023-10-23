import random as rd
import numpy as np

class Projectile:
    def __init__(self, name) -> None:
        self.name = name
        self.speed = 0
        self.firmness = rd.choice(range(0,10))
        self.weight = rd.choice(range(1,8))

    def throw(self, speed=-1):
        if speed <= 0 : self.speed = rd.choice(np.arange(0.2,5,0.2))
        else : self.speed = speed
        
    def get_force(self):
        force = (self.weight / 2)*(self.speed**2)
        return round(force, 2)
    
    def get_pain(self):
        pain = int(self.get_force())*self.firmness
        return pain

# ce qui se passe quand on appelle directement le fichier
if __name__ == '__main__':
    print('Mauvais point d’entrée')