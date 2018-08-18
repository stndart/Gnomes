#encoding: utf-8

import json
from jsonbuilder import action

class Cell:
    def __init__(self, name):
        self.name = name
        with open('resources/cells/properties.json', 'r') as f:
            self.properties = json.load(f)[self.name]
        if 'health' in self.properties:
            self.create_death_voice()
            self.properties.pop('death_voice')
    
    def create_death_voice(self):
        turninto = self.properties['death_voice']['turninto']
        loot = self.properties['death_voice']['loot'].copy()
        def death_voice():
            self.__init__(turninto)
            self.properties['loot'] = loot
            self.properties['actions'].append(action('getloot', 'resources/actions/getloot.png', repeats=1, duration=1, actions=[('loot',)], conditions=[]))
        self.death_voice = death_voice
        
class Player:
    def __init__(self, nick, coords, speed):
        self.nick = nick
        self.coords = coords.copy()
        self.old_coords = coords.copy()
        self.movement_progress = 0
        self.speed = speed
        self.cellsleft = speed
        self.backpack = Inventory()
        self.achievements = []

class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.storage = [['empty', 0] for i in range(size)]
        self.recipes = []
        self.available_recipes = []
        self.add('wooden_axe', 50)
    
    def count_empty(self):
        c = 0
        for e in self.storage:
            if e[0] == 'empty':
                c += 1
        return c
    
    def add(self, name, amount):
        found = False
        for i in range(self.size):
            if self.storage[i][0] == name:
                self.storage[i][1] += amount
                found = True
                break
        if found == False:
            for i in range(self.size):
                if self.storage[i][0] == 'empty':
                    self.storage[i][0] = name
                    self.storage[i][1] = amount
                    break
        print('Added %s %s' % (amount, name), flush=True)
    
    def lose(self, name, amount, silent=True):
        for i in range(self.size):
            if self.storage[i][0] == name:
                self.storage[i][1] -= amount
                if self.storage[i][1] == 0:
                    self.storage.pop(i)
                if self.storage[i][1] < 0:
                    if silent:
                        self.storage.pop(i)
                    else:
                        raise RuntimeError('InventoryError: lost more things then available')
                break
        else:
            if not silent:
                raise RuntimeError('InventoryError: lost more things then available')
    
    def contains(self, name, amount):
        for t, a in self.storage:
            if t == name and a >= amount:
                return True
        return False
    
    def find(self, name):
        for i in range(self.size):
            if self.storage[i][0] == name:
                return i
        return -1
    
    def load_recipes(self, fn):
        self.recipes = []
        with open(fn, 'r') as f:
            lines = f.readlines()
        for r in lines:
            words = r.split()
            q = 0
            ing = []
            res = []
            for w in words:
                if q == 0:
                    ing.append((w, 1))
                    q = 1
                elif q == 1:
                    if w == '*':
                        q = 2
                    elif w == '+':
                        q = 0
                    elif w == '=':
                        q = 4
                    else:
                        raise RuntimeError("Unexpected symbol %s" + w)    
                elif q == 2:
                    ing[-1] = (ing[-1][0], int(w))
                    q = 3
                elif q == 3:
                    if w == '+':
                        q = 0
                    elif w == '=':
                        q = 4
                    else:
                        raise RuntimeError("Unexpected symbol %s" + w)    
                elif q == 4:
                    res.append((w, 1))
                    q = 5
                elif q == 5:
                    if w == '*':
                        q = 6
                    elif w == '+':
                        q = 2
                    elif w == '=':
                        q = 8
                    else:
                        raise RuntimeError("Unexpected symbol %s" + w)                        
                elif q == 6:
                    res[-1] = (res[-1][0], int(w))
                    q = 7
                elif q == 7:
                    if w == '+':
                        q = 4
                    elif w == '=':
                        raise RuntimeError("Unexpected equation symbol") 
            self.recipes.append(Recipe(*zip(*ing), *zip(*res)))
    
    def check_recipe(self, recipe):
        for i, a in zip(recipe.ingridients, recipe.amount):
            found = False
            for j in range(self.size):
                if self.storage[j][0] == i:
                    found = True
                    if self.storage[j][1] < a:
                        return False
                    break
            if not found:
                return False
        return True
    
    def filter_recipes(self):
        self.available_recipes = []
        for r in self.recipes:
            if self.check_recipe(r):
                self.available_recipes.append(r)
    
    def perform_recipe(self, recipe):
        for i, a in zip(recipe.ingridients, recipe.amount):
            for j in range(self.size):
                if self.storage[j][0] == i:
                    self.storage[j][1] -= a
                    if self.storage[j][1] == 0:
                        self.storage[j] = ['empty', 0]
                    break
        for i, a in zip(recipe.result, recipe.ramount):
            for j in range(self.size):
                if self.storage[j][0] == i:
                    self.storage[j][1] += a
                    break
            else:
                for j in range(self.size):
                    if self.storage[j][0] == 'empty':
                        self.storage[j] = [i, a]
                        break

class Recipe:
    def __init__(self, ingridients, amount, result, ramount):
        self.ingridients = ingridients
        self.amount = amount
        self.result = result
        self.ramount = ramount
    
    def __repr__(self):
        amount = lambda m, a: '%s(x%s)' % (m, a) if a != 1 else m
        s = amount(self.ingridients[0], self.amount[0])
        for m, a in zip(self.ingridients[1:], self.amount[1:]):
            s += ', %s' % amount(m, a)
        s += ' → '
        s += amount(self.result[0], self.ramount[0])
        for m, a in zip(self.result[1:], self.ramount[1:]):
            s += ', %s' % amount(m, a)
        
        return s

if __name__ == '__main__':
    i = Inventory()
    i.load_recipes('resources/recipes.txt')
    i.add('rocks', 1)
    i.add('sticks', 3)
    print(i.check_recipe(i.recipes[0]))