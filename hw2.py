import scipy.fft as fft
import scipy.io.wavfile as wav
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from time import time
from math import sin, pi

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

def filtraggio_filtro_1(rate, data):
    T = 0.01
    N = int(rate * T)  #numero di campioni
    h = np.ones(N) / N   #porta discreta di durata T
    y = np.convolve(data, h)  #convoluzione
    return y

def filtro1(rate, data):
    uscita = filtraggio_filtro_1(rate, data)
    file_output = "output1.wav"
    wav.write(file_output, rate, np.int16)  #errore da risolvere
    outrate, outdata = wav.read(file_output)
    plot_waveform(outrate, outdata)

def sinc(t):
    if (t == 0):
        return 1
    return (sin(pi*t))/(pi*t)

def filtro3_tempo(t, B, r):
    ris = -2*B*sinc((t-r)*2*B)
    if (t == r):
        ris += 1
    return ris

def filtro3(rate, data):
    nH = int(5E3)
    h = []
    B = 1E3
    r = nH/(2*rate)
    for i in range(nH):
        h.append(filtro3_tempo(i/rate, B, r))

    # plt.plot(np.linspace(0, (nH-1)/rate, nH), h)
    # plt.grid(True)
    # plt.show()
    h = np.array(h)
    y = np.convolve(data, h, "same")
    # sd.play(y, rate)
    # sd.wait()

    calcolo_fft_libreria([data],rate)
    calcolo_fft_libreria([y],rate)

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

def divisione_audio(rate, data, M):
    """
    Divisione del segnale audio in sezioni di M secondi

    Args:
        rate: frequenza di campionamento del segnale audio 
        data: contenuto del segnale audio
        M (integer): durata in secondi di ogni sezione

    Returns:
        sezioni (list): lista di sezioni di M secondi
    """

    campioni_per_sezione = rate*M # numero di campioni per sezione
    num_sezioni = (data.shape[0]//campioni_per_sezione) + 1# numero di sezioni
    
    sezioni = []
    for i in range(num_sezioni):
        inizio = i * campioni_per_sezione # inizio della sezione
        fine = (i+1) * campioni_per_sezione # fine della sezione
        sezioni.append(data[inizio:fine]) # aggiungo la sezione 

    return sezioni


def calcolo_fft_libreria(segmenti, rate):
    """
    Calcolo della FFT del segnale audio con la libreria scipy

    Args:
        segmenti (list): lista di sezioni di M secondi
    """

    for i,segmento in enumerate(segmenti):
        start = time()
        fft_segmento = fft.fft(segmento) #calcolo fft del segmento
        stop = time()
        print("Tempo di esecuzione:", stop-start)
        freq_segmento = fft.fftfreq(len(segmento), d=1/rate) / 1000  #calcolo frequenze 
        ampiezza_segmento = np.abs(fft_segmento) / len(segmento) #calcolo ampiezze
        plot_fft(freq_segmento, ampiezza_segmento, i+1)

def main():
    FILENAME = "halleluja.wav" # nome del file audio

    # rate è la frequenza di campionamento
    # data è una matrice di 2 colonne (perchè il file è stereo) e tante 
    # righe quante sono i campioni
    # data.shape() restituisce il numero di righe e colonne della matrice
    rate, data = wav.read(FILENAME)
    
    if data.shape[1] == 2:
        data = np.mean(data, axis=1).astype(data.dtype) # converte il segnale stereo in mono

    # sd.play(data, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio  

    #plot_waveform(rate, data)
    
    plot_fft(data, rate, "FFT segnale audio")

    y = passa_basso_sinc(rate, data)

    # sd.play(y, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio
    
    plot_fft(y, rate, "FFT segnale audio filtrato")

    return 0

main()
