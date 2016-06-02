from Observer import Observer

class WaitObserver(Observer):

    def __init__(self, dialog):
        super(Observer, self).__init__()
        self.dialog = dialog

    def trigger(self):
        """
        This method logs the appropriate state of a message to the wait dialog box
        """
        self.dialog.set(self.status)
