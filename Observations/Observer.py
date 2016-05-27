class Observer(object):

    def __init__(self):
        self.status = ''
        self.op = 0
        self.new = 0

    def __nonzero__(self):
        return self.new

    def update(self, string, op=None):
        self.new = 1
        self.status = string
        if op is not None: self.op = op
        self.trigger()

    def trigger(self):
        print self.status, self.op

    def check(self):
        self.new = 0
        return self.status, self.op


class Observable(object):

    def __init__(self):
        self.observers = []

    def setStatus(self, string, op=None):
            if self.observers:
                for observer in self.observers:
                    observer.update(string, op)

    def register(self, object):
        self.observers.append(object)
