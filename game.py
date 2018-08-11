class Cell:
    def __init__(self, name):
        self.name = name
        if self.name == 'grass':
            self.walken = 1
        if self.name == 'tree':
            self.walken = 2
        if self.name == 'bush':
            self.walken = 3
        if self.name == 'log':
            self.walken = 1

class Player:
    def __init__(self, nick, coords, speed):
        self.nick = nick
        self.coords = coords.copy()
        self.old_coords = coords.copy()
        self.movement_progress = 0
        self.speed = speed
        self.cellsleft = speed