class Cell:
    def __init__(self, name, walken=1):
        self.name = name
        self.walken = walken

class Player:
    def __init__(self, nick, coords, speed):
        self.nick = nick
        self.coords = coords
        self.speed = speed