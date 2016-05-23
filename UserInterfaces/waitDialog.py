import Tkinter as tk
from Tkinter import *
import StaticMapsConnections.ImageMerge
from PIL import Image
import UI

class waitDialog(tk.Tk):

    def __init__(self, w, h, outimage, build):
        """
        This class encapsulates the functionality of the dialog box, specially designed to inform the user to wait during extended execution.
        Its job also serves to update the text of dialog as the execution of persitently extended work
        `w`: desired width of app window
        `h`: desired width of app window
        `outimage`: destination of resultant image required to be oriented here to ensure updates are recorded
        `build`: state or URL builder required to be here as it is essential to execution of image downloading
        """
        self.w = w
        self.h = h
        self.outimage = outimage
        self.build = build

    def set(self, format, *args):
        """
        This method sets the field of the display to the value of args

        `format`: layout of text to be prefaced in the display of the dialog
        `args`: string value to be displayed by dialog
        """
        self.update()
        self.label.config(text=format % args)
        self.label.pack(in_=self.frame)
        self.label.update_idletasks()

    def clear(self):
        """
        This method clears the display of all text

        :return:
        """
        self.label.config(text="")
        self.label.update_idletasks()

    def view(self):
        """
        This method allows to illustration of an image in the dialog

        """
        im = Image.open(self.outimage)
        im.show()
        self.destroy()

    def close(self):
        """
        This method closes this dialog instance

        """
        self.destroy()

    def activate(self):
        """
        This method executes all of the essential code rewuired to beexecuted, in sequence, and in tandem with the UI driver

        """
        # first render this window as the foremost visual element
        tk.Tk.__init__(self)
        self.frame = tk.Frame(self)
        self.frame.pack(padx = 0, pady = 0, fill="both", expand=True)
        self.title("Please Wait")

        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.offset_x = x - (self.w // 2)
        self.offset_y = y - (self.h // 2)
        self.geometry('%sx%s+%s+%s' % (self.w, self.h, self.offset_x, self.offset_y))

        # generate buttons to be used as View and Close
        self.buttonView = tk.Button(self, text="View", bg='#4d79ff', command=self.view)
        self.buttonClose = tk.Button(self, text="Close", bg='#cc5933', command=self.close)
        self.label = tk.Label(self, text="", padx = 5, pady = 5, wrap=self.w - 10)

        self.set("We are merging the downloaded URL images now. This may take a few minutes" + "\nA button will appear for you to close this when work is done")

        # taken from the linear execution in UI
        # first download URLS, then Image merge all of the images, finally then merge the results
        self.images = self.build.download(self.outimage, 'image')
        self.images = StaticMapsConnections.ImageMerge.convertPtoRGB(*self.images)
        StaticMapsConnections.ImageMerge.mergeModeRGB(self.outimage, *self.images)

        self.set("Finished. \nPlease hit View to view the image, or close to continue")
        self.buttonView.pack(side=LEFT, padx = 15, pady = 3, fill = BOTH, expand = YES)
        self.buttonClose.pack(side=RIGHT, padx = 15, pady = 3, fill = BOTH, expand = YES)

def main(w, h):
    """
    This method generates the dialog body, the rendering is done via the activate method
    CANNOT BE USED INDEPENDENT OF UI DRIVER

    `w`: desired width of app window
    `h`: desired width of app window
    """
    app = waitDialog(w, h)
    app.activate()
    app.mainloop()
    return 0

if __name__ == '__main__':
    main(350, 200)