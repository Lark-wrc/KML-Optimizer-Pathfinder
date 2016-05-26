from StaticMapsConnections.Observer import Observer

class UiObserver(Observer):

    def __init__(self, text):
        self.status = []
        self.count = 0
        self.new = 0
        self.text = text

    def trigger(self):
        self.text.log("URLS", self.status)

