import os, io
from tkinter import filedialog as fd

class Model():

    #initialize object variables
    def __init__(self):
        self.filename = ""
        self.f: io.TextIOWrapper
    
    #get file from user and open it
    def openFile(self):
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        self.f = open(self.filename, 'r')
    
    #these are the functions that will calculate the values such as the Waveform, resonance,
    #low, med, high rt60, etc
    def getResonance(self):
        pass

    def getRT(self):
        pass

    def getWavLength(self):
        return "5" 

    def getFileName(self):
        print(self.filename)
        return self.filename

    def __del__(self):
        self.f.close()