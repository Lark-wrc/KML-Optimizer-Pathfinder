
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

    line_count = 1                                              # count for lin e of entry in highlighting of text area
    wd = None                                                   # variable state for the wait dialog to be created and then self-destroyed
    ftypes = [('KML files', '.kml'), ('KMZ files', '.kmz')]     # default file types of kml save and open
    itypes = [('All files', '.*'), ('PNG files', '.png')]       # default file types of image saving
    init_dir = '../Inputs/KML Files/'                           # destination of local resources for file attribution
    url_doc = r"http://www.google.com"                          # resource of documentation TBD
    div_string = "=*"                                           # string to be used to 'divide' separate execs in the text area
    directions = "To Begin first select the source KML file by clicking 'Open KML.'\n\n" + "Next choose the destination to which the new KML will be saved, by clicking, 'Save KML.'\n\n" +    "Then choose the destination to which the resulting image file will be saved by clicking, 'Save Image.'\n\n" +    "If no destination file is selected, then the choice of open kml will be overwritten during operation.\n\n" +    "If neither the destination of open, or save image is chosen, the procedure will prompted you to do so.\n\n" +    "Next, input the appropriate fields to be used in the procedure;\n" +    u'\u2022' + "  Latitude of Center: latitude of center point of focused sub-portion.\n" +    u'\u2022' + "  Longitude of Center: longitude of center point of focused sub-portion.\n" +    u'\u2022' + "  Zoom: Relative level of perspective zoom, google api depenedent.\n" +    u'\u2022' + "  Image Size: distance, in miles, spanning the desired region of restriction. \n\n" +    "Finally click run, and wait as the operations are executed."

    root = Tkinter.Tk()
    root.withdraw()

    # fields for user input, stored along with their respective entries
    fields = 'Latitude of Center', 'Longitude of Center', 'Zoom Distance (1 through 20)', 'Image Size'
    entries = []
    infile = None      # destination of KML file to be read
    outfile = None     # destination of KML file to be written
    outimage = None    # destination of Image file to be read

    def __init__(self, parent):
        """
        Author: Bob Seedorf

        This is the graphic user interface of the program. The goa is to provide a user the ability to open a chosen file for processing,
        apply filters for the processing functionality, and save a processed file to a chosen location. In addition, the option to view the resulting file is allowed
        as well as repeat the procedure, with different parameters and resources, and redirect to the resulting hyper text links.

        `parent`: always tkinter's root field
        """

        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        """
        Author: Bob Seedorf

        This is the constructor for the gui which reads in and processes user input
        Using a list of 'entries', representing fields of input, and the run button, the attributed work can be executed repeatedly
        The body of the text area (self.txt), to be kn onw as the console, is used to relay to the user the results of their actions.
        Useful for debugging as well as updating interactive links used to render kml in a browser with google's api
        """

        self.parent.title("KML Klipper")
        self.pack(fill=BOTH, expand=1)
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        menubar.add_command(label="How To", command=self.howTo)             # Dialog to general directions for GUI usage
        menubar.add_command(label="Open KML", command=self.onOpen)          # choose which kml file to open
        menubar.add_command(label="Save KML", command=self.saveFileKML)     # choose where to save processed kml
        menubar.add_command(label="Save Img", command=self.saveFileImg)     # choose where to save generated image of focused region

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

        link = Label(self, text="Link To Our Py Doc", fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda url=self.url_doc: self.open_url(url))
        font = tkFont.Font(link, link.cget("font"))
        font.configure(underline=True)
        link.configure(font=font)
        link.pack(side=BOTTOM, fill=X, padx=15, pady=15)

        self.txt = ScrolledText(self, font = ("Consolas", 10))
        self.hyperlink = HyperLinkManager(self.txt)              # used for generating hyper text links that redirect the local browser to the image of the link
        self.txt.pack(fill=NONE, expand=1)

    def howTo(self):
        tkMessageBox.showinfo("How To", self.directions)

    def applyTag(self, tag, text):
        """
        Author: Bob Seedorf

        this method applies the tag configurations of the appropriate highlighting to the text area
        this process can be used to augment the console for improved interpretation of user generated procedures

        `tag`: this is the key that specifies which type of highlighting is applied to the current body of text in the console
        `text`: string to be inserted into the console
        """
        self.txt.tag_add(tag.__str__(), self.line_count.__str__() + ".0",
                         self.line_count.__str__() + "." + len(tag.__str__()).__str__())
        if tag.__str__() == 'ERROR':
            self.txt.tag_config(tag.__str__(), background="red", foreground="black")
            self.line_count += text.count('\n')
        elif tag.__str__() == 'FINISHED':
            self.txt.tag_config(tag.__str__(), background="green", foreground="black")
            self.line_count += text.count('\n')
        elif tag.__str__() == 'URLS':
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="blue")
            self.line_count += len(text) + 1
        else:
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="blue")
            self.line_count += text.count('\n')

    def log(self, tag, text):
        """
        Author: Bob Seedorf

        This method is used to update the text area of the UI with the recent input, and notifications
        NOTE the case of the tag 'URLS' implies that the parameter text is an iterable list that can be processed using the hypertext manager

        `tag`: this is the key that specifies which type of highlighting is applied to the current body of text in the console
        `text`: string to be inserted into the console
        """
        message = tag.__str__() + ": " + text.__str__()
        print message
        if tag.__str__() == 'URLS':
            self.txt.insert(END, tag.__str__() + ":\n")
            for url in text:
                self.txt.insert(END, str(url)[0:58] + "\n", self.hyperlink.add(lambda: self.open_url(str(url))))
        else:
            self.txt.insert(END, message)
        self.applyTag(tag, text)              # comment out to turn off text area highlights
        self.txt.see(END)

    def open_url(self, url):
        """
        Author: Bob Seedorf

        This method can be used to open a viable URL in a web browser

        'url': link to be opened using webbrowser package
        """
        self.log('REDIRECTING', "\nRedirecting to " + str(url) + "\n")
        webbrowser.open_new(url)

    def start(self):
        """
        Author: Bob Seedorf

        This is code executes the method that runs the processing procedures of the fasade, clipper, etc.
        This method is tied to the Run button's command
        NOTE if an interruption in execution is triggered, in the form of an exception, or error, it is caught and reported to the console for debugging
        """

        try:
            for entry in self.entries:
                field = entry[0]
                text  = entry[1].get()
                self.log("ENTRY", '%s: %s \n' % (field, text))

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

        This is code that clears the running application upon quit button
        """
        if tkMessageBox.askokcancel("Quit?", "Do you want to quit?"):
            self.master.destroy()

    def onOpen(self):
        """
        Author: Bob Seedorf

        This method will read in, at the request of the user, a file to be used for processing
        """

        # init pathname to local resource __file__ in case of erroneous choice
        myFrame.infile = os.path.join(os.path.dirname(__file__), '..')
        file =tkFileDialog.askopenfilename(parent=self.root, filetypes=self.ftypes, initialdir=self.init_dir, title = "Please choose a file to open", defaultextension='.kml')
        if file != '':
            myFrame.infile = os.path.abspath(file)
            self.log("OPEN", "Successfully chose " + myFrame.infile + "\n")
        return myFrame.infile

    def saveFileKML(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the file after processing
        """
        myFrame.outfile = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.ftypes , initialdir=self.init_dir, title="Save the file as", defaultextension='.kml')
        if file:
            myFrame.outfile = os.path.abspath(file)
            self.log("SAVE", "Successfully chose " + myFrame.infile + "\n")
        return myFrame.outfile

    def saveFileImg(self):
        """
        Author: Bob Seedorf

        This method will write, at the request of the user, the image file after processing
        """
        myFrame.outimage = os.path.join(os.path.dirname(__file__), '..')
        file = tkFileDialog.asksaveasfilename(parent=self.root, filetypes=self.itypes, initialdir=self.init_dir, title="Save the image as", defaultextension='.png')
        if file:
            myFrame.outimage = os.path.abspath(file)
            self.log("IMAGE", "Successfully chose " + myFrame.infile + "\n")
        return myFrame.outimage

    def driver(self):
        """
        Author Bob Seedorf

        This method executes the linear code of the former driver class, uniting the runtime states of the functionality and UI
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

        # CAN BE USED TO MANDATE KML DESTINATION SELECTION IF DESIRED
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
            if element.tag == "Point":
                markerlist.append(element.printCoordinates())
            if element.tag == "Polygon":
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

        self.log("FINISHED", "\n" + str("-" * ((58/len("-"))+1))[:58] + "\n")

def main(w, h):
    """
    Author: Bob Seedorf

    Run-Me method to start application

    `w`: desired width of app window
    `h`: desired width of app window
    """
    root= Tk()
    frame= myFrame(root)
    frame.pack()
    offset_x, offset_y = center(root, w, h)
    # find the center of the screen and then offset to open window at middle
    root.geometry('%sx%s+%s+%s' % (w, h, offset_x, offset_y))
    root.wm_protocol("WM_DELETE_WINDOW", frame.onQuit)
    root.mainloop()

def center(root, w, h):
    """
    Author: Bob Seedorf

    find the center of the screen and then offset to open window at middle

    `root`: 'screen' resource in which application is to be rendered
    `w`: desired width of app window
    `h`: desired width of app window
    `offset_x, offset_y': return values for coordinate of beginning point of render (top left most corner) of frame
    """
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    offset_x = x - (w // 2)
    offset_y = y - (h // 2)
    return offset_x, offset_y

if __name__ == '__main__':
    main(550, 550)