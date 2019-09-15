from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk()
root.title("Title")
root.geometry('600x600')

def shrinkImg(size, target=440):
    largest = max(size)
    smallest = min(size)
    percent = round(target/largest, 2)
    return (target, int(round(smallest) * percent))


def gcd(point):
    gcd = 1

    if point[0] % point[1] == 0:
        return point[1]

    for k in range(int(point[1] / 2), 0, -1):
        if point[0] % k == 0 and point[1] % k == 0:
            gcd = k
            break
    return gcd

image = Image.open('../jpg.jpg')
print(image.size)
print(gcd(image.size))

#def resize_image(event):
#    eventsize = (event.width, event.height)
#    imgsize = shrinkImg(basesize, min(eventsize))
#    image = copy_of_image.resize(imgsize)
#    photo = ImageTk.PhotoImage(image)
#    label.config(image = photo)
#    label.image = photo #avoid garbage collection


#basesize = image.size

#copy_of_image = image.copy()
#photo = ImageTk.PhotoImage(image)
#label = ttk.Label(root, image = photo)
#label.bind('<Configure>', resize_image)
#label.pack(fill=BOTH, expand = YES)

#root.mainloop()
