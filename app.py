import components.victimes as vic
import components.projectiles as proj
import random as rd

def throw_at(victim:vic.Victim, object:proj.Projectile):
    object.throw()
    print(f'{object.name} a été jetté sur {victim.name} avec une force de {object.get_force()}')
    victim.hit(object.get_pain())
    object.speed = 0
    print('–––––––')


brian = vic.Victim('brian')
marc = vic.Victim('marc')
eloise = vic.Victim('eloise')
victims = [brian, eloise, marc]

parpaing = proj.Projectile('un parpaing')
fourchette = proj.Projectile('une fourchette')
annuaire = proj.Projectile('un annuaire')
objects = [parpaing, fourchette, annuaire]

rd.shuffle(victims)
rd.shuffle(objects)

for o,v in zip(objects, victims):
    throw_at(v, o)