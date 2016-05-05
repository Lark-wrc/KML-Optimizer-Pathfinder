
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Tkinter, Tkconstants
import os

class Example(Frame):

    ftypes = [('KML files', '*.kml'), ('All files', '*')]
    text = "testing"
    root = Tkinter.Tk()
    root.withdraw()

    fields = 'latitude', 'longitude', 'distance'
    entries = []

    def __init__(self, parent):
        """
        Author: Bob Seedorf

        This is the ui interface from which a user is provided the ability to open a chosen file for processing,
        apply filters fo rth proccessing functionality, and save a processed file to a location
        :param parent:
        """

        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        """
        Author: Bob Seedorf

        This is the constructor for the ui which reads in and processes user input
        :param :
        """

        self.parent.title("Visual-Ice")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Save", command=self.saveFile)
        menubar.add_cascade(label="File", menu=fileMenu)

        for field in self.fields:
            row = Frame(self)
            lable = Label(row, width=15, text=field, anchor='w')
            entry = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lable.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append((field, entry))

        go = Button(self, text = "GO.", command = self.start)
        go.pack()

        quitButton = Button (self, text = "QUIT.", command = self.onQuit).pack()
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def start(self):
        """
        Author: Bob Seedorf

        This is code executes the method that runs the processing procedures of the fasade, etc.
        :param :
        """

        for entry in self.entries:
            field = entry[0]
            text  = entry[1].get()
            print('%s: "%s"' % (field, text))
            self.txt.insert(END, '%s: "%s"' % (field, text))
            self.txt.insert(END, "\n")

        #TODO add call to method which connects process

    def onQuit(self):
        """
        Author: Bob Seedorf

        This is code that clears the running application upon  quit button
        :param :
        """
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()


    def onOpen(self):
        """
        Author: Bob Seedorf
        Version = 1.0
        This method will read in, at the request of the user, a file to be used for processing
        :param :
        """

        file =tkFileDialog.askopenfilename(parent=self.root, filetypes=self.ftypes, title = "Open which file...")
        if file != '':
            infile = open(file, 'r')
            self.text = infile.read()

            path = os.path.split(file) [0]
            name = os.path.split(file) [1]
            pathname = path + "/" + name
            message = "Successfuly read " + pathname
            print message
            self.txt.insert(END, message)
            self.txt.insert(END, "\n")
            return
        return

    def saveFile(self):
        """
        Author: Bob Seedorf
        Version = 1.0
        This method will wirte, at the requst of the user, the file after porcessing
        :param :
        """

        file = tkFileDialog.asksaveasfilename(parent=self.root,filetypes=self.ftypes ,title="Save the file as...", defaultextension=".kml")
        if file:
            outfile = open(file, 'w')
            outfile.write(self.text)

            path = os.path.split(file) [0]
            name = os.path.split(file) [1]
            pathname = path + "/" + name
            message = "Successfuly wrote to " + pathname
            print message
            self.txt.insert(END, message)
            self.txt.insert(END, "\n")
            return
        return

def main():
    """
    Author: Bob Seedorf
    Version = 1.0
    This is the comment
    param :
    """
    root= Tk()
    frame= Example(root)
    frame.pack()
    root.geometry("500x350+300+300")

    root.wm_protocol("WM_DELETE_WINDOW", frame.onQuit)

    root.mainloop()


if __name__ == '__main__':
    main()