class Cell:
    def __init__(self, name):
        self.name = name
        if self.name == 'grass':
            self.walken = 1
        if self.name == 'tree':
            self.walken = 2

class Player:
    def __init__(self, nick, coords, speed):
        self.nick = nick
        self.coords = coords
        self.speed = speed
        self.cellsleft = speed