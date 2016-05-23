from Tkinter import *

class HyperLinkManager:
    """
    This code has been adapted from effbot.org
    src: http://effbot.org/zone/tkinter-text-hyperlink.htm
    """

    def __init__(self, text):

        self.title = 'hyper'
        self.text = text
        self.text.tag_config(self.title, foreground="blue", underline=1)
        self.text.tag_bind(self.title, "<Enter>", self._enter)
        self.text.tag_bind(self.title, "<Leave>", self._leave)
        self.text.tag_bind(self.title, "<Button-1>", self._click)
        self.links = {}

    def add(self, action):
        tag = self.title + '-%d' % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return