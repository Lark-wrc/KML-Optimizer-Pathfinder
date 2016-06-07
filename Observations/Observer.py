class Observer(object):

    def __init__(self):
        """
        `Author`: Bill Clark

        An implementation of the observer pattern. An observer contains a text status, an optional 'op' field,
        and a new status flag. The observer pattern was implemented for the UI module, so that the UI could gain
        data from the various function modules. ImageMerge and UrlBuilder are both observed in this design.
        :return:
        """
        self.status = ''
        self.op = 0
        self.new = 0

    def __nonzero__(self):
        return self.new

    def update(self, string, op=None):
        """
        `Author`: Bill Clark

        Updates the observer's values. the op value is defaulted to None, and if it isn't set the op remains the same.
        The trigger method is called after update, allowing for an activity to occur every update. Trigger can be
        overwritten, but update should not be changed. The new value is also set to 1, showing the observer
        has a new status to report.

        `string`: The text value to set the status too.

        `op`: Defaulted to none. The optional argument.
        """
        self.new = 1
        self.status = string
        if op is not None: self.op = op
        self.trigger()

    def trigger(self):
        """
        `Author`: Bill Clark

        A default trigger method. Rather than pass, it prints the status and op values. This should more than likely
        be overwritten.
        """
        print self.status, self.op

    def check(self):
        """
        `Author`: Bill Clark

        A check method. This is method to use to process data if one wants to make use of the new flag. This method,
        as opposed to trigger, turns off the new flag. This should be overwritten and have super called to it, or
        copy the self.new = 0 line to your implementation.
        """
        self.new = 0


class Observable(object):

    def __init__(self):
        """
        `Author`: Bill Clark

        This method is used to give a module the ability to be observed. Any module that extends this class
        gains a list of observers, a register observer method, and setStatus.
        """
        self.observers = []

    def setStatus(self, string, op=None):
        """
        `Author`: Bill Clark

        Set the status of each observer the object has. Does so via the update method in each Observer.

        `string`: Text to set the observer's status too.

        `op`: The optional argument.
        """
        if self.observers:
            for observer in self.observers:
                observer.update(string, op)

    def register(self, object):
        """
        `Author`: Bill Clark

        Register a new observer to the Observable.

        `object`: An observer to add to this object.
        """
        self.observers.append(object)
