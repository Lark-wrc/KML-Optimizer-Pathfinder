from StaticMapsConnections.Observer import Observer

class WaitObserver(Observer):

    def __init__(self, dialog):
        self.status = ''
        self.count = 0
        self.new = 0
        self.dialog = dialog

    def trigger(self):
        self.dialog.set(self.status)