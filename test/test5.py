import os
from PIL import Image, ImageTk
import cv2
import numpy as np
import io
import json
import tkinter as tk
import math
#from StringIO import StringIO
import backend
import frontend

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(target/largest, 2)
    return (target, int(round(smallest) * percent))

class Main:
    def __init__(self, CataloguePath):
        self.catalogue = backend.Catalogue(CataloguePath)
        self.root = tk.Tk()
        self.imgLabel = None
        self.tkImgDict = {}
        self.tkGifDict = {}
        self.imgListBox = None
        self.gifDisplay = None
        self.baseColor = '#0e2f44'

    def __call__(self):
        self.refreshImgList()

        screenDim = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        windowDim = (int((screenDim[0] / 5) * 2), int((screenDim[1] / 5) * 2))
        self.root.geometry(str(windowDim[0])+'x'+str(windowDim[1])+'+'
            +str((screenDim[0] - windowDim[0]) // 2)+'+'+str((screenDim[1] - windowDim[1]) // 2)
        )

        self.root.configure(background=self.baseColor)

        tk.Label(self.root, text="Add Image: ").grid(row=0, column=1)
        InputBox = tk.Entry(self.root)
        InputBox.grid(row=0, column=2)
        InputBox.bind("<Return>", self.AddImage_Tkinter)
        InputBox.config(highlightbackground=self.baseColor)
        self.root.title("Image Database")
        self.root.iconbitmap(r"D:\Zone\icons\Franksouza183-Fs-Places-folder-python.ico")
        self.root.mainloop()

    def showChosen(self, *ignore):
        ImgName = self.imgListBox.get(self.imgListBox.curselection()[0])
        if self.gifDisplay != None and self.gifDisplay._job != None:
            self.gifDisplay.stop()
        if ImgName in self.tkImgDict:
            self.imgLabel.config(image=self.tkImgDict[ImgName])
        elif ImgName in self.tkGifDict:
            self.gifDisplay = frontend.GIF(self.root, self.imgLabel, ImgName, self.tkGifDict[ImgName])
            self.gifDisplay.start()

    def refreshImgList(self, **kwargs):
        self.catalogue.getCatalogue()
        self.tkImgDict = {}
        self.tkGifDict = {}
        self.imgListBox = frontend.FancyListbox(self, selectmode=tk.SINGLE)
        for img in self.catalogue.images:
            PIL_img = Image.open(io.BytesIO(img.data))
            print(img.name, PIL_img.size, end=" ")
            PIL_img = PIL_img.resize(shrinkImg(PIL_img.size), Image.ANTIALIAS)
            print(PIL_img.size)
            CurrentTkImg = ImageTk.PhotoImage(PIL_img)
            self.tkImgDict[img.name] = CurrentTkImg
            self.imgListBox.insert(tk.END, img.name)
        for gif in self.catalogue.gifs:
            self.imgListBox.insert(tk.END, gif.name)
            self.tkGifDict[gif.name] = gif.frames
        self.imgListBox.config(highlightbackground=self.baseColor)
        self.imgListBox.grid(row=2, column=2, sticky="ew")
        self.imgListBox.pack_propagate(0)
        self.imgLabel = tk.Label(width=440, height=340, bg=self.baseColor)
        self.imgLabel.configure(highlightbackground=self.baseColor)
        self.imgLabel.grid(row=2, column=0)
        self.imgListBox.bind('<ButtonRelease-1>', self.showChosen)
        ImgName = kwargs.get("ImgName")
        if ImgName == None:
            ImgName = list(self.tkImgDict)[0]
        if ImgName in self.tkImgDict:
            self.imgLabel.config(image=self.tkImgDict[ImgName])
        elif ImgName in self.tkGifDict:
            self.gifDisplay = frontend.GIF(self.root, self.imgLabel, ImgName, self.tkGifDict[ImgName])
            self.gifDisplay.start()

    def AddImage_Tkinter(self, event):
        inputValue = event.widget.get()
        if os.path.isfile(inputValue) and os.path.splitext(inputValue)[1] in self.catalogue.imageExtenions:
            if self.tkImgDict.get(inputValue) == None:
                self.catalogue.addFile(inputValue)
                print("adding %s..." % inputValue)
                self.refreshImgList(ImgName=os.path.basename(inputValue))
            else:
                print(inputValue, "already exists")
        else:
            print(inputValue, "\tis not an image file")

if __name__ == "__main__":
    Main("../catalogue.bin")()
