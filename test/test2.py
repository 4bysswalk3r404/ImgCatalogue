from PIL import Image, ImageSequence, ImageTk
import backend
import io
import os
import tkinter as tk
import sys
#from StringIO import StringIO

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(target/largest, 2)
    return (target, int(round(smallest) * percent))

class GIF:
    def __init__(self, name, data):
        im = Image.open(io.BytesIO(data))
        self.name = name
        self.frames = [ImageTk.PhotoImage(frame.copy().resize(shrinkImg(im.size), Image.ANTIALIAS)) for frame in ImageSequence.Iterator(im)]
        self.framerate = 20
        self.root = None
        self.master = None

    def __call__(self, root, master):
        self.root = root
        self.master = master
        self.root.after(0, self.update, 0)

    def update(self, ind):
        ind = ind % len(self.frames)
        frame = self.frames[ind]
        self.master.configure(image=frame)
        self.root.after(self.giftimeout, self.update, ind + 1)

class Main:
    def __init__(self, CataloguePath):
        self.catalogue = backend.Catalogue(CataloguePath)
        self.giftimeout = 26
        self.root = tk.Tk()
        self.frames = None
        self.MyImages = self.catalogue.getCatalogue()
        self.label = None

    def __call__(self):
        #frames = [PhotoImage(file='mygif.gif', format='gif -index %i' % (i)) for i in range(100)]
        self.frames = self.catalogue.gifs[0].frames
        self.label = tk.Label(self.root)
        self.label.pack()
        self.root.bind("<KeyPress>", self.keydown)
        self.root.after(0, self.update, 0)
        self.root.mainloop()

    def keydown(self, e):
        if e.char == 'w':
            self.giftimeout -= 1 if self.giftimeout > 1 else 1
        elif e.char == 's':
            self.giftimeout += 1
        print(self.giftimeout)

    def update(self, ind):
        ind = ind % len(self.frames)
        frame = self.frames[ind]
        self.label.configure(image=frame)
        self.root.after(self.giftimeout, self.update, ind + 1)

if __name__ == "__main__":
    Main("../catalogue.bin")()

#for MyImage in MyImages:
#    if os.path.splitext(MyImage[0])[1] in [".gif", ".avi"]:
#        img = Image.open(io.BytesIO(MyImage[1]))
#        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
#        print(image)
