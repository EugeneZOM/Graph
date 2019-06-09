class Vertex:
    index = -1
    elemId = -1

    def __init__(self, index, elemId):
        self.index = index
        self.elemId = elemId
    
    def getIndex(self):
        return self.index
    def getElemId(self):
        return self.elemId
    def setIndex(self, index):
        self.index = index

class VertexList:
    vertexes = []

    def add(self, vertexElemId, textElemId):
        index = len(self.vertexes)
        self.vertexes.append( (Vertex(index, vertexElemId), textElemId) )

    def get(self, index):
        ids = ( self.vertexes[index][0].getElemId(), self.vertexes[index][1] )
        return ids
    
    def getVertexElemId(self, index):
        return self.vertexes[index][0].getElemId()
    
    def getTextElemId(self, index):
        return self.vertexes[index][1]
    
    def getAmount(self):
        return len(self.vertexes)

    def delete(self, index):
        del self.vertexes[index]
        for i in range(index, len(self.vertexes)):
            v = self.vertexes[i][0]
            v.setIndex(v.getIndex() - 1)