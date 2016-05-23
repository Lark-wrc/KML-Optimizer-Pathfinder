class Observer():

    def __init__(self):
        self.status = ''
        self.count = 0
        self.new = 0

    def __nonzero__(self):
        return self.new

    def update(self, string, int):
        self.new = 1
        self.status = string
        self.count = int
        self.trigger()

    def trigger(self):
        print self.status, self.count

    def check(self):
        self.new = 0
        return self.status, self.count