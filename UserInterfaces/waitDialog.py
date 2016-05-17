import Tkinter as tk
from Tkinter import *
import time

class SampleApp(tk.Tk):
    def __init__(self, w, h):
        tk.Tk.__init__(self)
        self.frame = tk.Frame(self)
        self.frame.pack(side="top", fill = "both", expand=True)
        self.title("Please Wait")

        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        offset_x = x - (w // 2)
        offset_y = y - (h // 2)
        self.geometry('%sx%s+%s+%s' % (w, h, offset_x, offset_y))

        self.button = tk.Button(self, text="Continue", command=self.destroy)
        self.label = tk.Label(self, text="", wrap=w-10)

        self.activate()

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.pack(in_=self.frame)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def activate(self):
        self.update()
        self.set("We are merging the downloaded URL images now. This may take a few minutes" + "\nA button will appear for you to close this when work is done")
        #
        # RUN CODE HERE
        #
        time.sleep(2)
        self.set("Done. \nPlease hit close to view the image")
        self.button.pack(in_=self.frame)

def main(w, h):
    app = SampleApp(w, h)
    app.mainloop()
    return 0

if __name__ == '__main__':
    main(350, 100)