
class OrderedSet(object):
    """
    this class is our implementation of an ordered set in python

    It wraps a list, allowing the the admission of elements only if the are NOT already contained in the list

    """

    lst = []    # internal component, collection of elements

    def __init__(self, iterable=None):
        self.clear()

    def __len__(self):
        return len(self.lst)

    def __contains__(self, item):
        return item in self.lst

    def add(self, item):
        print self.lst
        if not self.__contains__(item):
            self.lst.append(item)
            return True
        return False

    def clear(self):
        self.lst = []

    def __iter__(self):
        return self.lst

    def __getitem__(self, index):
        return self.lst[index]
