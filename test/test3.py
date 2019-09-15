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
    def __init__(self, root, master, name, frames):
        self.name = name
        self.frames = frames
        self.framerate = 20
        self.root = root
        self.master = master
        self._job = None

    def update(self, ind):
        ind = ind % len(self.frames)
        frame = self.frames[ind]
        self.master.configure(image=frame)
        self._job = self.root.after(self.framerate, self.update, ind + 1)

    def stop(self, *ignore):
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None

    def start(self, *ignore):
        self._job = self.root.after(0, self.update, 0)

    def rocker(self, *ignore):
        if self._job == None:
            self.start()
        else:
            self.stop()

class Main:
    def __init__(self, CataloguePath):
        self.catalogue = backend.Catalogue(CataloguePath)
        self.root = tk.Tk()
        self.label = None
        self.gif = None

    def __call__(self):
        self.catalogue.getCatalogue()
        self.label = tk.Label(self.root)
        self.label.pack()

        self.gif = GIF(self.root, self.label, self.catalogue.gifs[0].name, self.catalogue.gifs[0].frames)
        b = tk.Button(text="Kill", command=self.newImage)
        b.pack()
        self.root.bind("<KeyPress>", self.gif.rocker)
        self.gif.start()

        self.root.mainloop()

    def newImage(self):
        pass

if __name__ == "__main__":
    Main("../catalogue.bin")()

#for MyImage in MyImages:
#    if os.path.splitext(MyImage[0])[1] in [".gif", ".avi"]:
#        img = Image.open(io.BytesIO(MyImage[1]))
#        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
#        print(image)
