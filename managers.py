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
                x = (i - 1/2 - self.gm.player.coords[0]) * w + 500 / 2
                y = (j - 1/2 - self.gm.player.coords[1]) * h + 500 / 2
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
        self.field[1][1] = game.Cell('tree')
        self.player = game.Player('P1', (px, py), 10)