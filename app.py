# Include libs
from tkinter import Tk, Button, Canvas, Frame, Label

class App:

    # Window config
    title    = 'Graph | UniverProject'
    width    = 600
    height   = 400
    modes    = [ 'add vertex', 'add connection', 'remove', 'move' ]
    
    # Program elements
    buttons  = {}
    layouts  = {}
    labels   = {}
    canvas   = None
    root     = None

    # Data
    mode     = 0
    vertexes = []

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
        for k, v in self.buttons.items():
            v.grid( row = 0, column = column, in_ = self.layouts['modeSelector'], padx = 10, pady = 10)
            column += 1

        self.labels['currentMode'].grid( row = 0, column = column, in_ = self.layouts['modeSelector'], padx = 30, pady = 10)

    def initEvents(self):
        self.buttons['addVertex'].bind( '<Button-1>', lambda _: self.setMode(0) )
        self.buttons['addConnection'].bind( '<Button-1>', lambda _: self.setMode(1) )
        self.buttons['remove'].bind( '<Button-1>', lambda _: self.setMode(2) )
        self.buttons['move'].bind( '<Button-1>', lambda _: self.setMode(3) )
    
    def setMode(self, mode):
        self.mode = mode
        self.labels['currentMode'].config( text = 'Mode: ' + self.modes[self.mode] )
    
    def run(self):
        self.root.mainloop()