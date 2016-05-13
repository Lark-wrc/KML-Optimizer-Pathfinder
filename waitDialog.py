import Tkinter as tk
from Tkinter import *
import time
import StaticMapsConnections.ImageMerge

class waitDialog(tk.Tk):
    def __init__(self, w, h, outimage, build):

        tk.Tk.__init__(self)
        self.outimage = outimage
        self.build = build

        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill = "both", expand=True)
        self.title("Please Wait")

        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        offset_x = x - (w // 2)
        offset_y = y - (h // 2)
        self.geometry('%sx%s+%s+%s' % (w, h, offset_x, offset_y))

        self.button = tk.Button(self, text="Close", command=self.destroy)
        self.label = tk.Label(self, text="", wrap=w-10)

        self.activate()

    def set(self, format, *args):
        self.update()
        self.label.config(text=format % args)
        self.label.pack(in_=self.frame)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def activate(self):
        self.set("We are merging the downloaded URL images now. This may take a few minutes" + "\nA button will appear for you to close this when work is done")
        time.sleep(3)

        self.images = self.build.download(self.outimage, 'image')
        self.images = StaticMapsConnections.ImageMerge.convertPtoRGB(*self.images)
        StaticMapsConnections.ImageMerge.mergeModeRGB(self.outimage, *self.images)

        self.set("Finished. \nPlease hit Close to view the image")
        self.button.pack(in_=self.frame)

def main(w, h):
    app = waitDialog(w, h)
    app.mainloop()
    return 0

if __name__ == '__main__':
    main(350, 100)