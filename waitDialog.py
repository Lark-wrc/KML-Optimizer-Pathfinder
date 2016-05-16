import Tkinter as tk
from Tkinter import *
import time
import StaticMapsConnections.ImageMerge
from PIL import Image

class waitDialog(tk.Tk):

    def __init__(self, w, h, outimage, build):
        self.w = w
        self.h = h
        self.outimage = outimage
        self.build = build


    def set(self, format, *args):
        self.update()
        self.label.config(text=format % args)
        self.label.pack(in_=self.frame)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def view(self):
        im = Image.open(self.outimage)
        im.show()
        self.destroy()

    def close(self):
        self.destroy()

    def activate(self):
        tk.Tk.__init__(self)
        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill="both", expand=True)
        self.title("Please Wait")

        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.offset_x = x - (self.w // 2)
        self.offset_y = y - (self.h // 2)
        self.geometry('%sx%s+%s+%s' % (self.w, self.h, self.offset_x, self.offset_y))

        self.buttonView = tk.Button(self, text="View", bg='#4d79ff', command=self.view)
        self.buttonClose = tk.Button(self, text="Close", bg='#cc5933', command=self.close)
        self.label = tk.Label(self, text="", wrap=self.w - 10)

        self.set("We are merging the downloaded URL images now. This may take a few minutes" + "\nA button will appear for you to close this when work is done")

        # taken from the linear execution in UI
        self.images = self.build.download(self.outimage, 'image')
        self.images = StaticMapsConnections.ImageMerge.convertPtoRGB(*self.images)
        StaticMapsConnections.ImageMerge.mergeModeRGB(self.outimage, *self.images)

        self.set("Finished. \nPlease hit View to view the image, or close to continue")
        self.buttonView.pack(side=LEFT, padx = 20, pady = 3, fill = X, expand = YES)
        self.buttonClose.pack(side=RIGHT, padx = 20, pady = 3, fill = X, expand = YES)

def main(w, h):
    app = waitDialog(w, h)
    app.activate()
    app.mainloop()
    return 0

if __name__ == '__main__':
    main(350, 100)