class mylist:
    def __init__(self):
        self.data = None
        self.next = None

    def add_list(self, val):
        if self.data is None:
            self.data = val
            return self
        else:
            new_index = mylist()
            new_index.add_tolist(val)
            return new_index

    #recursive function to get last index, complexity O(n)
    def get_last(self):
        if self.next is None:
            return self
        else:
            return self.get_last(self.next)

    # recursive function to print all indexes, complexity O(n)
    def print_list_to_console(self):
        print(self.data)
        if self.next is None:
            return
        self.next.print_list_to_console()


class queue:
    def __init__(self):
        qlist = mylist()
        self.anchor = qlist
        self.last = qlist
        self.size = 0

    def add_list_to_q(self,l: mylist):
        self.anchor = l
        self.last = l.get_last()

    def isempty(self):
        return self.size == 0

    def add_to_q(self, val):
        new_l = mylist()
        new_l.add_list(val)
        self.size += 1
        if self.last == self.anchor:
            if self.anchor.data is None:
                self.anchor = new_l
                self.last = new_l
                return
        self.last.next = new_l
        self.last = self.last.next

    def pop_from_q(self):
        if self.size == 0:
            return None
        val = self.anchor.data
        if self.anchor.next is None:
            self.anchor.data = None
        else:
            self.anchor = self.anchor.next
        self.size -= 1
        return val

    def print_q_log(self):
        self.anchor.print_list_to_console()

""" Tests
q = queue()
q.add_to_q(5)
q.add_to_q(8)
q.add_to_q(9)
q.print_q_log()
print(f"popped: {q.pop_from_q()}")
q.print_q_log()
"""