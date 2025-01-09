import scipy.fft as fft
import scipy.io.wavfile as wav
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from time import time

def filtro_sinc(B, rate):
    """
    Calcolo del filtro sinc nel dominio del tempo

    Args:
        B: banda del filtro
        rate: frequenza di camoionamento del segnale audio

    Returns:
        h: funzione sinc nel dominio del tempo
    """
    N=5E3
    T= N//2
    t = np.arange(0, N)/rate
    h = 2*B*np.sinc(2*B*(t-T/rate))
    # plot_fft(h, rate, "FFT filtro sinc")
    return h


def passa_basso_sinc(rate, data):
    """
    Applicazione del filtro passa basso sinc al segnale audio

    Args:
        rate: frequenza di campionamento del segnale audio
        data: contenuto del segnale audio

    Returns:
        y: segnale audio filtrato
    """
    B = 1000
    h = filtro_sinc(B, rate)
    y = np.convolve(data, h, mode='same')
    return y


def plot_waveform(rate, data):
    """
    Plot della waveform del segnale audio

    Args:
        rate: frequenza di campionamento del segnale audio
        data: contenuto del segnale audio
    """
    # La durata è il numero di righe (campioni) diviso la frequenza di campionamento
    durata = len(data)/ rate
    
    plt.plot(np.linspace(0, durata, data.shape[0]), data)
    plt.xlabel("Tempo [s]")
    plt.ylabel("Ampiezza [dB]")
    plt.title("Waveform del segnale audio")
    plt.grid(True)
    plt.show()  

def plot_fft(segnale, rate, descrizione):
    """
    Plot della FFT del segnale audio

    Args:
        segnale: segnale da analizzare
        rate: frequenza di campionamento del segnale audio
        descrizione: descrizione del plot
    """
    fft_segnale = fft.fft(segnale) #calcolo fft del segnale
    freq = fft.fftfreq(len(segnale), d=1/rate) / 1000  #calcolo frequenze 
    amp = np.abs(fft_segnale) / len(segnale) #calcolo ampiezze
    

    plt.plot(freq, amp)
    plt.xlabel("Frequenza [kHz]")
    plt.ylabel("Ampiezza [dB]")
    plt.suptitle(descrizione)
    plt.title("Spettro di energia")
    plt.grid(True)
    plt.show()
        


def main():
    FILENAME = "halleluja.wav" # nome del file audio
    M = 30 # durata in secondi di ogni sezione

    # rate è la frequenza di campionamento
    # data è una matrice di 2 colonne (perchè il file è stereo) e tante 
    # righe quante sono i campioni
    # data.shape() restituisce il numero di righe e colonne della matrice
    rate, data = wav.read(FILENAME)
    
    if data.shape[1] == 2:
        data = np.mean(data, axis=1).astype(data.dtype) # converte il segnale stereo in mono

    # sd.play(data, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio  

    plot_waveform(rate, data)
    
    plot_fft(data, rate, "FFT segnale audio")

    y = passa_basso_sinc(rate, data)

    # sd.play(y, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio
    
    plot_fft(y, rate, "FFT segnale audio filtrato")

    return 0

main()
