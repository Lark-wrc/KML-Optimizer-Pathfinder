from Observer import Observable


class ObservableConsole(Observable):

    def __init__(self):
        """
        `Author`: Bill Clark

        An observable extension used to observe our console module. Any logging or debugging information is sent to
        the setStatus method from the Console. string contains the text to print, and op is an optional argument.
        The op value for the console is the identifier to use in the text UI. URLS, CONSOLE, etc.
        """
        super(ObservableConsole, self).__init__()

    def setStatus(self, string, op=None):
        """
        `Author`: Bill Clark

        Overrides the setStatus method from Observable.

        `string`: The text to set Observable's status to.

        `op`: The UI printing tag to be used.
        """
        if self.observers:
            super(ObservableConsole, self).setStatus(string, op)
        else:
            print string
