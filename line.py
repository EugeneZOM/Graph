class Line:
    vertex1 = None
    vertex2 = None
    lineId = -1

    def __init__(self, v1, v2, lid):
        self.vertex1 = v1
        self.vertex2 = v2
        self.lineId = lid
    def getVertexesIndex(self):
        return ( self.vertex1, self.vertex2 )
    def getLineId(self):
        return self.lineId
    def setVertexesIndex(self, v1, v2):
        self.vertex1 = v1
        self.vertex2 = v2

class LineList:
    lines = {}

    def add(self, v1, v2, lid):
        if str(v1) not in self.lines: self.lines[str(v1)] = []
        if str(v2) not in self.lines: self.lines[str(v2)] = []
             
        self.lines[str(v1)].append( Line(v1, v2, lid) )
        self.lines[str(v2)].append( self.lines[str(v1)][-1] )
    
    def has(self, index):
        return ( (str(index) in self.lines) and (len(self.lines[str(index)]) > 0) )
    
    def getLines(self, index):
        return self.lines[str(index)]
    
    def deleteByVertex(self, v):
        result = []
        tmp_lines = self.lines[str(v)].copy()
        for line in tmp_lines:
            result.append(line.getLineId())
            self.deleteById(line.getLineId())

        #for i in range(v, len(self.lines)-1):
        #    self.lines[str(i)] = self.lines[str(i+1)].copy()
        #self.lines[str(len(self.lines)-1)] = []

        # Update vertexes's index
        changedLines = []
        for vindex in self.lines.values():
            for l in vindex:
                if l in changedLines:
                    continue
                changedLines.append(l)
                vertexes = l.getVertexesIndex()
                v1 = vertexes[0]
                v2 = vertexes[1]
                v1 = v1-1 if v1 > v else v1
                v2 = v2-1 if v2 > v else v2
                l.setVertexesIndex(v1, v2)

        return result
    
    def deleteById(self, lid):
        line = None
        for v in self.lines.values():
            for l in v:
                if l.getLineId() == lid:
                    line = l
                    break

        vertexes = line.getVertexesIndex()
        v1 = vertexes[0]
        v2 = vertexes[1]
        
        for i in range(len(self.lines[str(v1)])):
            if self.lines[str(v1)][i] == line:
                del self.lines[str(v1)][i]
                break

        for i in range(len(self.lines[str(v2)])):
            if self.lines[str(v2)][i] == line:
                del self.lines[str(v2)][i]
                break