from tkinter import *
from time import time
from managers import DisplayManager, GameManager, EventManager
from random import choice


root = Tk()
root.geometry('500x500')
GM = GameManager(10, 10, 2, 3)
maps = ['maps/map.txt',
        'maps/map1.txt',
        'maps/map2.txt',
        'maps/map3.txt',
        'maps/map4.txt']
GM.load_map('maps/map4.txt')  # choice(maps))
EM = EventManager(GM)
DM = DisplayManager(500, 500, GM)
canv = Canvas()
canv.place(x=0, y=0, width=500, height=500)
imtk = DM.getimage()
im = canv.create_image(0, 0, image=imtk, anchor='nw')

spf = 1 / 10
def display():
    global im, imtk
    ts = time()
    canv.delete(im)
    imtk = DM.getimage()
    im = canv.create_image(0, 0, image=imtk, anchor='nw')
    timespent = time() - ts
    root.after(max(0, int((spf - timespent) * 1000)), display)

def event(e):
    if e.keysym_num in [65362, 119]:  # Up
        EM.arrowpressed('up')
    elif e.keysym_num in [65364, 115]:  # Down
        EM.arrowpressed('down')
    elif e.keysym_num in [65361, 97]:  # Left
        EM.arrowpressed('left')
    elif e.keysym_num in [65363, 100]:  # Right
        EM.arrowpressed('right')
    elif e.keysym_num == 65307:  # Escape
        EM.escape()
    elif e.keysym_num == 32:  # Space (next turn)
        EM.nextturn()
    elif e.keysym_num == 101:  # E (Inventory)
        EM.openinventory()
    elif e.keysym_num == 114:  # R (Action)
        EM.show_action()
    elif 48 <= e.keysym_num <= 57:  # from 0 to 9
        EM.numberpressed(e.keysym_num - 48)
    else:
        print(e.keysym_num, flush=True)
        pass

def mouseclick(button, e):
    if button == 1:
        EM.mouseclick(e.x, e.y)
    elif button == 2:
        EM.mouseclickright(e.x, e.y)

root.bind('<KeyPress>', event)
root.bind('<Button-1>', lambda e: mouseclick(1, e))
root.bind('<Button-3>', lambda e: mouseclick(3, e))
root.after(1000, display)
root.mainloop()