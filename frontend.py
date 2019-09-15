import tkinter as tk

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
        if self.gif._job == None:
            self.gif.start()
        else:
            self.gif.stop()

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

    #def popup(self):
    #    w=popupWindow(self.root)
    #    self.root.wait_window(w.top)
    #    return w.value


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
        self.parent.catalogue.remove(self.curselection()[0])
        self.parent.refreshImgList()

    def rename_selected(self):
        print("rename", self.curselection()[0], "to", end=" ")
        newname = self.parent.popup()
        print(newname)
        self.parent.catalogue.rename(self.curselection()[0], newname)
        self.parent.refreshImgList(ImgName=newname)
