from tkinter import ttk
from tkinter import font as tkFont
import tkinter as tk
from PIL import ImageTk, Image
from controller import Controller
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create view, and controller objects in order to organize funcionality in the application.
# Creating the  view, and controller objects here will reduce clutter in the project.
# The other py modules will contain code to handle the audio processing.


#create new window to show four plots, as well as a button to combine the plots


class MainView(ttk.Frame):
    
    def uploadButtonClicked(self):
        self.controller.upload()

    def showAmplitude(self):
        self.controller.showAmplitude() 

    def setController(self, controller):
        self.controller = controller

    def getResonantFreq(self):
        return self.controller.getResonantFreq()
    
    def getrt60s(self):
        return self.controller.getrt60s()
    
    def getDifference(self):
        return self.controller.getDifference()
    
    def plotrt60s(self):
        self.controller.plotrt60s()

        self.lowCanvas = FigureCanvasTkAgg(self.controller.lowPlot, master=self.newWindow)
        self.lowCanvas.get_tk_widget().grid(column=1, row=1, padx=20, pady=20)

        self.medCanvas = FigureCanvasTkAgg(self.controller.medPlot, master=self.newWindow)
        self.medCanvas.get_tk_widget().grid(column=2, row=1, padx=20, pady=20)
        
        self.highCanvas = FigureCanvasTkAgg(self.controller.highPlot, master=self.newWindow)
        self.highCanvas.get_tk_widget().grid(column=1, row=2, padx=20, pady=20)

        self.combinedCanvas = FigureCanvasTkAgg(self.controller.combinedPlot, master=self.newWindow)

    def combinePlot(self):
        self.combinedCanvas.get_tk_widget().grid(column=2, row=2, padx=20, pady=20)

    def plotWave(self, fig):
        #generate canvas to use as widget in tk
        self.canvas = FigureCanvasTkAgg(fig, master=self.plotWindow)
        self.canvas.get_tk_widget().pack(padx=20)
        self.plotWindow.grid(column=1, row=1, sticky='n')

    def newRT60Window(self):
        self.newWindow = tk.Toplevel()

        self.newWindow.resizable(False, False)
        self.newWindow.config(width=700, height=400)

        self.plotrt60s()

        self.newRTText = ttk.Label(self.newWindow, text="Difference: " + self.getDifference(), font=self.helveticaLabel)
        self.newRTText.grid(column=1, row=0)

        self.combineButton = tk.Button(self.newWindow, text="Combine Plots", command=self.combinePlot, font=self.helveticaButton)
        self.combineButton.grid(column=0, row=0, padx=20, pady=20, sticky='nw')
    
    #code to run once a file has been uploaded
    def fileUploaded(self):
        self.panel.pack(side=tk.LEFT, padx=(0, 20))

        self.uploadButton.destroy()
        
        #ensure the right file name is being used for the label
        self.fileName = self.filePath.split("/")[-1]
        self.fileLabel.config(text=self.fileName, justify=tk.RIGHT)
        self.fileLengthLabel.config(text=self.controller.getWavLength() + "s", justify=tk.RIGHT)

        self.fileLabel.pack(side=tk.TOP)
        self.fileLengthLabel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.fileText.grid(row=1, column=0, sticky="nw", pady=20)

        #trigger wave plotting function in order to plot the waveform of thie audio file
        self.controller.plotWave()

        #plot button
        self.amplitudeButton.grid(row=1, column=0, pady=20)
        self.plotButton.grid(row=1, column=0, sticky='s', pady=20)


        #resonance data text
        self.highestResonanceLabel.config(text="Highest Resonance")
        self.rt60Label.config(text="Low, Med, High RT60")
        
        self.highestResonanceValue.config(text=str(self.getResonantFreq()) + " Hz")
        self.rt60Value.config(text=str(self.getrt60s()))

        self.highestResonanceLabel.grid(row=3, column=0, sticky='n', pady=20)
        self.rt60Label.grid(row=3, column=1, sticky='n', pady=20)

        self.highestResonanceValue.grid(row=4, column=0, sticky='n')
        self.rt60Value.grid(row=4, column=1, sticky='n')

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)


        self.helveticaLabel = tkFont.Font(family='Helvetica', size=18, weight='bold')
        self.helveticaButton = tkFont.Font(family='Helvetica', size=12, weight='bold')

        self.controller: Controller()
        self.filePath = ""

        #set size of root window and prevent resizing
        parent.resizable(False, False)
        parent.geometry('700x450')
        parent.config(padx=20, pady=20)

        self.fileText = tk.Frame(parent)
        self.uploadText = tk.Frame(parent)
        self.resonanceText = tk.Frame(parent)

        self.plotWindow = tk.Frame(parent)

        #Upload File label and button
        self.uploadLabel = ttk.Label(self.uploadText, text="Upload Data", font=self.helveticaLabel)
        self.uploadLabel.pack(side=tk.LEFT, fill=tk.X)
        self.uploadButton = tk.Button(self.uploadText, text="Select File", font=self.helveticaButton, command=self.uploadButtonClicked)
        self.uploadButton.pack(side=tk.RIGHT, fill=tk.X)

        self.uploadText.grid(row=0, column=0, sticky="w")

        #every widget after file upload, such as convert status, plot button, file icon, time, waveform,
        #highest resonance, low, medium, and high frequency RT60, etc
        #once file is uploaded, these widgets will show
        self.fileIcon = ImageTk.PhotoImage(Image.open('wavicon.png').resize((60,60)))
        self.panel = ttk.Label(self.fileText, image=self.fileIcon)

        self.fileLabel = ttk.Label(self.fileText, font=self.helveticaLabel)
        self.fileLengthLabel = ttk.Label(self.fileText, font=self.helveticaLabel)

        #button to show plots of rt60
        self.amplitudeButton = tk.Button(parent, text="Plot Average Amplitude", font=self.helveticaButton, command=self.showAmplitude)
        self.plotButton = tk.Button(parent, text="Plot RT60", font=self.helveticaButton, command=self.newRT60Window)

        #data about the audio file
        self.highestResonanceLabel = ttk.Label(parent, font=self.helveticaLabel)
        self.highestResonanceValue = ttk.Label(parent, font=self.helveticaLabel)

        self.rt60Label = ttk.Label(parent, font=self.helveticaLabel)
        self.rt60Value = ttk.Label(parent, font=self.helveticaLabel)



