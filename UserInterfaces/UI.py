
import Tkinter
from Tkinter import *
import webbrowser
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import os
from GeometricDataStructures.KmlFasade import KmlFasade
from StaticMapsConnections.UrlBuilder import UrlBuilder
from RestrictionEngine.RestrictionEngine import RestrictionFactory
import StaticMapsConnections
import waitDialog
import traceback
import tkFont
from UserInterfaces.HyperLinkManager import HyperLinkManager
from GeometricDataStructures.Mercator import *

class myFrame(Frame):

    line_count = 1
    wd = None
    ftypes = [('KML files', '*.kml'), ('KMZ files', '*.kmz'), ('All files', '*')]
    itypes = [('All files', '*'), ('PNG files', '*.png')]
    sample_input = '../Inputs/KML Files/'
    text = "KML Klipper"
    root = Tkinter.Tk()
    root.withdraw()

    # fields for user input, stored along with their respective entries
    fields = 'Latitude of Center', 'Longitude of Center', 'Zoom Distance (1 through 20)', 'Image Size'
    entries = []
    infile = None
    outfile = None
    outimage = None
    url_doc = r"http://www.google.com"      # change to destination of documentation

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

    def initUI(self):
        """
        Author: Bob Seedorf

        This is the constructor for the ui which reads in and processes user input
        """

        self.parent.title("Visual-Ice")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        menubar.add_command(label="Open KML", command=self.onOpen)
        menubar.add_command(label="Save KML", command=self.saveFileKML)
        menubar.add_command(label="Save Img", command=self.saveFileImg)

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
        link = Label(self, text="Link To Our Py Doc", fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e, url=self.url_doc: self.open_url(url))
        font = tkFont.Font(link, link.cget("font"))
        font.configure(underline=True)
        link.configure(font=font)
        row.pack(side=TOP, fill=X, padx=15, pady=15)
        go.pack(side=LEFT, expand = YES)

        quitButton.pack(side=RIGHT, expand=YES)
        link.pack(side=BOTTOM, fill=X, padx=15, pady=15)

        label = Label(self, text = "Output:")
        label.pack()

        self.txt = ScrolledText(self)
        self.hyperlink = HyperLinkManager(self.txt)
        self.txt.pack(fill=NONE, expand=1)

    def applyTag(self, tag, text):
        self.txt.tag_add(tag.__str__(), self.line_count.__str__() + ".0",
                         self.line_count.__str__() + "." + len(tag.__str__()).__str__())
        if tag.__str__() == 'ERROR':
            self.txt.tag_config(tag.__str__(), background="red", foreground="black")
            self.line_count += 5
        elif tag.__str__() == 'FINISHED':
            self.txt.tag_config(tag.__str__(), background="green", foreground="black")
            self.line_count += 2
        elif tag.__str__() == 'URLS':
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="blue")
            self.line_count += len(text) + 1
        else:
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="blue")
            self.line_count += 1

    def log(self, tag, text):
        """
        This method is used to update the text area of the UI with the recent input, and notifications
        :param: tag
        :param: text
        :return:
        """
        message = tag.__str__() + ": " + text.__str__()
        print message
        if tag.__str__() == 'URLS':
            self.txt.insert(END, tag.__str__() + ":\n")
            for url in text:
                self.txt.insert(END, str(url)[0:65] + "\n", self.hyperlink.add(lambda: self.open_url(str(url))))
        else:
            self.txt.insert(END, message)
        self.applyTag(tag, text)              # comment out to turn off text area highlights
        self.txt.see(END)

    def open_url(self, url):
        self.log('REDIRECTING', "redirecting to " + str(url) + "\n")
        webbrowser.open_new(url)

    def start(self):
        """
        Author: Bob Seedorf

        This is code executes the method that runs the processing procedures of the fasade, clipper, etc.
        """

        try:
            for entry in self.entries:
                field = entry[0]
                text  = entry[1].get()
                self.log("ENTRY", '%s: %s' % (field, text))

            # class wide storage of necessary center of focus info
            self.lat = float(self.entries[0][1].get())
            self.lng = float(self.entries[1][1].get())
            self.dist = float(self.entries[2][1].get())
            self.size = float(self.entries[3][1].get())

            self.driver()
        except:
            e = sys.exc_info()
            tb = traceback.format_exc()
            self.log("ERROR", str(e) + str(tb) + "\n")
            if StaticMapsConnections.ImageMerge.wd != None:
                StaticMapsConnections.ImageMerge.wd.set("An error has occurred.\nPlease close this dialog to continue.")


    def onQuit(self):
        """
        Author: Bob Seedorf

        This is code that clears the running application upon  quit button
        """
        if tkMessageBox.askokcancel("Quit?", "Do you want to quit?"):
            self.master.destroy()

    def onOpen(self):
        """
        Author: Bob Seedorf

        This method will read in, at the request of the user, a file to be used for processing
        :param :
        """

    # init pathname to local resource __file__ in case of erroneous choice
        myFrame.infile = os.path.join(os.path.dirname(__file__), '..')
        file =tkFileDialog.askopenfilename(parent=self.root, filetypes=self.ftypes, initialdir=self.sample_input, title = "Please choose a file to open", defaultextension=".kml")
        if file != '':
            myFrame.infile = os.path.abspath(file)
            self.log("OPEN", "Successfully chose" + myFrame.infile + "\n")
        return myFrame.infile

    def saveFileKML(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the file after processing
        :param :
        """
        myFrame.outfile = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.ftypes , initialdir=self.sample_input, title="Save the file as", defaultextension=".kml")
        if file:
            myFrame.outfile = os.path.abspath(file)
            self.log("SAVE", "Successfully chose" + myFrame.infile + "\n")
        return myFrame.outfile

    def saveFileImg(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the image file after processing
        :param :
        """
        myFrame.outimage = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.itypes, initialdir=self.sample_input, title="Save the image as", defaultextension=".png")
        if file:
            myFrame.outimage = os.path.abspath(file)
            self.log("IMAGE", "Successfully chose" + myFrame.infile + "\n")
        return myFrame.outimage

    def driver(self):
        """
        Author Bob Seedorf

        This method executes the linear code of the former driver class, uniting the runtime states of the functionality and UI
        :param arg: file to be used as read in
        :return:
        """

        # Create the KmlFasade, force user input if not read file has been selected
        if myFrame.infile is None:
            tkMessageBox.showwarning("Open file", "Please Choose A KML file to Open")
            fasade = KmlFasade(self.onOpen())
        else:
            fasade = KmlFasade(myFrame.infile)

        merc = MercatorProjection()
        centerPoint = LatLongPoint(self.lat, self.lng)
        f = RestrictionFactory()

        clipped = f.newWAClipping(merc.get_corners(centerPoint, self.dist, self.size, self.size))
        fasade.placemarkToGeometrics()
        fasade.removeGarbageTags()

        clipped.restrict(fasade.geometrics)
        fasade.fasadeUpdate()

        # code to indicate the user has not chosen an output kml and then requests one
        # if (myFrame.outfile is None):
        #     tkMessageBox.showwarning("Write KML file", "Please Choose A KML file to write to")
        #     fasade.rewrite(self.saveFileKML())
        # else:
        #     fasade.rewrite(myFrame.outfile)

        # Build the Url
        build = UrlBuilder(600)
        build.centerparams('%s,%s' % (self.lat, self.lng), '%s' % (self.dist))

        markerlist = []
        for element in fasade.geometrics:
            # element.switchCoordinates()
            # print element.printCoordinates()
            if element.tag == "Point":
                markerlist.append(element.printCoordinates())
            if element.tag == "Polygon":
                # markerlist = element.coordinatesAsList()
                build.addpath({"color": "red", "weight": '5'}, element.coordinatesAsListStrings())
            if element.tag == "LineString":
                build.addpath({"color": "blue", "weight": '5'}, element.coordinatesAsListStrings())

        build.addmarkers({"color": "blue"}, markerlist)
        self.log("URLS", build.printUrls())

        if myFrame.outimage is None:
            tkMessageBox.showwarning("Write Img file", "Please Choose an image file to write to")
            myFrame.outimage = self.saveFileImg()

        # Merge the Url Images
        # merges by downloading everything and merging everything.
        StaticMapsConnections.ImageMerge.wd = waitDialog.waitDialog(350, 100, myFrame.outimage, build)
        StaticMapsConnections.ImageMerge.wd.activate()  # call activate in waitDialog to process image downloads

        self.log("FINISHED", "\n------------------------------------------------------------\n")

def main(w, h):
    """
    Author: Bob Seedorf

    Run-Me method
    param :
    """
    root= Tk()
    frame= myFrame(root)
    frame.pack()

    # find the center of the screen and then offset to open window at middle
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    offset_x = x - (w // 2)
    offset_y = y - (h // 2)
    root.geometry('%sx%s+%s+%s' % (550, 550, offset_x, offset_y))

    root.wm_protocol("WM_DELETE_WINDOW", frame.onQuit)
    root.mainloop()

if __name__ == '__main__':
    main(550, 550)