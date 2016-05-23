class Observer():

    def __init__(self):
        self.status = ''
        self.count = 0

    def update(self, string, int):
        self.status = string
        self.count = int
        self.trigger()

    def trigger(self):
        print self.status, self.count
