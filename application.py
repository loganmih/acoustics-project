from tkinter import ttk
from tkinter import font as tkFont
import tkinter as tk
from PIL import ImageTk, Image
from model import Model


# Create view, and controller objects in order to organize funcionality in the application.
# Creating the  view, and controller objects here will reduce clutter in the project.
# The other py modules will contain code to handle the audio processing.

root = tk.Tk()

helveticaLabel = tkFont.Font(family='Helvetica', size=18, weight='bold')
helveticaText = tkFont.Font(family='Helvetica', size=16)
helveticaButton = tkFont.Font(family='Helvetica', size=12, weight='bold')

class MainView(ttk.Frame):

    def uploadButtonClicked(self):
        self.controller.upload()

    def setController(self, controller):
        self.controller = controller

    
    #code to run once a file has been uploaded
    def fileUploaded(self):
        self.panel.pack(side=tk.LEFT)
        
        #ensure the right file name is being used for the label
        self.fileLabel.config(text=self.fileName, justify=tk.RIGHT)
        self.fileLengthLabel.config(text=self.controller.getWavLength(), justify=tk.RIGHT)

        self.fileLabel.pack(side=tk.TOP)
        self.fileLengthLabel.pack(side=tk.RIGHT, expand=True, fill=tk.Y)

        self.fileText.grid(row=1, column=0, sticky=tk.W, pady=20)

    
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self.controller: Controller()
        self.fileName = ""

        #set size of root window and prevent resizing
        parent.resizable(False, False)
        parent.geometry('700x400')
        parent.config(padx=20, pady=20)

        self.fileText = tk.Frame(parent)
        self.uploadText = tk.Frame(parent)

        #Upload File label and button
        self.uploadLabel = ttk.Label(self.uploadText, text="Upload Data", font=helveticaLabel)
        self.uploadLabel.pack(side=tk.LEFT, fill=tk.X)
        self.uploadButton = tk.Button(self.uploadText, text="Select File", font=helveticaButton, command=self.uploadButtonClicked)
        self.uploadButton.pack(side=tk.RIGHT, fill=tk.X)

        self.uploadText.grid(row=0, column=0, sticky="w")

        #every widget after file upload, such as convert status, plot button, file icon, time, waveform,
        #highest resonance, low, medium, and high frequency RT60, etc
        #once file is uploaded, these widgets will show
        self.fileIcon = ImageTk.PhotoImage(Image.open('wavicon.png').resize((60,60)))
        self.panel = tk.Label(self.fileText, image=self.fileIcon)

        self.fileLabel = ttk.Label(self.fileText, font=helveticaText)
        self.fileLengthLabel = ttk.Label(self.fileText, font=helveticaText)
        
class Controller():

    def __init__(self, model: Model, view: MainView):
        self.model = model 
        self.view = view

    def upload(self):
        self.model.openFile()

        #grab file name before indicating it has been uploaded
        self.view.fileName = self.model.getFileName()
        self.view.fileUploaded()

    def getWavLength(self):
        return self.model.getWavLength()

view = MainView(root)
model = Model()
controller = Controller(model, view)
view.setController(controller)
view.grid(row=0, column=0)

view.mainloop()
