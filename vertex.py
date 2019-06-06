class Vertex:
    index = -1
    elem_id = -1

    def __init__(self, index, elem_id):
        self.index = index
        self.elem_id = elem_id
    
    def getIndex(self):
        return self.index
    def getElemId(self):
        return self.elem_id
    def remove(self, callback):
        callback(self.elem_id)