import Tkinter
from Tkinter import *
import webbrowser
import codecs
import tkFileDialog
import tkMessageBox
import os
import waitDialog
import traceback
import tkFont

import Console
from WaitObserver import WaitObserver

class myFrame(Frame):

    line_count = 1                                              # count for line of entry in highlighting of text area
    wd = None                                                   # variable state for the wait dialog to be created and then self-destroyed
    ftypes = [('KML files', '.kml')]     # default file types of kml save and open
    itypes = [('All files', '.*'), ('PNG files', '.png')]       # default file types of image saving
    init_dir = '../Inputs/KML Files/'                           # destination of local resources for file attribution
    url_doc = r"http://www.google.com"                          # resource of documentation TBD
    div_string = ("_", 2048)                                     # string to be used to 'divide' separate execs in the text area, with length as width
    hypkey = 'hyper'                                            # USed by hyper text capabilities to add clickable links to console
    console_font_size = 8                                       # size of text for console
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
        self.wd = None              # field to use for wait dialog when necessary
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
        self.run = Button(row, width = 20, text = "RUN", command = self.start, bg = '#59cc33')
        self.quit = Button(row, width = 20, text = "QUIT", command = self.onQuit, bg = '#cc5933')
        row.pack(side=TOP, fill=X, padx=15, pady=15)
        self.run.pack(side=LEFT, expand = YES)
        self.quit.pack(side=RIGHT, expand=YES)
        label = Label(self, text = "Output:")
        label.pack()

        link = Label(self, text="Link To Our Py Doc", fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda url=self.url_doc: self.open_url(url))
        font = tkFont.Font(link, link.cget("font"))
        font.configure(underline=True)
        link.configure(font=font)
        link.pack(side=BOTTOM, fill=X, padx=15, pady=15)

        self.txt = Text(self, font = ("Consolas", self.console_font_size), wrap = NONE)
        self.txt.pack(fill=BOTH, expand=True)

        # configure console for scrolling on entries
        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        yscrollbar = Scrollbar(self.txt)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar.config(command=self.txt.xview)
        yscrollbar.config(command=self.txt.yview)

        # configure tags for blue links in the console
        self.txt.tag_config(self.hypkey, foreground="blue", underline=1)
        self.txt.tag_bind(self.hypkey, "<Enter>", self.enter)
        self.txt.tag_bind(self.hypkey, "<Leave>", self.leave)
        self.txt.tag_bind(self.hypkey, "<Button-1>", self.click)
        self.links = {}

    def howTo(self):
        """
        This method reads and renders the dialog with the 'how to' text for the user to read

        """
        directions = []
        with open ("../how_to.txt", "r") as file:
            for line in file.readlines():
                directions.append(line)
        directions = ''.join(directions)
        tkMessageBox.showinfo("How To", directions)

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
            for line in text.splitlines():
                self.txt.tag_add(tag.__str__(), self.line_count.__str__() + ".0",
                                  self.line_count.__str__() + "." + len(line.__str__()).__str__())
                self.line_count += 1
            self.txt.tag_config(tag.__str__(), background="#ffb3b3", foreground="black")
        elif tag.__str__() == 'FINISHED':
            self.txt.tag_config(tag.__str__(), background="green", foreground="black")
            self.line_count += text.count('\n')
        elif tag.__str__() == 'URLS':
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="#004d1a")
            self.line_count += len(text) + 1
        else:
            self.txt.tag_config(tag.__str__(), background="yellow", foreground="#004d1a")
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
                self.txt.insert(END, str(url) + "\n", self.add_hyper(lambda link=url: self.open_url(str(link))))
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
            self.zoom = int(self.entries[2][1].get())
            self.size = int(self.entries[3][1].get())

            self.interfaceConsole()
            self.run.config(state=NORMAL)

        except:
            self.run.config(state=NORMAL)
            e = sys.exc_info()
            tb = traceback.format_exc()
            self.log("ERROR", "\n" + str(e) + str(tb) + "\n")
            if self.wd != None:
                self.wd.set("An error has occurred.\nPlease close this dialog to continue.")

    def onQuit(self):
        """
        Author: Bob Seedorf

        This is code that clears the running application upon quit button
        """
        if tkMessageBox.askokcancel("Quit?", "Do you want to quit?"):
            self.master.destroy()
            raise SystemExit

    def enter(self, event):
        """
        this method changes the configuration of the cursor over the hypertext links upon hover

        `event`: the action of the cursor's movement over the text
        """
        self.txt.config(cursor="hand2")

    def leave(self, event):
        """
        this method changes the configuration of the cursor over the hypertext links upon hover

        `event`: the action of the cursor's movement off the text
        """
        self.txt.config(cursor="")

    def click(self, event):
        """
        this method allows the links to e used as urls

        `event`: click action
        """
        for tag in self.txt.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

    def add_hyper(self, action):
        """
        This method adds the links to a list so that their reference is stable for future use

        `action` : the method desired to be used upon event with the action, must be callable
        """
        tag = self.hypkey + '-%d' % len(self.links)
        self.links[tag] = action
        return "hyper", tag

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

    def interfaceConsole(self):
        lat = self.lat
        lng = self.lng
        zoom = self.zoom
        size = self.size

        if myFrame.infile is None:
            tkMessageBox.showwarning("Open file", "Please Choose A KML file to Open")
            infile = self.onOpen()
        else:
            infile = myFrame.infile
        if myFrame.outimage is None:
            tkMessageBox.showwarning("Write Img file", "Please Choose an image file to write to")
            outimage = self.saveFileImg()
        else:
            outimage = myFrame.outimage
        if (myFrame.outfile is None):
            tkMessageBox.showwarning("Write KML file", "Please Choose A KML file to write to")
            outfile = self.saveFileKML()
        else:
            outfile = myFrame.outfile

        # if ' ' in infile: infile = '"'+infile+'"'
        # if ' ' in outimage: outimage = '"'+outimage+'"'
        # if ' ' in outfile: outfile = '"'+outfile+'"'


        sampleLine = """-wa -w {} -m {} -v -z {} -c {},{} -s {} {}""".format(outfile,
            outimage, repr(zoom), repr(lat), repr(lng), repr(size), infile)
        args = ['-wa', '-w', outfile, '-m', outimage, '-v', '-z', repr(zoom),
                '-c', repr(lat)+','+ repr(lng), '-s', repr(size), infile]


        self.run.config(state=DISABLED)
        self.wd = waitDialog.waitDialog(350, 100, myFrame.outimage)
        self.wd.activate()  # call activate in waitDialog to process image downloads
        imobserver = WaitObserver(self.wd)
        urlobserver = WaitObserver(self.wd)
        Console.interface(args, imobserver, urlobserver)
        self.wd.end()
        self.log("FINISHED", "\n" + str(self.div_string[0] * ((self.div_string[1]/len(self.div_string[0]))+1))[:self.div_string[1]] + "\n")
        self.run.config(state=NORMAL)

    # def driver(self):
    #     """
    #     Author Bob Seedorf
    #
    #     This method executes the linear code of the former driver class, uniting the runtime states of the functionality and UI
    #     """
    #
    #     # Create the KmlFasade, force user input if not read file has been selected
    #     if myFrame.infile is None:
    #         tkMessageBox.showwarning("Open file", "Please Choose A KML file to Open")
    #         fasade = KmlFasade(self.onOpen())
    #     else:
    #         fasade = KmlFasade(myFrame.infile)
    #
    #     merc = MercatorProjection()
    #     centerPoint = LatLongPoint(self.lat, self.lng)
    #     f = RestrictionFactory()
    #
    #     clipped = f.newWAClipping(merc.get_corners(centerPoint, self.zoom, self.size, self.size))
    #     fasade.placemarkToGeometrics()
    #     fasade.removeGarbageTags()
    #
    #     clipped.restrict(fasade.geometrics)
    #     fasade.fasadeUpdate()
    #
    #     # CAN BE USED TO MANDATE KML DESTINATION SELECTION IF DESIRED
    #     # code to indicate the user has not chosen an output kml and then requests one
    #     # if (myFrame.outfile is None):
    #     #     tkMessageBox.showwarning("Write KML file", "Please Choose A KML file to write to")
    #     #     fasade.rewrite(self.saveFileKML())
    #     # else:
    #     #     fasade.rewrite(myFrame.outfile)
    #
    #     # Build the Url
    #     build = UrlBuilder(600)
    #     build.centerparams('%s,%s' % (self.lat, self.lng), repr(self.zoom))
    #
    #     markerlist = []
    #     for element in fasade.geometrics:
    #         if element.tag == "Point":
    #             markerlist.append(element.printCoordinates())
    #         if element.tag == "Polygon":
    #             build.addpath({"color": "red", "weight": '5'}, element.coordinatesAsListStrings())
    #         if element.tag == "LineString":
    #             build.addpath({"color": "blue", "weight": '5'}, element.coordinatesAsListStrings())
    #
    #     build.addmarkers({"color": "blue"}, markerlist)
    #     self.log("URLS", build.printUrls())
    #
    #     if myFrame.outimage is None:
    #         tkMessageBox.showwarning("Write Img file", "Please Choose an image file to write to")
    #         myFrame.outimage = self.saveFileImg()
    #
    #     # Merge the Url Images
    #     # merges by downloading everything and merging everything.
    #     self.run.config(state=DISABLED)
    #     self.wd = waitDialog.waitDialog(350, 100, myFrame.outimage, build)
    #     self.wd.activate()  # call activate in waitDialog to process image downloads
    #     self.log("FINISHED", "\n" + str(self.div_string[0] * ((self.div_string[1]/len(self.div_string[0]))+1))[:self.div_string[1]] + "\n")
    #     self.run.config(state=NORMAL)

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
    root.wm_protocol("WM_DEICONIFY")
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