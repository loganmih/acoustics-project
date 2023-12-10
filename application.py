from tkinter import ttk
from tkinter import font as tkFont
import tkinter as tk
from PIL import ImageTk, Image
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

    def getResonantFreq(self):
        return self.controller.getResonantFreq()
    
    def getrt60s(self):
        return self.controller.getrt60s()

    def plotWave(self, fig):
        #generate canvas to use as widget in tk
        self.canvas = FigureCanvasTkAgg(fig, master=self.plotWindow)
        self.canvas.get_tk_widget().pack(padx=20)
        self.plotWindow.grid(column=1, row=1, sticky='n')
    
    #code to run once a file has been uploaded
    def fileUploaded(self):
        self.panel.pack(side=tk.LEFT, padx=(0, 20))
        
        #ensure the right file name is being used for the label
        self.fileName = self.filePath.split("/")[-1]
        self.fileLabel.config(text=self.fileName, justify=tk.RIGHT)
        self.fileLengthLabel.config(text=self.controller.getWavLength() + " sec", justify=tk.RIGHT)

        self.fileLabel.pack(side=tk.TOP)
        self.fileLengthLabel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.fileText.grid(row=1, column=0, sticky="nw", pady=20)

        #trigger wave plotting function in order to plot the waveform of thie audio file
        self.controller.plotWave()

        #plot button
        self.plotButton.grid(row=1, column=0, sticky='s', pady=20)


        #resonance data text
        self.highestResonanceLabel.config(text="Highest Resonance")
        self.rt60Label.config(text="Low, Med, High RT60")
        
        self.highestResonanceValue.config(text=str(self.getResonantFreq()) + " hz")
        self.rt60Value.config(text=str(self.getrt60s()))

        self.highestResonanceLabel.grid(row=3, column=0, sticky='n', pady=20)
        self.rt60Label.grid(row=3, column=1, sticky='n', pady=20)

        self.highestResonanceValue.grid(row=4, column=0, sticky='n')
        self.rt60Value.grid(row=4, column=1, sticky='n')

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self.controller: Controller()
        self.filePath = ""

        #set size of root window and prevent resizing
        parent.resizable(False, False)
        parent.geometry('700x400')
        parent.config(padx=20, pady=20)

        self.fileText = tk.Frame(parent)
        self.uploadText = tk.Frame(parent)
        self.resonanceText = tk.Frame(parent)

        self.plotWindow = tk.Frame(parent)

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
        self.panel = ttk.Label(self.fileText, image=self.fileIcon)

        self.fileLabel = ttk.Label(self.fileText, font=helveticaLabel)
        self.fileLengthLabel = ttk.Label(self.fileText, font=helveticaLabel)

        #button to show plots of rt60
        self.plotButton = tk.Button(parent, text="Plot RT60", font=helveticaButton)

        #data about the audio file
        self.highestResonanceLabel = ttk.Label(parent, font=helveticaLabel)
        self.highestResonanceValue = ttk.Label(parent, font=helveticaLabel)

        self.rt60Label = ttk.Label(parent, font=helveticaLabel)
        self.rt60Value = ttk.Label(parent, font=helveticaLabel)

class Controller():

    def __init__(self, model: Model, view: MainView):
        self.model = model 
        self.view = view

    def upload(self):
        self.model.setup_audio_file()
        self.model.process_audio_file()
        self.model.find_frequency_RT60s()

        #grab file name before indicating it has been uploaded
        self.view.filePath = self.model.filein.split("/")[-1]
        self.view.fileUploaded()

    def getResonantFreq(self):
        return self.model.resonant_freq
    
    def getrt60s(self):
        return [round(x["RT60"], 3) for x in self.model.frequency_data]
        
    def getWavLength(self):
        return str(self.model.audio_duration)
    
    def plotWave(self):
        #calculate waveform using the model plot wave function
        self.model.plot_wave()
        #self.model.process_audio_file()

        #grab the figure calculated in the model function and pass it through to the view in order to plot
        self.fig = Figure(figsize=(4,2))
        a = self.fig.add_subplot(111)
        a.plot(self.model.sig)

        self.view.plotWave(self.fig)

view = MainView(root)
model = Model()
controller = Controller(model, view)
view.setController(controller)
view.grid(row=0, column=0)

view.mainloop()
