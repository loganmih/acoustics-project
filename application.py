from tkinter import ttk
from tkinter import font as tkFont
from tkinter import filedialog as fd
import tkinter as tk
from PIL import ImageTk, Image
import os, io
# Create model, view, and controller objects in order to organize funcionality in the application.
# Creating the model, view, and controller objects here will reduce clutter in the project.
# The other py modules will contain code to handle the audio processing.

root = tk.Tk()

helveticaLabel = tkFont.Font(family='Helvetica', size=18, weight='bold')
helveticaButton = tkFont.Font(family='Helvetica', size=12, weight='bold')

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

    def __del__(self):
        self.f.close()
    
class MainView(ttk.Frame):

    def fileUploaded(self):
        self.panel.grid(row=2, column=0, sticky='W', pady=20)

    def uploadButtonClicked(self):
        self.controller.upload()

    def setController(self, controller):
        self.controller = controller

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self.controller: Controller()

        #set size of root window and prevent resizing
        parent.resizable(False, False)
        parent.geometry('700x400')

        #Upload File label and button
        self.uploadLabel = ttk.Label(self, text="Upload Data", font=helveticaLabel)
        self.uploadLabel.grid(row=1, column=0)

        self.uploadButton = tk.Button(self, text="Select File", font=helveticaButton, command=self.uploadButtonClicked)
        self.uploadButton.grid(row=1, column=1)

        #every widget after file upload, such as convert status, plot button, file icon, time, waveform,
        #highest resonance, low, medium, and high frequency RT60, etc
        #once file is uploaded, these widgets will show

        self.fileIcon = ImageTk.PhotoImage(Image.open('wavicon.png').resize((60,60)))
        self.panel = tk.Label(self, image=self.fileIcon)
        
class Controller():

    def __init__(self, model: Model, view: MainView):
        self.model = model 
        self.view = view


    def upload(self):
        self.model.openFile()
        self.view.fileUploaded()

view = MainView(root)
model = Model()
controller = Controller(model, view)
view.setController(controller)
view.grid(row=0, column=0, padx=20, pady=20)

view.mainloop()
