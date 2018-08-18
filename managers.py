from PIL import Image
from PIL import ImageTk
from PIL import ImageFont
from PIL import ImageDraw
import game

class DisplayManager:
    ANIMLEN = 100
    ANIMSTEP = 25
    def __init__(self, wx, wy, gm):
        self.wx = wx
        self.wy = wy
        self.gm = gm
        self.sprites = dict()
    
    def load_sprite(self, fn, spritename, size=None):
        if spritename not in self.sprites:
            sprite = Image.open(fn).convert(mode='RGBA')
            self.sprites[spritename] = dict()
            s = (sprite.width, sprite.height)
            self.sprites[spritename][s] = sprite
            self.sprites[spritename]['defaultsize'] = s
        defaultsize = self.sprites[spritename]['defaultsize']
        if size is not None and size not in self.sprites[spritename]:
            self.sprites[spritename][size] = self.sprites[spritename][defaultsize].resize(size, resample=Image.BICUBIC)
        return self.sprites[spritename][size]
    
    def getimage(self):
        im = Image.new('RGBA', (self.wx, self.wy), color=(255, 0, 0))
        
        if self.gm.inventory_opened:
            background = self.load_sprite('resources/inventory_back.png', 'inventory_back', (self.wx, self.wy))
            im.paste(background, (0, 0))
            
        else:
            # Animating player
            real_pos = self.gm.player.coords.copy()
            if self.gm.player.old_coords != self.gm.player.coords:
                self.gm.player.movement_progress += DisplayManager.ANIMSTEP
                if self.gm.player.movement_progress >= DisplayManager.ANIMLEN:
                    self.gm.player.old_coords = self.gm.player.coords.copy()
                    self.gm.player.movement_progress = 0
                else:
                    dx = self.gm.player.coords[0] - self.gm.player.old_coords[0]
                    dy = self.gm.player.coords[1] - self.gm.player.old_coords[1]
                    real_pos = [self.gm.player.old_coords[0] + dx * self.gm.player.movement_progress / DisplayManager.ANIMLEN,
                                self.gm.player.old_coords[1] + dy * self.gm.player.movement_progress / DisplayManager.ANIMLEN]
            
            # Drawing cells
            w = 50
            h = 50        
            for i in range(len(self.gm.field)):
                for j in range(len(self.gm.field[i])):
                    if 'health' in self.gm.field[i][j].properties and self.gm.field[i][j].properties['health'] <= 0:
                        self.gm.field[i][j].death_voice()
                        if [j, i] == self.gm.player.coords:
                            self.gm.show_action()
                            self.gm.show_action()
                    
                    name = self.gm.field[i][j].name
                    x = (j - 1/2 - real_pos[0]) * w + 500 / 2
                    y = (i - 1/2 - real_pos[1]) * h + 500 / 2
                    sprite = self.load_sprite('resources/cells/%s.png' % name, name, (w, h))
                    im.paste(sprite, (int(x), int(y)), mask=sprite)
            
            # Drawing player
            x = (-1 / 2) * w + 500 / 2
            y = (-1 / 2) * h + 500 / 2
            sprite = self.load_sprite('resources/player.png', 'player', (w, h))
            im.paste(sprite, (int(x), int(y)), mask=sprite)
            
            # Drawing action circle
            if self.gm.actions is not None:
                actionscircle = self.load_sprite('resources/actions/circle.png', 'actioncircle', (200, 200))
                im.paste(actionscircle, (int(x) + sprite.width // 2 - actionscircle.width // 2,
                                         int(y) + sprite.height // 2 - actionscircle.height // 2), mask=actionscircle)
                delta = (1j ** (4 / 6))
                radius = 70
                for i in range(6):
                    if hasattr(self.gm.actions[i], 'spritename') and hasattr(self.gm.actions[i], 'spritepath'):
                        spritepath = self.gm.actions[i].spritepath
                        spritename = self.gm.actions[i].spritename
                        action = self.load_sprite(spritepath, spritename, size=(60, 60))
                        cx = int(x) + sprite.width // 2 + radius * (delta ** i).real
                        cy = int(y) + sprite.height // 2 + radius * (delta ** i).imag
                        im.paste(action, (int(cx) - action.width // 2, int(cy) - action.height // 2), mask=action)
            
            # Adding 'turns left' indicator
            font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 35)
            draw = ImageDraw.Draw(im, mode='RGBA')
            draw.text((450, 0), str(self.gm.player.cellsleft), (0, 0, 0), font=font)
        
        return ImageTk.PhotoImage(im)

class GameManager:
    def __init__(self, cx, cy, px, py):
        self.field = [[game.Cell('grass') for i in range(cx)] for j in range(cy)]
        self.player = game.Player('P1', [px, py], 10)
        self.player.backpack.load_recipes('resources/recipes.txt')
        self.em = None
        self.inventory_opened = False
        self.actions = None
    
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
                if lines[i][j] == 'b':
                    self.field[i][j] = game.Cell('bush')
                if lines[i][j] == 'l':
                    self.field[i][j] = game.Cell('log')
    
    def openinventory(self):
        self.inventory_opened = not self.inventory_opened
        
        if self.inventory_opened:
            self.player.backpack.filter_recipes()
            
            print(self.player.backpack.storage)
            for i in range(len(self.player.backpack.available_recipes)):
                print(i + 1, self.player.backpack.available_recipes[i], flush=True)
    
    def show_action(self):
        if self.actions is None:
            self.actions = [lambda e: 0] * 6
            for i in range(6):
                self.actions[i].e = None
            py, px = self.player.coords
            i = 0
            actions = self.field[px][py].properties['actions']
            for j in range(len(actions)):
                if actions[j]['repeats'] > 0:
                    allowed = True
                    for condition in actions[j]['conditions']:
                        if not self.condition(condition):
                            allowed = False
                    if allowed:
                        self.actions[i] = lambda e: self.perform_action(e)
                        self.actions[i].e = actions[j]
                        self.actions[i].spritename = actions[j]['name']
                        self.actions[i].spritepath = actions[j]['texture']
                        i += 1
        else:
            self.actions = None
    
    def condition(self, condition):
        name = condition[0]
        if name == 'have':
            return self.player.backpack.contains(condition[1], condition[2])
        elif name == 'uhave':
            return not self.player.backpack.contains(condition[1], condition[2])
        elif name == 'gained':
            return getattr(self.player, condition[1]) >= condition[2]
        elif name == 'ugained':
            return getattr(self.player, condition[1]) < condition[2]
        elif name == 'achievement':
            return self.player.achievements.count(condition[1]) > 0
        elif name == 'uachievement':
            return self.player.achievements.count(condition[1]) == 0
        else:
            raise RuntimeError('Unknown condition %s' % condition)
    
    def perform_action(self, action):
        if self.player.cellsleft <= 0:
            return
        
        for a in action['actions']:
            if a[0] == 'give':
                self.player.backpack.add(a[1], a[2] + a[3] * action['performed'])
            elif a[0] == 'gain':
                setattr(self.player, a[1], getattr(self.player, a[1]) + a[2] + a[3] * action['performed'])
            elif a[0] == 'break':  # Lustig, aber 100 axes is in fact one axe with 100 uses
                self.player.backpack.add(a[1], a[2] + a[3] * action['performed'])
            elif a[0] == 'damage':
                if a[1] == 5:
                    py, px = self.player.coords
                    self.field[px][py].properties['health'] += a[2] + a[3] * action['performed']
                #elif
            elif a[0] == 'ach':
                self.player.achievements.append(a[1])
            elif a[0] == 'loot':
                py, px = self.player.coords
                cell = self.field[px][py]
                names = list(zip(*cell.properties['loot']))[0]
                ex = 0
                for e in self.player.backpack.storage:
                    if e[0] in names:
                        ex += 1
                if self.player.backpack.count_empty() >= len(cell.properties['loot']) - ex:
                    for e in cell.properties['loot']:
                        self.player.backpack.add(*e)
        action['performed'] += 1
        action['repeats'] -= 1
        self.player.cellsleft -= action['duration']
    
    def find_thing(self, name):
        py, px = self.player.coords
        if self.field[px][py].properties['things_left'][name] > 0:
            self.player.backpack.add(name, 3)
            self.field[px][py].properties['things_left'][name] -= 1
    
    def craft_recipe(self, i):
        self.player.backpack.perform_recipe(self.player.backpack.available_recipes[i])
        self.player.backpack.filter_recipes()
        
        print(self.player.backpack.storage)
        for i in range(len(self.player.backpack.available_recipes)):
            print(i + 1, self.player.backpack.available_recipes[i], flush=True)

class EventManager:
    def __init__(self, gm):
        self.gm = gm
        self.queue = list()
        self.gm.em = self
    
    def proceed_events(self):
        if len(self.queue) > 0:
            ev = self.queue[0]
            self.queue.pop(0)
            self.arrowpressed(ev)
    
    def arrowpressed(self, arrow):
        if self.gm.inventory_opened:
            self.queue.clear()
            return
        
        if self.gm.actions is not None:
            self.show_action()
        
        if self.gm.player.movement_progress != 0:
            self.queue.append(arrow)
            return
        
        is_moved = False
        
        if self.gm.player.cellsleft <= 0:
            self.queue.clear()
            return
        
        if arrow == 'up':
            if self.gm.player.coords[1] > 0:
                self.gm.player.coords[1] -= 1
                is_moved = True
        if arrow == 'down':
            if self.gm.player.coords[1] < len(self.gm.field) - 1:
                self.gm.player.coords[1] += 1
                is_moved = True
        if arrow == 'right':
            if self.gm.player.coords[0] < len(self.gm.field[0]) - 1:
                self.gm.player.coords[0] += 1
                is_moved = True
        if arrow == 'left':
            if self.gm.player.coords[0] > 0:
                self.gm.player.coords[0] -= 1
                is_moved = True
            
        coords = self.gm.player.coords
        if is_moved:
            self.gm.player.cellsleft -= self.gm.field[coords[1]][coords[0]].properties['walken']
        
        self.proceed_events()
    
    def escape(self):
        if self.gm.actions is not None:
            self.gm.show_action()
        elif self.gm.inventory_opened:
            self.gm.openinventory()
        else:
            exit()
    
    def nextturn(self):
        self.gm.player.cellsleft = self.gm.player.speed
    
    def openinventory(self):
        if self.gm.actions is not None:
            self.gm.show_action()
        self.gm.openinventory()
    
    def show_action(self):
        self.gm.show_action()
    
    def numberpressed(self, number):
        if self.gm.actions is not None:
            if number != 0 and number - 1 < len(self.gm.actions):
                self.gm.actions[number - 1](self.gm.actions[number - 1].e)
                self.gm.show_action()
                self.gm.show_action()
        elif self.gm.inventory_opened:
            if 0 < number <= len(self.gm.player.backpack.available_recipes):
                self.gm.craft_recipe(number - 1)