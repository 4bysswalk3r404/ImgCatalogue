import os
import sys
import backend
import frontend
import io
from PIL import Image, ImageSequence, ImageTk
import tkinter as tk

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(target/largest, 2)
    return (target, int(round(smallest) * percent))

class Main:
    def __init__(self, CataloguePath):
        self.catalogue = backend.Catalogue(CataloguePath)
        self.root = tk.Tk()
        self.imgLabel = tk.Label()
        self.imgListbox = frontend.FancyListbox(self, selectmode=tk.SINGLE)
        self.gifDisplay = None
        self.tkImgDict = {}
        self.tkGifDict = {}
        self.baseColor = "#0e2f44"

    def __call__(self):
        #refresh
        self.imgListbox.bind('<ButtonRelease-1>', self.showChosen)
        self.imgListbox.grid()
        self.refresh()
        #set window dimensions
        screenDim = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        windowDim = (int((screenDim[0] / 5) * 2), int((screenDim[1] / 5) * 2))
        self.root.geometry(str(windowDim[0])+'x'+str(windowDim[1])+'+'
            +str((screenDim[0] - windowDim[0]) // 2)+'+'+str((screenDim[1] - windowDim[1]) // 2)
        )
        #set window background color
        self.root.configure(background=self.baseColor)
        #create image addition entry
        tk.Label(self.root, text="Add Image: ").grid(row=0, column=1)
        InputBox = tk.Entry(self.root)
        InputBox.grid(row=0, column=2)
        InputBox.bind("<Return>", self.AddImage_Tkinter)
        InputBox.config(highlightbackground=self.baseColor)
        #set window title and icon
        self.root.title("Image Database")
        self.root.iconbitmap(r"D:\Zone\icons\Franksouza183-Fs-Places-folder-python.ico")
        self.root.mainloop()

    def refresh(self, **kwargs):
        #get list of gifs and images
        self.tkImgDict = {}
        self.tkGifDict = {}
        items = self.catalogue.getCatalogue()
        #self.imgListbox.delete(1.0, tk.END)
        for img in self.catalogue.images:
            self.imgListbox.insert(tk.END, img.name)
            PIL_img = Image.open(io.BytesIO(img.data))
            self.tkImgDict[img.name] = ImageTk.PhotoImage((PIL_img).resize(shrinkImg(PIL_img.size), Image.ANTIALIAS))
        for gif in self.catalogue.gifs:
            self.imgListbox.insert(tk.END, img.name)
            self.tkGifDict[gif.name] = gif.frames
        #set imgLabel
        current = kwargs.get("current")
        if current == None:
            current = list(self.tkImgDict)[0]
        if current in self.tkImgDict:
            self.imgLabel.config(image=self.tkImgDict[current])
        elif current in self.tkGifDict:
            self.gifDisplay = frontend.GIF(self.root, self.imgLabel, current, self.tkGifDict[current])
            self.gifDisplay.start()

    def AddImage_Tkinter(self, event):
        inputValue = event.widget.get()
        if os.path.isfile(inputValue) and os.path.splitext(inputValue)[1] in self.catalogue.imageExtenions:
            if self.TkImgDict.get(inputValue) == None:
                self.catalogue.addFile(inputValue)
                print("adding %s..." % inputValue)
                self.refreshImgList(ImgName=os.path.basename(inputValue))
            else:
                print(inputValue, "already exists")
        else:
            print(inputValue, "\tis not an image file")

    def showChosen(self, *ignore):
        ImgName = self.imgListbox.get(self.imgListbox.curselection()[0])
        if ImgName in self.tkImgDict:
            self.imgLabel.config(image=self.tkImgDict[ImgName])
        elif ImgName in self.tkGifDict:
            self.gifDisplay = frontend.GIF(self.root, self.imgLabel, ImgName, self.tkGifDict[ImgName])
            self.gifDisplay.start()

    def addFile(self):
        pass

    def removeFile(self):
        pass

if __name__ == "__main__":
    Main("../catalogue.bin")()
