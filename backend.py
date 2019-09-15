import os
from PIL import Image, ImageTk, ImageSequence
import numpy as np
from itertools import chain
import io
#from StringIO import StringIO

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(target/largest, 2)
    return (target, int(round(smallest) * percent))

def ByteFill(bytes, size):
    return bytes + (size - len(bytes)) * b'\x00'

class Catalogue:
    class GIF:
        def __init__(self, name, data):
            im = Image.open(io.BytesIO(data))
            self.name = name
            self.frames = [ImageTk.PhotoImage(frame.copy().resize(shrinkImg(im.size), Image.ANTIALIAS)) for frame in ImageSequence.Iterator(im)]

    class IMG:
        def __init__(self, name, data):
            self.name = name
            self.data = data

    def __init__(self, path):
        self.path = path
        self.gifs = None
        self.images = None
        self.imageExtenions = [
            ".ai",
            ".bmp",
            ".gif",
            ".ico",
            ".jpeg",
            ".jpg",
            ".png",
            ".ps",
            ".psd",
            ".svg",
            ".tif",
            ".jfif"
        ]

    def getCatalogue(self):
        #make sure main file exists
        if os.path.exists(self.path):
            data = open(self.path, "rb").read()
        else:
            #if it doest throw an error
            raise Exception("%s does not exist" % self.path)
        #get number of images to loop through
        imgnum = int.from_bytes(data[:1], 'big')
        #omit first byte
        data = data[1:]

        self.images = []
        self.gifs = []
        #loop through images
        for i in range(imgnum):
            #get image name
            imgname = data[:100].decode('utf-8').strip('\x00')
            #get size of current image
            imgsize = int.from_bytes(data[100:104], 'big')
            #get data of current image from imgsize
            imgdata = data[104:104+imgsize]
            #add image data to list
            if os.path.splitext(imgname)[1] == ".gif":
                self.gifs.append(self.GIF(imgname, imgdata))
            else:
                self.images.append(self.IMG(imgname, imgdata))
            #get rid of image data
            data = data[imgsize+104:]
        return list(chain.from_iterable((self.images, self.gifs)))

    def addFile(self, path):
        #make sure given path exists
        if not os.path.exists(path):
            return 0
        #tell if main file exists
        if os.path.exists(self.path):
            olddata = open(self.path, "rb").read()
        else:
            olddata = b''
        #where the magic happens
        with open(self.path, "wb") as catalogue:
            #write number of images to file
            catalogue.write((int.from_bytes(olddata[:1], 'big') + 1).to_bytes(1, 'big'))
            #write the previous data omitting the first byte
            catalogue.write(olddata[1:])
            #get new image data
            newdata = open(path, "rb").read()
            #add file name
            catalogue.write(os.path.basename(path).encode('utf-8') + (100 - os.path.basename(path).encode('utf-8').__len__()) * b'\x00')
            #add size of new image
            catalogue.write(len(newdata).to_bytes(4, 'big'))
            #add new image
            catalogue.write(newdata)
        return 1

    def addDir(self, path):
        #get all files in given directory
        files = [path for sub in [[os.path.join(w[0], file) for file in w[2]] for w in os.walk(path)] for path in sub]
        #loop through files
        for file in files:
            #if file is an image
            if os.path.splitext(file)[1] in self.imageExtenions or os.path.splitext(file)[1] in [".gif", ".avi"]:
                print(file)
                self.addFile(file)

    def rename(self, index, newname):
        items = self.getCatalogue()
        with open(self.path, "wb") as catalogue:
            catalogue.write(len(items).to_bytes(1, 'big'))
            for i, item in enumerate(items):
                if i == index:
                    catalogue.write(ByteFill(newname.encode('utf-8'), 100))
                else:
                    catalogue.write(ByteFill(item.name.encode('utf-8'), 100))
                catalogue.write(len(item.data).to_bytes(4, 'big'))
                catalogue.write(item.data)

    def remove(self, index):
        items = self.getCatalogue()
        #loop through images
        with open(self.path, "wb") as catalogue:
            #write number of images to file
            catalogue.write((len(items) - 1).to_bytes(1, 'big'))
            #loop through images adding all except index
            for i, item in enumerate(items):
                if i != index:
                    #add file name
                    catalogue.write(ByteFill(item.name.encode('utf-8'), 100))
                    #add image size
                    catalogue.write(len(item.name).to_bytes(4, 'big'))
                    #add image data
                    catalogue.write(item.name)

if __name__ == "__main__":
    inp = input(">>>")
    catalogue = Catalogue("../catalogue.bin")
    if inp == "add":
        catalogue.addImage(input("new image path: "))
    elif inp == "remove":
        catalogue.removeImage(int(input("image index: ")))
    elif inp == "add dir":
        catalogue.addDir(input("new dir: "))
    elif inp == "rename":
        catalogue.renameImage(int(input("index: ")), input("new name: "))
