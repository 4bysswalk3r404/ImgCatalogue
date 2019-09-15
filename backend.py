import os
from PIL import Image
import numpy as np

def ByteFill(bytes, size):
    return bytes + (size - len(bytes)) * b'\x00'

class Catalogue:
    def __init__(self, path):
        self.path = path
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

    def getImages(self):
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

        images = []
        #loop through images
        for i in range(imgnum):
            #get image name
            imgname = data[:100].decode('utf-8').strip('\x00')
            #get size of current image
            imgsize = int.from_bytes(data[100:104], 'big')
            #get data of current image from imgsize
            imgdata = data[104:104+imgsize]
            #add image data to list
            images.append([imgname, imgdata])
            #get rid of image data
            data = data[imgsize+104:]
        return images

    def addImage(self, path):
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
        #get all image extentions
        #get all files in given directory
        files = [path for sub in [[os.path.join(w[0], file) for file in w[2]] for w in os.walk(path)] for path in sub]
        #loop through files
        for file in files:
            #if file is an image
            if os.path.splitext(file)[1] in self.imageExtenions:
                print(file)
                self.addImage(file)

    def renameImage(self, index, newname):
        images = self.getImages()
        with open(self.path, "wb") as catalogue:
            catalogue.write(len(images).to_bytes(1, 'big'))
            for i, image in enumerate(images):
                if i == index:
                    catalogue.write(ByteFill(newname.encode('utf-8'), 100))
                else:
                    catalogue.write(ByteFill(image[0].encode('utf-8'), 100))
                catalogue.write(len(image[1]).to_bytes(4, 'big'))
                catalogue.write(image[1])

    def removeImage(self, index):
        images = self.getImages()
        #loop through images
        with open(self.path, "wb") as catalogue:
            #write number of images to file
            catalogue.write((len(images) - 1).to_bytes(1, 'big'))
            #loop through images adding all except index
            for i, image in enumerate(images):
                if i != index:
                    #add file name
                    catalogue.write(ByteFill(image[0].encode('utf-8'), 100))
                    #add image size
                    catalogue.write(len(image[1]).to_bytes(4, 'big'))
                    #add image data
                    catalogue.write(image[1])

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
