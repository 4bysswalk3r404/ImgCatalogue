import os
from PIL import Image
import cv2
import numpy as np
import io
import json

def ByteFill(bytes, size):
    return bytes + (size - len(bytes)) * b'\x00'

def GetImages():
    #make sure main file exists
    if os.path.exists("catalogue.dat"):
        data = open("catalogue.dat", "rb").read()
    else:
        #if it doest throw an error
        raise Exception("catalogue.dat does not exist")
    #get number of images to loop through
    imgnum = int.from_bytes(data[:1], 'big')
    #omit first byte
    data = data[1:]

    images = []
    #loop through images
    for i in range(imgnum):
        #get image name
        imgname = data[:100]
        #get size of current image
        imgsize = int.from_bytes(data[100:104], 'big')
        #get data of current image from imgsize
        imgdata = data[104:104+imgsize]
        #add image data to list
        images.append([imgname, imgdata])
        #get rid of image data
        data = data[imgsize+104:]
    return images

def AddImage(path):
    #make sure given path exists
    if not os.path.exists(path):
        print(path, "does not exist")
        return 0
    #tell if main file exists
    if os.path.exists("catalogue.dat"):
        olddata = open("catalogue.dat", "rb").read()
    else:
        olddata = b''
    #where the magic happens
    with open("catalogue.dat", "wb") as catalogue:
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

def AddDir(path):
    exts = json.loads(open("extentions.json").read())
    files = [path for sub in [[os.path.join(w[0], file) for file in w[2]] for w in os.walk(path)] for path in sub]
    for file in files:
        if os.path.splitext(file)[1] in exts:
            print(file)
            AddImage(file)

def RemoveImage(index):
    images = GetImages()
    #loop through images
    with open("catalogue.dat", "wb") as catalogue:
        #write number of images to file
        catalogue.write((len(images) - 1).to_bytes(1, 'big'))
        #loop through images adding all except index
        for i, image in enumerate(images):
            if i != index:
                #add file name
                catalogue.write(image[0])
                #add image size
                catalogue.write(len(image[1]).to_bytes(4, 'big'))
                #add image data
                catalogue.write(image[1])

def LoopImages():
    #get list of images
    images = GetImages()
    #loop through images
    for image in images:
        #retrieve imagename
        imgname = image[0].strip(b'\x00').decode('utf-8')
        #if image is video, write to file
        if os.path.splitext(imgname)[1] in ['.gif', '.avi']:
            open(imgname, "wb").write(image[1])
        else:
            #create PIL image object
            img = Image.open(io.BytesIO(image[1]))
            #show image
            img.show()
            print(imgname)

if __name__ == "__main__":
    inp = input(">>>")
    if inp == "add":
        AddImage(input("new image path: "))
    elif inp == "loop":
        LoopImages()
    elif inp == "remove":
        RemoveImage(int(input("image index: ")))
    elif inp == "add dir":
        AddDir(input("new dir: "))
