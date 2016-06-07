from Observer import Observer

class UiObserver(Observer):

    def __init__(self, ui):
        """
        `Author`: Bill Clark

        An extentsion of the Observer module. This observer is used to update the UI's text log with
        the status of the observed.

        `ui`: The ui to send status updates to.
        """

        super(Observer, self).__init__()
        self.ui = ui

    def trigger(self):
        """
        `Author`: Bill Clark

        This overrides the default trigger method to send the op value and status to the ui's log method.
        The op field should contain the log tag (URLS, CONSOLE, etc) and the status is the text to be printed to the
        log.
        """
        self.ui.log(self.op, self.status)

