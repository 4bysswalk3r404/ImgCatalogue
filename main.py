import os
from PIL import Image, ImageTk
import cv2
import numpy as np
import io
import json
import tkinter as tk
import math
import backend

class FancyListbox(tk.Listbox):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        tk.Listbox.__init__(self, parent.root, *args, **kwargs)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
        self.popup_menu.add_command(label="Rename",
                                    command=self.rename_selected)

        self.bind("<Button-3>", self.popup) # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        print("remove", self.curselection()[0])
        self.parent.catalogue.removeImage(self.curselection()[0])
        self.parent.refreshImgList()

    def rename_selected(self):
        print("rename", self.curselection()[0], "to", end=" ")
        newname = self.parent.popup()
        print(newname)
        self.parent.catalogue.renameImage(self.curselection()[0], newname)
        self.parent.refreshImgList(ImgName=newname)

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(440/largest, 2)
    return (440, int(round(smallest) * percent))

class popupWindow(object):
    def __init__(self,master):
        top=self.top=tk.Toplevel(master)
        self.l=tk.Label(top,text="Hello World")
        self.l.pack()
        self.e=tk.Entry(top)
        self.e.bind("<Return>", self.cleanup)
        self.e.pack()
        self.value = None
    def cleanup(self, *ignore):
        self.value=self.e.get()
        self.top.destroy()

class Main:
    def __init__(self, CataloguePath):
        self.catalogue = backend.Catalogue(CataloguePath)
        self.root = tk.Tk()
        self.ImgLabel = None
        self.TkImgDict = None
        self.ImageListBox = None
        self.addType = tk.IntVar()

    def __call__(self):
        self.refreshImgList()

        screenDim = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        windowDim = (int((screenDim[0] / 5) * 2), int((screenDim[1] / 5) * 2))
        self.root.geometry(str(windowDim[0])+'x'+str(windowDim[1])+'+'
            +str((screenDim[0] - windowDim[0]) // 2)+'+'+str((screenDim[1] - windowDim[1]) // 2)
        )

        self.root.configure(background='#133337')
        #tk.Radiobutton(self.root, text="Image Dir", value=0, variable=self.addType).grid()
        #tk.Radiobutton(self.root, text="Image File", value=1, variable=self.addType).grid()

        tk.Label(self.root, text="Add Image: ").grid(row=0, column=0)
        InputBox = tk.Entry(self.root)
        InputBox.grid(row=0, column=3)
        InputBox.bind("<Return>", self.AddImage_Tkinter)
        self.root.mainloop()

    def popup(self):
        w=popupWindow(self.root)
        self.root.wait_window(w.top)
        return w.value

    def list_entry_clicked(self, *ignore):
        ImgName = self.ImageListBox.get(self.ImageListBox.curselection()[0])
        self.ImgLabel.config(image=self.TkImgDict[ImgName])

    def refreshImgList(self, **kwargs):
        self.TkImgDict = {}
        self.ImageListBox = FancyListbox(self, selectmode=tk.SINGLE)
        MyImages = self.catalogue.getImages()
        self.root.update()
        print("Root window: ", self.root.winfo_width(), self.root.winfo_height())
        for i, MyImage in enumerate(MyImages):
            ImgName = MyImage[0]
            PIL_img = Image.open(io.BytesIO(MyImage[1]))
            print(ImgName, PIL_img.size, end=" ")
            PIL_img = PIL_img.resize(shrinkImg(PIL_img.size), Image.ANTIALIAS)
            print(PIL_img.size)
            CurrentTkImg = ImageTk.PhotoImage(PIL_img)
            self.TkImgDict[ImgName] = CurrentTkImg
            self.ImageListBox.insert(tk.END, ImgName)
        self.ImageListBox.grid(row=1, column=3)
        self.ImgLabel = tk.Label()
        self.ImgLabel.grid(row=1)
        self.ImageListBox.bind('<ButtonRelease-1>', self.list_entry_clicked)
        ImgName = kwargs.get("ImgName")
        if ImgName != None:
            self.ImgLabel.config(image=self.TkImgDict[ImgName])
        else:
            self.ImgLabel.config(image=self.TkImgDict[list(self.TkImgDict.keys())[0]])

    def AddImage_Tkinter(self, event):
        inputValue = event.widget.get()
        if os.path.isfile(inputValue) and os.path.splitext(inputValue)[1] in self.catalogue.imageExtenions:
            if self.TkImgDict.get(inputValue) == None:
                self.catalogue.addImage(inputValue)
                print("adding %s..." % inputValue)
                self.refreshImgList(ImgName=os.path.basename(inputValue))
            else:
                print(inputValue, "already exists")
        else:
            print(inputValue, "\tis not an image file")

if __name__ == "__main__":
    Main("../catalogue.bin")()
