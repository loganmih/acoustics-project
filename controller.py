from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Controller():

    def __init__(self, model, view):
        self.model = model 
        self.view = view

    def upload(self):
        self.model.setup_audio_file()
        self.model.process_audio_file()
        self.model.find_frequency_RT60s()

        #grab file name before indicating it has been uploaded
        self.view.filePath = self.model.filein.split("/")[-1]
        self.view.fileUploaded()

    def showAmplitude(self):
        plt.plot(self.model.freqs, self.model.avg_amplidtude_per_freq)
        plt.xlim(0, 3000)
        plt.tight_layout()

        plt.xlabel("frequency")
        plt.ylabel("amplitude")

        plt.show()

    def getResonantFreq(self):
        return self.model.resonant_freq
    
    def getrt60s(self):
        return [round(x["RT60"], 3) for x in self.model.frequency_data]

    def getDifference(self):
        return str(round(self.model.difference, 3))
    
    def plotrt60s(self):
        self.lowPlot = Figure(figsize=(3, 3), layout="constrained")
        self.medPlot = Figure(figsize=(3, 3), layout="constrained")
        self.highPlot = Figure(figsize=(3, 3), layout="constrained")

        self.combinedPlot = Figure(figsize=(3, 3), layout="constrained")

        a = self.lowPlot.add_subplot(111)
        b = self.medPlot.add_subplot(111)
        c = self.highPlot.add_subplot(111)

        lowSubPlot = self.combinedPlot.add_subplot(111)

        self.RT60plots = [a, b, c]

        a.set_title("Low RT60")
        b.set_title("Med RT60")
        c.set_title("High RT60")
        lowSubPlot.set_title("Combined Plot")

        for i, x in enumerate(self.model.frequency_data):
            self.RT60plots[i].plot(self.model.times, x["amplitudes"])
            self.RT60plots[i].plot(self.model.times[x["max_amplitude_index"]], x["max_amplitude"], "go")
            self.RT60plots[i].plot(self.model.times[x["top_RT20_index"]], x["top_RT20_amplitude"], "yo")
            self.RT60plots[i].plot(self.model.times[x["bottom_RT20_index"]], x["bottom_RT20_amplitude"], "ro")
            self.RT60plots[i].set_xlabel("time")
            self.RT60plots[i].set_ylabel("amplitude")

        lowSubPlot.plot(self.model.times, self.model.frequency_data[0]["amplitudes"])
        lowSubPlot.plot(self.model.times, self.model.frequency_data[1]["amplitudes"])
        lowSubPlot.plot(self.model.times, self.model.frequency_data[2]["amplitudes"])

        lowSubPlot.set_xlabel("time")
        lowSubPlot.set_ylabel("amplitude")
        lowSubPlot.legend(['low', 'med', 'high'])

    def getWavLength(self):
        return str(self.model.audio_duration)
    
    def plotWave(self):
        #calculate waveform using the model plot wave function
        self.model.plot_wave()
        #self.model.process_audio_file()

        #grab the figure calculated in the model function and pass it through to the view in order to plot
        self.fig = Figure(figsize=(4.5,2.5), layout="constrained")
        a = self.fig.add_subplot()
        a.plot(self.model.sig)

        a.set_title("WAV Waveform")
        a.set_xlabel("time")
        a.set_ylabel("amplitude")
        
        self.view.plotWave(self.fig)
