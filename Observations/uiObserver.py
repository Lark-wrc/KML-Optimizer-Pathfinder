from Observer import Observer

class UiObserver(Observer):

    def __init__(self, ui):

        super(Observer, self).__init__()
        self.ui = ui

    def trigger(self):
        """
        This method logs the appropriate state of the url list
        """
        self.ui.log(self.op, self.status)

