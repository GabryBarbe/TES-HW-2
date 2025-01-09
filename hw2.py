import scipy.fft as fft
import scipy.io.wavfile as wav
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from time import time
from math import sin, pi

def filtro1(rate, data):
    T = 0.01
    N = int(rate * T)  #numero di campioni
    h = np.ones(N) / N   #porta discreta di durata T
    h = np.append(h, np.zeros(4*N))
    y = np.convolve(data, h, "same")  #convoluzione
    return y

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

def filtro2(rate, data):
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

def filtro3_tempo(t, B, r):
    """funzione del filtro

    Args:
        t: tempo [s]
        B: Banda [Hz]
        r: ritardo [s]

    Returns:
        _type_: _description_
    """
    ris = -2*B*np.sinc((t-r)*2*B)
    if (t == r):
        ris += 1
    return ris

def filtro3(rate, data):
    """funzione generale del filtro 3

    Args:
        rate: frequenza di campionamento [Hz]
        data: dati file audio non filtrati
    """
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
    return y

def rumore_bianco(rate, durata):
    """
    Generazione di rumore bianco gaussiano

    Args:
        rate: frequenza di campionamento del segnale audio
        durata: durata del segnale audio

    Returns:
        n: rumore bianco gaussiano
    """
    n = np.random.randn(rate*durata)
    return n

def funzione_di_trasferimento(rate, uscita, durata):
    """
    Calcolo e plot della funzione di trasferimento

    Args:
        rate: frequenza di campionamento del segnale audio
        uscita: segnale audio in uscita filtrato
        durata: durata del file audio
    """
    n = rumore_bianco(rate, durata)
    
    min_len = min(len(n), len(uscita))
    n = n[:min_len]
    uscita = uscita[:min_len]

    fft_ingresso = fft.fft(n)
    fft_uscita = fft.fft(uscita)

    H = np.abs(fft_uscita) / np.abs(fft_ingresso)
    freq = fft.fftfreq(len(H), d=1/rate) / 1000  

    plt.plot(freq, H)
    plt.xlabel("Frequenza [kHz]")
    plt.ylabel("Ampiezza [dB]")
    plt.title("Funzione di trasferimento")
    plt.grid(True)
    plt.show()
    return H

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
<<<<<<< HEAD
=======
    M = 30 # durata in secondi del brano audio
>>>>>>> barbe

    # rate è la frequenza di campionamento
    # data è una matrice di 2 colonne (perchè il file è stereo) e tante 
    # righe quante sono i campioni
    # data.shape() restituisce il numero di righe e colonne della matrice
    rate, data = wav.read(FILENAME)
    
    if data.shape[1] == 2:
        data = np.mean(data, axis=1).astype(data.dtype) # converte il segnale stereo in mono

    # sd.play(data, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio  

<<<<<<< HEAD
    #plot_waveform(rate, data)
=======
    # plot_waveform(rate, data)
>>>>>>> barbe
    
    # plot_fft(data, rate, "FFT segnale audio")

    scelta = int(input("Inserire numero filtro da utilizzare: "))
    
    if (scelta == 1):
        y = filtro1(rate, data)
    elif (scelta == 2):
        y = filtro2(rate, data)
    elif (scelta == 3):
        y =  filtro3(rate, data)
    else:
        print("Nessun filtro con questo numero.")
        return 1
    
    # sd.play(y, rate)  # riproduce il file audio
    # sd.wait() # attende la fine esecuzione del file audio
    
    # plot_fft(y, rate, "FFT segnale audio filtrato")

    funzione_di_trasferimento(rate, y, M)

    return 0

main()
