# Simple realization of queue ADT

class Queue:
    """Realization of queue ADT
    Works using list"""
    def __init__(self):
        self.items = []

    def isEmpty(self):
        """Return if queue is empty"""
        return self.items == []

    def enqueue(self, item):
        """Adds item to the queue"""
        self.items.insert(0, item)

    def dequeue(self):
        """Removes item from the queue"""
        return self.items.pop()

    def get_item(self, index):
        """Get item by index from the queue"""
        return self.items[index]

    def size(self):
        """Returns size of the queue"""
        return len(self.items)
