import os, io
from tkinter import filedialog as fd
import matplotlib.figure as plt
from matplotlib.figure import Figure
import wave
import numpy as np
import sox as sox

class Model():

    #initialize object variables
    def __init__(self):
        self.filename = ""
        self.f: io.TextIOWrapper
    
    #get file from user and open it
    def openFile(self):
        filetypes = (
            ('Audio files', '*.wav *.ogg *.mp3'),
            ('All files', '*.*')
        )

        self.filein = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

        tfm = sox.Transformer()
        tfm.set_output_format(bits=16, encoding='signed-integer')
        tfm.build(self.filein, "output.wav")

        self.f = wave.open("output.wav", 'r')
        sample_rate = 16000
        self.sig = np.frombuffer(self.f.readframes(sample_rate), dtype=np.int16)

    
    #these are the functions that will calculate the values such as the Waveform, resonance,
    #low, med, high rt60, etc
    def getResonance(self):
        pass

    def getRT(self):
        pass

    def getWavLength(self):
        return str(round(sox.file_info.duration("output.wav"), 2))
    
    def plotWave(self):
        self.fig = Figure(figsize=(4,2))
        a = self.fig.add_subplot(111)
        a.plot(self.sig)

    def getFileName(self):
        print(self.filename)
        return self.filein

    def __del__(self):
        self.f.close()