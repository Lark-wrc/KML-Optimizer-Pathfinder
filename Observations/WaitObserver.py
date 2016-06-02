from Observer import Observer

class WaitObserver(Observer):

    def __init__(self, dialog):
        """
        `Author`: Bill Clark

        This is an extentsion of the observer class that observes the urlbuilder and imagemerge classes to report
        their status to the waitdialog. This allows for the waitdialog to trace each step of the module's iterations.

        `dialog`: The wait dialog to report to.
        """
        super(Observer, self).__init__()
        self.dialog = dialog

    def trigger(self):
        """
        `Author`: Bill Clark

        Overrides the default trigger to set the status observed to the dialog in the class.
        """
        self.dialog.set(self.status)
