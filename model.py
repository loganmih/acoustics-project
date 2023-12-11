import os
import pydub
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
from tkinter import filedialog as fd
import wave
import math


class Model():

    def get_audio_file(self):
        filetypes = (
            ('Audio files', '*.wav *.mp3'),
            ('All files', '*.*')
        )

        self.filein = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
        )

    def setup_audio_file(self, file_path = "clap.mp3"):
        
        self.file_path = file_path

        #grab file path through select dialog
        self.get_audio_file()

        #set file path if one is given
        #if not, it will remain defualt
        if self.filein:
            self.file_path = self.filein
        
        file_type = self.file_path[-3:]

        print("File path:", self.file_path)

        # Converting the file format if needed
        if file_type == "wav":
            print("File already in wav format")

            self.audio = AudioSegment.from_wav(self.file_path)
        elif file_type == "mp3":
            print("File is in mp3 format, converting to wav")
            
            self.audio = AudioSegment.from_mp3(self.file_path)
        else:
            print("ERROR: File format not accepted. Please try again with a different file.")
            exit()


        # Converting from stereo to mono if needed
        print("Number of channels:", self.audio.channels)

        if self.audio.channels == 2:
            print("Converting from stereo to mono")
            self.audio = self.audio.set_channels(1)
        
        # Exporting audio file
        self.audio.export("output.wav", format="wav")
        

        #convert to 16 bit in order for wave library to work
        sr, data = wavfile.read("output.wav")
        wavfile.write("output.wav", sr, np.int16(data))

        # Duration of the audio in seconds
        self.audio_duration = len(self.audio) / 1000

        print("Audio duration:", self.audio_duration, "seconds")


    # Reads the audio data and uses the spectrogram to estimate the resonance
    def process_audio_file(self):
        sample_rate, data = wavfile.read("output.wav")

        spectrum, freqs, times, image = plt.specgram(data, Fs=sample_rate, NFFT=1024)

        self.sample_rate = sample_rate

        self.spectrum = spectrum
        self.freqs = freqs
        self.times = times
        self.image = image

        self.avg_amplidtude_per_freq = self.spectrum.mean(axis=1)

        self.max_freq_index = np.argmax(self.avg_amplidtude_per_freq)

        self.resonant_freq = self.freqs[self.max_freq_index]

        print("Resonant frequency (highest resonance):", self.resonant_freq, "Hz")


    # Finds the closest frquency to the target frequency
    def find_closest_freq(self, target_freq):
        # Subtracting the target freq from all of the freqencies and taking the absolute value.
        # This leaves the displacement from the target value, so taking the minimum of those will give us the closest element
        closest_index = np.argmin(np.abs(self.freqs - target_freq))

        return self.freqs[closest_index], closest_index

    # Finds the closest amplitude after the index offset
    def find_closest_amplitude(self, amplitudes, target_amplitude, index_offset = 0):
        # Loop through all of the amplitudes after the offset
        for i in range(index_offset, len(amplitudes)):
            # If we go past the target check this amplitude and the previous one
            if(amplitudes[i] < target_amplitude):
                prev_index = i - 1
                prev_amplitude = amplitudes[prev_index]

                # Use this amplitude if its closer to the target than the previous amplitude, or if the preview amplitude index is before the offset 
                if(abs(amplitudes[i] - target_amplitude) <= abs(prev_amplitude - target_amplitude) or prev_index < index_offset):
                    return amplitudes[i], i
                 
                # Otherwise return the previous amplitude
                return amplitudes[prev_index], prev_index 

        print("ERROR: Could not find amplitude smaller than target amplitude:", target_amplitude, "after index offset:", index_offset, "Returning last amplitude")
        return amplitudes[-1], -1


    # Finds the RT60 value for a target freqency, and stores relavant data in the given dictionary
    def find_RT60(self, target_freq, data_dict):
        print("Finding RT60 for target freqency", target_freq, "Hz")
        
        # Finding the closest frequency to the target frequency
        freq, freq_index = self.find_closest_freq(target_freq)

        print("The closest frequency to", target_freq, "Hz found in the data set was", freq, "Hz, so that will be used instead.")


        # Grabbing the amplitudes of the frequency over the time interval in decibels
        amplitudes = 10 * np.log10(self.spectrum[freq_index])

        self.amplitudes = amplitudes


        # Finding the max amplitude for this frequency
        max_amplitude_index = np.argmax(amplitudes)

        max_amplitude = amplitudes[max_amplitude_index]

        print("The max amplitude for this frequency is", max_amplitude, "dB")


        # The larger amplitude that we will be using in the RT20 calculation (max - 5dB), and its index in the amplitude array
        top_RT20_amplitude, top_RT20_index = self.find_closest_amplitude(amplitudes, max_amplitude - 5, max_amplitude_index + 1)

        # The smaller amplitude that we will be using in the RT20 calculation (max - 25dB), and its index in the amplitude array
        bottom_RT20_amplitude, bottom_RT20_index = self.find_closest_amplitude(amplitudes, max_amplitude - 25, top_RT20_index + 1)


        # Calculating the RT60 time using the RT20 time
        rt20 = self.times[bottom_RT20_index] - self.times[top_RT20_index]

        rt60 = rt20 * 3

        print("RT20 value:", rt20)
        print("RT60 value:", rt60)

        
        print("Storing results in dictionary")

        # Storing results
        data_dict["actual_freq"] = freq
        data_dict["amplitudes"] = amplitudes
        data_dict["max_amplitude"] = max_amplitude
        data_dict["top_RT20_amplitude"] = top_RT20_amplitude
        data_dict["bottom_RT20_amplitude"] = bottom_RT20_amplitude
        data_dict["top_RT20_time"] = self.times[top_RT20_index]
        data_dict["bottom_RT20_time"] = self.times[bottom_RT20_index]
        data_dict["RT20"] = rt20
        data_dict["RT60"] = rt60
        data_dict["max_amplitude_index"] = max_amplitude_index
        data_dict["top_RT20_index"] = top_RT20_index
        data_dict["bottom_RT20_index"] = bottom_RT20_index


    # Finds the RT60 time for the low, mid, and high target freqencies 
    def find_frequency_RT60s(self):
        LOW_TARGET_FREQ = 200
        MID_TARGET_FREQ = 1600
        HIGH_TARGET_FREQ = 5000

        # Setting up dictionary list
        self.frequency_data = [{"target_freq": 0, "actual_freq": 0, "amplitudes": [], "max_amplitude": 0, "top_RT20_amplitude": 0, "bottom_RT20_amplitude": 0, "top_RT20_time": 0, "bottom_RT20_time": 0, "RT20": 0, "RT60": 0, "max_amplitude_index": 0, "top_RT20_index": 0, "bottom_RT20_index": 0} for f in range(0, 3)]

        self.frequency_data[0]["target_freq"] = LOW_TARGET_FREQ
        self.frequency_data[1]["target_freq"] = MID_TARGET_FREQ
        self.frequency_data[2]["target_freq"] = HIGH_TARGET_FREQ

        # Finding the RT60 times
        for f in self.frequency_data:
            self.find_RT60(f["target_freq"], f)

        # Finding the average RT60 time and the difference for .5 seconds
        self.avg_RT60 = sum(f["RT60"] for f in self.frequency_data) / len(self.frequency_data)

        print("The average RT60 is", self.avg_RT60, "seconds")

        self.difference = self.avg_RT60 - .5

        print("The difference is", self.difference, "seconds")


    # Gets the amplitude values for the audio waveform
    def plot_wave(self):
        self.f = wave.open("output.wav", 'r')
        self.sig = np.frombuffer(self.f.readframes(self.sample_rate), dtype=np.int16)