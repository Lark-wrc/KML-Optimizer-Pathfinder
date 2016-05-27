from Observer import Observer

class WaitObserver(Observer):

    def __init__(self, dialog):
        super(Observer, self).__init__()
        self.dialog = dialog

    def trigger(self):
        self.dialog.set(self.status)
