
class Set:
    def __init__(self, list = None):
        if list != None:
            self.items = list
        else:
            self.items = []

    def __add__(self, item):
        if self.items.__contains__(item):
            return False
        self.items.append(item)
        return True

    def put(self, item):
        return self.__add__(item)

    def __index__(self, item):
        return self.items.index(item)

    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return self.items.__str__()

class Clique:

    def __init__(self, list):
        self.items = list

    def __add__(self, item):
        if self.items.__contains__(item):
            self.items.append(item)
            return True
        return False

    def insert(self, item):
        return self.__add__(item)

    def __index__(self, item):
        return self.items.index(item)

    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return self.items.__str__()

class Wrapper:

    def __init__(self):
        pass
    
    def wrap(self, start, end):
        
        if start.lng * end.lng < 0:
            if start.lng > end.lng:
                if (-1 * end.lng) + start.lng < 180:
                    #right hand build
            else:
                if (-1* start.lng) + end.lng < 180:
                    #left hand build