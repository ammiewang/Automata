class state():
    def __init__(self, id):
        self.id = id
        self.outpaths = {}
        self.parent = (None, None)
        self.children = []
    def reverse_outpaths(self):
        self.rev_op = {}
        temp = [(v,k) for k,v in self.outpaths.items()]
        for k,v in temp:
            if k in self.rev_op:
                self.rev_op[k].append(v)
            else:
                self.rev_op[k] = [v]

class path():
    def __init__(self, root):
        self.root = root
