# Include libs
from tkinter import Tk, Button, Canvas, Frame, Label
from vertex import VertexList
from line import LineList

class App:

    # Window config
    title       = 'Graph | UniverProject'
    width       = 600
    height      = 400
    modes       = [ 'add vertex', 'add connection', 'remove', 'move' ]
    vertexSize  = 30
    
    # Program elements
    buttons     = {}
    layouts     = {}
    labels      = {}
    canvas      = None
    root        = None

    # Data
    mode        = 0                         # 0 - add vertex, 1 - add line, 2 - remove, 3 - move
    vertexes    = VertexList()
    lines       = LineList()

    # Temporary variables
    tmp_vertex  = -1

    def __init__(self):
        self.initElements()
        self.styleElements()
        self.initEvents()
        self.packElements()

    def initElements(self):
        self.root = Tk()

        self.canvas                   = Canvas(self.root)
        self.layouts['modeSelector']  = Frame (self.root)

        self.buttons['addVertex']     = Button(self.layouts['modeSelector'], text = 'Add vertex')
        self.buttons['addConnection'] = Button(self.layouts['modeSelector'], text = 'Add connection')
        self.buttons['remove']        = Button(self.layouts['modeSelector'], text = 'Remove')
        self.buttons['move']          = Button(self.layouts['modeSelector'], text = 'Move')

        self.labels ['currentMode']   = Label (self.layouts['modeSelector'], text = 'Mode: ' + self.modes[self.mode])
    
    def styleElements(self):
        # Calculate position for window centering
        px = int(self.root.winfo_screenwidth() / 2 - self.width / 2)
        py = int(self.root.winfo_screenheight() / 2 - self.height / 2) 

        # Style for root window
        self.root.title ( self.title )
        self.root.geometry( str(self.width) + 'x' + str(self.height) + '+' + str(px) + '+' + str(py) )
        self.root.resizable( False, False )
        # Style for layouts
        self.layouts['modeSelector'].config( bg = '#aaa' )
        # Style for buttons
        self.buttons['addVertex'].config( borderwidth = 0 )
        self.buttons['addConnection'].config( borderwidth = 0 )
        self.buttons['remove'].config( borderwidth = 0 )
        self.buttons['move'].config( borderwidth = 0 )
        # Style for labels
        self.labels['currentMode'].config( padx = 10, pady = 10, font = 'Helvetica 8 bold', width = 20, anchor = 'w' )
        # Style for canvas
        self.canvas.config( bg = '#fff' )
    
    def packElements(self):
        # Add elements to window
        self.layouts['modeSelector'].pack( anchor = 'n', fill = 'x', expand = False )
        self.canvas.pack( anchor = 's', side = 'top', fill = 'both', expand = True )
        # Add buttons to layout
        column = 0
        for v in self.buttons.values():
            v.grid( row = 0, column = column, in_ = self.layouts['modeSelector'], padx = 10, pady = 10)
            column += 1

        self.labels['currentMode'].grid( row = 0, column = column, in_ = self.layouts['modeSelector'], padx = 30, pady = 10)

    def initEvents(self):
        self.buttons['addVertex'].bind( '<Button-1>', lambda _: self.setMode(0) )
        self.buttons['addConnection'].bind( '<Button-1>', lambda _: self.setMode(1) )
        self.buttons['remove'].bind( '<Button-1>', lambda _: self.setMode(2) )
        self.buttons['move'].bind( '<Button-1>', lambda _: self.setMode(3) )
        self.canvas.bind( '<Button-1>', self.canvasClick )
    
    def setMode(self, mode):
        self.mode = mode
        self.labels['currentMode'].config( text = 'Mode: ' + self.modes[self.mode] )
    
    def run(self):
        self.root.mainloop()

    # Events
    def canvasClick(self, event):
        if self.mode == 0:
            v = self.canvas.create_oval(
                event.x - self.vertexSize / 2,
                event.y - self.vertexSize / 2,
                event.x + self.vertexSize / 2,
                event.y + self.vertexSize / 2,
                fill = '#88f',
                activefill = '#aaf'
            )
            t = self.canvas.create_text(
                event.x, event.y,
                text = self.vertexes.getAmount()
            )
            self.vertexes.add(v, t)
            index = self.vertexes.getAmount() - 1

            self.canvas.tag_bind(v, '<Button-1>', lambda _: self.vertexClick(index))
            self.canvas.tag_bind(t, '<Button-1>', lambda _: self.vertexClick(index))
            self.canvas.tag_bind(v, '<B1-Motion>', lambda e: self.vertexMove(index, e))
            self.canvas.tag_bind(t, '<B1-Motion>', lambda e: self.vertexMove(index, e))
            self.canvas.tag_bind(t, '<Enter>', lambda _: self.canvas.itemconfig(v, fill = '#aaf'))
            self.canvas.tag_bind(t, '<Leave>', lambda _: self.canvas.itemconfig(v, fill = '#88f'))
    def vertexClick(self, index):
        if self.mode == 1:
            if self.tmp_vertex == -1:
                self.tmp_vertex = index
            else:
                v1 = self.tmp_vertex
                v2 = index

                if v1 == v2:
                    self.tmp_vertex = -1
                    return

                pos1 = self.canvas.coords(self.vertexes.getTextElemId(v1))
                pos2 = self.canvas.coords(self.vertexes.getTextElemId(v2))

                l = self.canvas.create_line(
                    pos1[0], pos1[1], pos2[0], pos2[1],
                    width = self.vertexSize / 3,
                    fill = '#888'
                )
                self.lines.add(v1, v2, l)
                self.canvas.tag_bind(l, '<Button-1>', lambda e: self.lineClick(l))

                depth = l - min(self.vertexes.getVertexElemId(v1), self.vertexes.getVertexElemId(v2))

                for i in range(depth):
                    self.canvas.tag_lower(l)

                self.tmp_vertex = -1
        elif self.mode == 2:
            vid, tid = self.vertexes.get(index)
            self.canvas.delete(vid, tid)
            self.vertexes.delete(index)

            # Update text values
            for i in range(index, self.vertexes.getAmount()):
                tmp_index = i
                elem = self.vertexes.get(tmp_index)
                v = elem[0]
                t = elem[1]
                
                self.canvas.itemconfig(t, text = tmp_index)
                # Update vertexes's events
                    # Unbind old events
                self.canvas.tag_unbind(v, '<Button-1>')
                self.canvas.tag_unbind(t, '<Button-1>')
                self.canvas.tag_unbind(v, '<B1-Motion>')
                self.canvas.tag_unbind(t, '<B1-Motion>')
                    # Bind updated events
                def bind(index):
                    self.canvas.tag_bind(v, '<Button-1>', lambda _: self.vertexClick(index))
                    self.canvas.tag_bind(t, '<Button-1>', lambda _: self.vertexClick(index))
                    self.canvas.tag_bind(v, '<B1-Motion>', lambda e: self.vertexMove(index, e))
                    self.canvas.tag_bind(t, '<B1-Motion>', lambda e: self.vertexMove(index, e))
                
                bind(tmp_index)

            # Delete lines if exist
            if(self.lines.has(index)):
                lines = self.lines.deleteByVertex(index)
                for lid in lines:
                    self.canvas.delete(lid)
    def lineClick(self, lineId):
        if self.mode != 2:
            return
        
        self.canvas.delete(lineId)
        self.lines.deleteById(lineId)
    def vertexMove(self, index, event):
        if self.mode != 3:
            return

        event.x = max(min(event.x, self.canvas.winfo_width()), 0)
        event.y = max(min(event.y, self.canvas.winfo_height()), 0)

        ids = self.vertexes.get(index)

        v = ids[0]
        t = ids[1]

        self.canvas.coords(
            v,
            event.x - self.vertexSize / 2,
            event.y - self.vertexSize / 2,
            event.x + self.vertexSize / 2,
            event.y + self.vertexSize / 2
        )
        self.canvas.coords(
            t, event.x, event.y
        )
        
        if not self.lines.has(index):
            return

        lines = self.lines.getLines(index)
        for line in lines:
            lid = line.getLineId()

            v1 = self.vertexes.getTextElemId(line.getVertexesIndex()[0])
            v2 = self.vertexes.getTextElemId(line.getVertexesIndex()[1])

            pos1 = self.canvas.coords(v1)
            pos2 = self.canvas.coords(v2)

            self.canvas.coords(
                lid,
                pos1[0], pos1[1],
                pos2[0], pos2[1]
            )