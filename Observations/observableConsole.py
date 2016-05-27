from Observer import Observable


class ObservableConsole(Observable):

    def __init__(self):
        super(ObservableConsole, self).__init__()

    def setStatus(self, string, op=None):
        if self.observers:
            super(ObservableConsole, self).setStatus(string, op)
        else:
            print string
