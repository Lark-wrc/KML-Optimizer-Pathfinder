
import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from GeometricDataStructures.KmlFasade import KmlFasade
from StaticMapsConnections.UrlBuilder import UrlBuilder
from RestrictionEngine.RestrictionEngine import RestrictionFactory
import StaticMapsConnections.ImageMerge as ImageMerge
# import Image

class myFrame(Frame):

    ftypes = [('KML files', '*.kml')]
    itypes = [('All files', '*'), ('PNG files', '*.png')]
    text = "testing"
    root = Tkinter.Tk()
    root.withdraw()

    # fields for user input, stored along with their respective entries
    fields = 'latitude', 'longitude', 'distance', 'size'
    entries = []

    # switch to request user input on go button
    haveReadFile = False
    haveWriteFile = False

    def __init__(self, parent):
        """
        Author: Bob Seedorf

        This is the ui interface from which a user is provided the ability to open a chosen file for processing,
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

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Save", command=self.saveFileKML)
        menubar.add_cascade(label="File", menu=fileMenu)

        for field in self.fields:
            row = Frame(self)
            label = Label(row, width=15, text=field, anchor='w')
            entry = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            label.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append((field, entry))

        go = Button(self, text = "GO.", command = self.start)
        go.pack()

        quitButton = Button(self, text = "QUIT.", command = self.onQuit)
        quitButton.pack()

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def start(self):
        """
        Author: Bob Seedorf

        This is code executes the method that runs the processing procedures of the fasade, clipper, etc.
        """

        for entry in self.entries:
            field = entry[0]
            text  = entry[1].get()
            print('%s: %s' % (field, text))
            self.txt.insert(END, '%s: %s' % (field, text))
            self.txt.insert(END, "\n")

        # class wide storage of necessary center of focus info
        self.lat = self.entries[0][1]
        self.lng = self.entries[1][1]
        self.dist = self.entries[2][1]

        self.driver()
        return

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

        file =tkFileDialog.askopenfilename(parent=self.root, filetypes=self.ftypes, title = "Open which file...")
        if file != '':
            self.infile = open(file, 'r')
            self.text = self.infile.read()

            path = os.path.split(file) [0]
            name = os.path.split(file) [1]
            pathname = path + "/" + name
            message = "Successfully read " + pathname
            print message
            self.txt.insert(END, message)
            self.txt.insert(END, "\n")
            self.haveReadFile = True
            return path
        return os.path.split(file) [0]

    def saveFileKML(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the file after processing
        :param :
        """

        file = tkFileDialog.asksaveasfilename(parent=self.root,filetypes=self.ftypes ,title="Save the file as...", defaultextension=".kml")
        if file:
            self.outfile = open(file, 'w')
            self.outfile.write(self.text)

            path = os.path.split(file) [0]
            name = os.path.split(file) [1]
            pathname = path + "/" + name
            message = "Successfully wrote to " + pathname
            print message
            self.txt.insert(END, message)
            self.txt.insert(END, "\n")
            self.haveReadFile = True
            return path
        return os.path.split(file) [0]

    def saveFileImg(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the image file after processing
        :param :
        """

        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.itypes, title="Save the file as...",
                                              defaultextension=".kml")
        if file:
            self.outimg = open(file, 'w')

            path = os.path.split(file)[0]
            name = os.path.split(file)[1]
            pathname = path + "/" + name
            message = "Successfully stored image in " + pathname
            print message
            self.txt.insert(END, message)
            self.txt.insert(END, "\n")
            return path
        return os.path.split(file) [0]

    def driver(self):
        """
        Author Bob Seedorf

        This method executes the linear code of the former driver class, uniting the runtime states of the functionality and UI
        :param arg: file to be used as read in
        :return:
        """

        # Create the KmlFasade, force user input if not read file has been selected
        if(not self.haveReadFile):
            fasade = KmlFasade(self.onOpen())
        else:
            fasade = KmlFasade(self.infile)
        fasade.placemarkToGeometrics()
        fasade.garbageFilter()
        f = RestrictionFactory()
        f = f.newSquareRestriction([float(self.lng), float(self.lat)], float(self.size))
        f.restrict(fasade.geometrics)
        fasade.fasadeUpdate()
        if (not self.haveWriteFile):
            fasade.rewrite(self.saveFileKML())
        else:
            fasade.rewrite(self.outfile)

        # Build the Url
        build = UrlBuilder(600)
        # build.centerparams('41.260352,-103.528629', '4')
        build.centerparams('%s, %s' % (self.lat, self.lng), '%s' % (self.dist))

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
            build.printUrls()

            print "Number of urls: ", len(build.urllist) + 2

            # Merge the Url Images

            # merges by downloading everything and merging everything.

            images = build.download()
            print "Downloaded."
            images = ImageMerge.convertPtoRGB(*images)
            outimage = self.saveFileImg()
            ImageMerge.mergeModeRGB(outimage, *images)

            # merges by downloading, merging, and repeating till none are left.

            # ImageMerge.debug = 0
            #
            # layers = ImageMerge.MergeGenerator('Outputs\Outfile.png', build.downloadBase())
            # for img in build.downloadGenerator():
            #     im = ImageMerge.convertPtoRGB(img)[0]
            #     layers.add(im)

            im = Image.open(outimage)
            im.show()

def main():
    """
    Author: Bob Seedorf

    Run-ME method
    param :
    """
    root= Tk()
    frame= myFrame(root)
    frame.pack()
    root.geometry("500x350+300+300")

    root.wm_protocol("WM_DELETE_WINDOW", frame.onQuit)

    root.mainloop()

if __name__ == '__main__':
    main()