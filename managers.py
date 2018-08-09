from PIL import Image
from PIL import ImageTk
import game

class DisplayManager:
    def __init__(self, wx, wy, gm):
        self.wx = wx
        self.wy = wy
        self.gm = gm
    
    def getimage(self):
        im = Image.new('RGBA', (self.wx, self.wy), color=(255, 0, 0))
        sprites = dict()
    
        w = 50
        h = 50        
        for i in range(len(self.gm.field)):
            for j in range(len(self.gm.field[i])):
                name = self.gm.field[i][j].name
                if name not in sprites:
                    sprites[name] = Image.open('resources/cells/%s.png' % name).convert(mode='RGBA')
                x = (j - 1/2 - self.gm.player.coords[0]) * w + 500 / 2
                y = (i - 1/2 - self.gm.player.coords[1]) * h + 500 / 2
                sprite = sprites[name].resize((w, h), resample=Image.BICUBIC)
                im.paste(sprite, (int(x), int(y)), mask=sprite)
            
        sprites['player'] = Image.open('resources/player.png').convert(mode='RGBA')
        x = (-1 / 2) * w + 500 / 2
        y = (-1 / 2) * h + 500 / 2
        sprite = sprites['player'].resize((w, h), resample=Image.BICUBIC)
        im.paste(sprite, (int(x), int(y)), mask=sprite)
        return ImageTk.PhotoImage(im)

class GameManager:
    def __init__(self, cx, cy, px, py):
        self.field = [[game.Cell('grass') for i in range(cx)] for j in range(cy)]
        self.player = game.Player('P1', [px, py], 10)
    
    def load_map(self, fn):
        f = open(fn, 'r')
        lines = f.readlines()
        f.close()
        self.field = [[game.Cell('grass') for i in range(len(lines[0].rstrip()))] for j in range(len(lines))]
        for i in range(len(lines)):
            for j in range(len(lines[0].rstrip())):
                if lines[i][j] == 'g':
                    self.field[i][j] = game.Cell('grass')
                if lines[i][j] == 't':
                    self.field[i][j] = game.Cell('tree')

class EventManager:
    def __init__(self, gm):
        self.gm = gm
    
    def arrowpressed(self, arrow):
        if arrow == 'up':
            if self.gm.player.coords[1] > 0:
                self.gm.player.coords[1] -= 1
        if arrow == 'down':
            if self.gm.player.coords[1] < len(self.gm.field) - 1:
                self.gm.player.coords[1] += 1
        if arrow == 'right':
            if self.gm.player.coords[0] < len(self.gm.field[0]) - 1:
                self.gm.player.coords[0] += 1
        if arrow == 'left':
            if self.gm.player.coords[0] > 0:
                self.gm.player.coords[0] -= 1