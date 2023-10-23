from components.victimes import Victim

def test_victim():
    vic = Victim('testbuddy')
    scream = vic.scream(8)
    print(type(scream))

