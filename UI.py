
import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import os
from GeometricDataStructures.KmlFasade import KmlFasade
from StaticMapsConnections.UrlBuilder import UrlBuilder
from RestrictionEngine.RestrictionEngine import RestrictionFactory
import StaticMapsConnections.ImageMerge as ImageMerge
from PIL import Image

class myFrame(Frame):

    ftypes = [('KML files', '*.kml'), ('KMZ files', '*.kmz'), ('All files', '*')]
    itypes = [('All files', '*'), ('PNG files', '*.png')]
    text = "KML Klipper"
    root = Tkinter.Tk()
    root.withdraw()

    # fields for user input, stored along with their respective entries
    fields = 'Latitude of Center', 'Longitude of Center', 'Zoom Distance (1 through 20)', 'Image Size'
    entries = []

    def __init__(self, parent):
        """
        Author: Bob Seedorf

        This is the user interface from which a user is provided the ability to open a chosen file for processing,
        apply filters for the processing functionality, and save a processed file to a location
        :param parent:
        """

        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

        # switch to request user input on go button
        self.infile = None
        self.outfile = None

    def initUI(self):
        """
        Author: Bob Seedorf

        This is the constructor for the ui which reads in and processes user input
        """

        self.parent.title("Visual-Ice")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        menubar.add_command(label="Open", command=self.onOpen)
        menubar.add_command(label="Save", command=self.saveFileKML)

        for field in self.fields:
            row = Frame(self)
            label = Label(row, width=30, text=field, anchor='w')
            entry = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            label.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append((field, entry))

        row = Frame(self)
        go = Button(row, width = 20, text = "RUN", command = self.start, bg = '#59cc33')
        quitButton = Button(row, width = 20, text = "QUIT", command = self.onQuit, bg = '#cc5933')
        row.pack(side=TOP, fill=X, padx=15, pady=15)
        go.pack(side=LEFT, expand = YES)
        quitButton.pack(side=RIGHT, expand=YES)

        label = Label(self, text = "Output:")
        label.pack()

        self.txt = ScrolledText(self)
        self.txt.pack(fill=NONE, expand=1)

    def log(self, text):
        """
        This method is used to update the text area of the UI with the recent input, and notifications
        :param text:
        :return:
        """
        print text
        self.txt.insert(END, text.__str__() + "\n")

    def start(self):
        """
        Author: Bob Seedorf

        This is code executes the method that runs the processing procedures of the fasade, clipper, etc.
        """

        for entry in self.entries:
            field = entry[0]
            text  = entry[1].get()
            self.log('%s: %s' % (field, text))

        # class wide storage of necessary center of focus info
        self.lat = float(self.entries[0][1].get())
        self.lng = float(self.entries[1][1].get())
        self.dist = float(self.entries[2][1].get())
        self.size = float(self.entries[3][1].get())

        self.driver()

    def onQuit(self):
        """
        Author: Bob Seedorf

        This is code that clears the running application upon  quit button
        """
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def onOpen(self):
        """
        Author: Bob Seedorf

        This method will read in, at the request of the user, a file to be used for processing
        :param :
        """

    # init pathname to local resource __file__ in case of erroneous choice
        pathname = os.path.join(os.path.dirname(__file__), '..')
        file =tkFileDialog.askopenfilename(parent=self.root, filetypes=self.ftypes, title = "Please choose a file to open", defaultextension=".kml")
        if file != '':
            pathname = os.path.abspath(file)
            message = "OPEN: Successfully chose " + pathname
            self.log(message)
        return pathname

    def saveFileKML(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the file after processing
        :param :
        """
        pathname = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root,filetypes=self.ftypes ,title="Save the file as", defaultextension=".kml")
        if file:
            pathname = os.path.abspath(file)
            message = "SAVE: Successfully chose " + pathname
            self.log(message)
        return pathname

    def saveFileImg(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the image file after processing
        :param :
        """
        pathname = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.itypes, title="Save the image as", defaultextension=".png")
        if file:
            pathname = os.path.abspath(file)
            message = "IMAGE: Successfully stored image in " + pathname
            self.log(message)
        return pathname

    def driver(self):
        """
        Author Bob Seedorf

        This method executes the linear code of the former driver class, uniting the runtime states of the functionality and UI
        :param arg: file to be used as read in
        :return:
        """

        # Create the KmlFasade, force user input if not read file has been selected
        if(self.infile is None):
            tkMessageBox.showwarning("Open file", "Please Choose A KML file to Open")
            fasade = KmlFasade(self.onOpen())
        else:
            fasade = KmlFasade(self.infile)

        fasade.placemarkToGeometrics()
        fasade.garbageFilter()
        f = RestrictionFactory()
        f = f.newSquareRestriction([self.lng, self.lat], self.size)
        f.restrict(fasade.geometrics)
        fasade.fasadeUpdate()

        # code to indicate the user has not chosen an output kml and then requests one
        # if (self.outfile is None):
        #     tkMessageBox.showwarning("Write KML file", "Please Choose A KML file to write to")
        #     fasade.rewrite(self.saveFileKML())
        # else:
        #     fasade.rewrite(self.outfile)

        # Build the Url
        build = UrlBuilder(600)
        build.centerparams('%s,%s' % (self.lat, self.lng), '%s' % (self.dist))

        markerlist = []
        for element in fasade.geometrics:
            element.switchCoordinates()
            # print element.printCoordinates()
            if element.tag == "Point":
                markerlist.append(element.printCoordinates())
            if element.tag == "Polygon":
                # markerlist = element.coordinatesAsList()
                build.addpath({"color": "red", "weight": '5'}, element.coordinatesAsListStrings())
            if element.tag == "LineString":
                build.addpath({"color": "blue", "weight": '5'}, element.coordinatesAsListStrings())

        build.addmarkers({"color": "blue"}, markerlist)
        self.log(build.printUrls())

        message = "Number of urls: ", len(build.urllist) + 2
        self.log(message)

        # Merge the Url Images
        # merges by downloading everything and merging everything.
        tkMessageBox.showwarning("Write Img file", "Please Choose A png file to write to")
        outimage = self.saveFileImg()
        images = build.download(outimage, 'image')
        self.log("Downloaded.")
        images = ImageMerge.convertPtoRGB(*images)
        ImageMerge.mergeModeRGB(outimage, *images)

        self.log("Opening, " + outimage)
        im = Image.open(outimage)
        im.show()
        self.log("\nFinished\n--------------------\n")


def main(w, h):
    """
    Author: Bob Seedorf

    Run-ME method
    param :
    """
    root= Tk()
    frame= myFrame(root)
    frame.pack()

    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    offset_x = x - (w // 2)
    offset_y = y - (h // 2)
    root.geometry('%sx%s+%s+%s' % (550, 550, offset_x, offset_y))

    root.wm_protocol("WM_DELETE_WINDOW", frame.onQuit)
    root.mainloop()

if __name__ == '__main__':
    main(550, 550)