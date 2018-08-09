from tkinter import *
from time import time
from managers import DisplayManager, GameManager


root = Tk()
root.geometry('500x500')
GM = GameManager(10, 10, 5, 5)
DM = DisplayManager(500, 500, GM)
canv = Canvas()
canv.place(x=0, y=0, width=500, height=500)
imtk = DM.getimage()
im = canv.create_image(0, 0, image=imtk, anchor='nw')

spf = 1#1 / 30
def display():
    global im, imtk
    ts = time()
    canv.delete(im)
    imtk = DM.getimage()
    im = canv.create_image(0, 0, image=imtk, anchor='nw')
    timespent = time() - ts
    root.after(max(0, int((spf - timespent) * 1000)), display)

root.after(1000, display)
root.mainloop()