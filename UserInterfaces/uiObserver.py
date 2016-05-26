from StaticMapsConnections.Observer import Observer

class UiObserver(Observer):

    def __init__(self, ui):
        """
        `Author`: Bob Seedorf

        This class observers the ui and the ui's console to allow for updates that render click-able links for the image urls

        `ui`: the instance of myFrame to which we are binding this observer

        """
        self.status = []    # list of urls needed to pass for logging
        self.count = 0
        self.new = 0
        self.ui = ui

    def trigger(self):
        """
        This method logs the appropriate state of the url list
        """
        self.ui.log_urls(self.status)

