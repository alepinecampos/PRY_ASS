import tkinter as tk
from tkinter import Label, ttk
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import os
import numpy as np
from thinkdsp import read_wave
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('1300x700')
root.configure(background='#b3ccff')
tabControl= ttk.Notebook(root)
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)
tab3=ttk.Frame(tabControl)
tab4=ttk.Frame(tabControl)
tab5=ttk.Frame(tabControl)
tab6=ttk.Frame(tabControl)
tabControl.add(tab1, text='Grabar')
tabControl.add(tab2, text='Datos')
tabControl.add(tab3, text='Filtros')
tabControl.add(tab4, text='Resultado #1')
tabControl.add(tab5, text='Resultado #2')
tabControl.add(tab6, text='Resultado #3')
tabControl.pack(expand=1,fill="both")

#Variable global para control de etiqueta de cada grabación
global etiqueta
etiqueta=0
global durations
durations=[0,1,2,3,4,5,6,7,8]
global sBox6
global sBox7

#Función para iniciar grabación 
def StartRecording():
    global etiqueta
    etiqueta+=1
    H=int(sBox1.get())*60*60
    M=int(sBox2.get())*60
    S=int(sBox3.get())
    global durations
    durations.append(sBox1.get()) #Adds duration of recording to array for further use
    durations.append(sBox2.get()) #Adds duration of recording to array for further use
    durations.append(sBox3.get()) #Adds duration of recording to array for further use
    fs = 46100 #Sample Rate
    seconds = (H+M+S) #Duration of recording
    recording = sd.rec(int(seconds*fs), samplerate=fs, channels=2,dtype=np.int16)
    sd.wait() #Wait until recording is finished
    write('outputRecording'+str(etiqueta)+'.wav',fs,recording) #Saves recording as WAV file in the same folder where this solution  is stored

#Funcion para abrir explorador de archivos en el directorio de la solución actual
def OpenPath(event):
    os.startfile(os.getcwd())

#Función para mostrar duración de cada grabación
def ShowDuration(x):
    if x==1:
        label = Label(frame4, text='Horas: '+durations[x-1]+'\n'+'Minutos: '+durations[x]+'\n'+'Segundos: '+durations[x+1])
        label.grid(row=x, column=1, sticky="nsew", padx=1, pady=1)
    
    if x==2:
        label = Label(frame4, text='Horas: '+durations[x+1]+'\n'+'Minutos: '+durations[x+2]+'\n'+'Segundos: '+durations[x+3])
        label.grid(row=x, column=1, sticky="nsew", padx=1, pady=1)
    
    if x==3:
        label = Label(frame4, text='Horas: '+durations[x+3]+'\n'+'Minutos: '+durations[x+4]+'\n'+'Segundos: '+durations[x+5])
        label.grid(row=x, column=1, sticky="nsew", padx=1, pady=1)
    
#Funcion para guardar figuras de onda y mostrarlas(#1)
def Save_Show_Wave_Spec(x):
    WaveIn = read_wave('outputRecording'+str(x)+'.wav')
    WaveIn.plot(color='#66a3ff')
    plt.xlabel('Tiempo (s)')
    plt.title('Onda #'+str(x))
    plt.grid(True)
    plt.savefig('Wave'+str(x)+'.png')
    plt.clf()
    SpecIn = WaveIn.make_spectrum()
    SpecIn.plot(color='#ff471a')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Espectro #'+str(x))
    plt.grid(True)
    plt.savefig('Spectrum'+str(x)+'.png')
    plt.clf()
    #WaveImage
    wIn_Img=Image.open('Wave'+str(x)+'.png')
    wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
    render1=ImageTk.PhotoImage(wIn_Img)
    wIn_Label = Label(frame4,image=render1)
    wIn_Label.image = render1
    wIn_Label.grid(row=x, column=5, sticky="nsew", padx=1, pady=1)
    #SpectrumImage
    sIn_Img=Image.open('Spectrum'+str(x)+'.png')
    sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
    render2=ImageTk.PhotoImage(sIn_Img)
    sIn_Label = Label(frame4,image=render2)
    sIn_Label.image=render2
    sIn_Label.grid(row=x, column=6, sticky="nsew", padx=1, pady=1)
    ShowDuration(x)
    SegmentControls()

#Función para filtrado de señal
def FiltrarS(S,F):
    #Señales
    if (S==1) and (F==1):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.low_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)
        
    if (S==1) and (F==2):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.high_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==1) and (F==3):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.band_stop(100,200)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)
    
    if (S==2) and (F==1):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.low_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==2) and (F==2):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.high_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==2) and (F==3):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.band_stop(100,200)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==3) and (F==1):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.low_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==3) and (F==2):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.high_pass(100)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

    if (S==3) and (F==3):
        SFiltrar=read_wave('outputRecording'+str(S)+'.wav')
        EspFiltrar= SFiltrar.make_spectrum()
        EspFiltrar.band_stop(100,200)#Cambiar segun filtro
        SFiltrada= EspFiltrar.make_wave()
        SFiltrada.normalize()
        #Guardado y Mostrado de resultados
        SFiltrada.plot(color='#66a3ff')
        plt.xlabel('Tiempo (s)')
        plt.title('Onda Filtrada')
        plt.grid(True)
        plt.savefig('Filtered_Wave.png')
        plt.clf()
        EspFiltrar.plot(color='#ff471a')
        plt.xlabel('Frecuencia (Hz)')
        plt.title('Espectro Filtrado')
        plt.grid(True)
        plt.savefig('Filtered_Spectrum.png')
        plt.clf()
        #FilteredWaveImage
        wIn_Img=Image.open('Filtered_Wave.png')
        wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
        render1=ImageTk.PhotoImage(wIn_Img)
        wIn_Label = Label(frame7,image=render1)
        wIn_Label.image = render1
        wIn_Label.grid(row=1, column=5, sticky="nsew", padx=1, pady=1)
        #FilteredSpectrumImage
        sIn_Img=Image.open('Filtered_Spectrum.png')
        sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
        render2=ImageTk.PhotoImage(sIn_Img)
        sIn_Label = Label(frame7,image=render2)
        sIn_Label.image=render2
        sIn_Label.grid(row=1, column=6, sticky="nsew", padx=1, pady=1)

#Función para controles para extracción de segmento
def SegmentControls():
    #Columna #7(Controles para extraer segmentos)#Resultados_1
    label=Label(frame7, text="A continuación se presentan algunos controles\n para extraer un segmento de la señal", bg="#b3ccff")
    label.grid(row=0, column=7, sticky="nsew", padx=1, pady=1)
    label=Label(frame7, text="Seleccione inicio", bg="#b3ccff")
    label.grid(row=1, column=7, sticky="nsew", padx=1, pady=1)
    global sBox6
    sBox6 = tk.Spinbox(frame7, from_=0,to=((durations[0]*60*60)+(durations[1]*60)+(durations[2])),wrap=True) #Inicio
    sBox6.grid(row=2, column=7, sticky="nsew", padx=1, pady=1)
    label=Label(frame7, text="Seleccione duración", bg="#b3ccff")
    label.grid(row=3, column=7, sticky="nsew", padx=1, pady=1)
    global sBox7
    sBox7 = tk.Spinbox(frame7, from_=0,to=((durations[0]*60*60)+(durations[1]*60)+(durations[2])),wrap=True) #Duración
    sBox7.grid(row=4, column=7, sticky="nsew", padx=1, pady=1)
    btn4 = tk.Button(frame7, text="Show Segment")
    btn4.grid(row=5, column=7, sticky="nsew", padx=1, pady=1,command= lambda: Make_ShowSegment_1())

#Función para mostrar segmentos
def Make_ShowSegment_1():
    WaveIn = read_wave('outputRecording1.wav')
    Seg1= WaveIn.segment(start=int(sBox6.get()),duration=int(sBox7.get()))
    Seg1.plot(color='#66a3ff')
    plt.xlabel('Tiempo (s)')
    plt.title('Segmento Onda Filtrada #1')
    plt.grid(True)
    plt.savefig('TestResultadoFiltrado_O1.png')
    plt.clf()
    SpecSeg1 = Seg1.make_spectrum()
    SpecSeg1.plot(color='#ff471a')
    plt.xlabel('Frecuencia (Hz)')
    plt.title('Segmento Espectro Filtrado #1')
    plt.grid(True)
    plt.savefig('TestResultadoFiltrado_S1.png')
    plt.clf()
    #WaveImage
    label = Label(frame7, text="Segmento Filtrado")
    label.grid(row=2, column=5, sticky="nsew", padx=1, pady=1)
    label = Label(frame7, text="Segmento Filtrado")
    label.grid(row=2, column=6, sticky="nsew", padx=1, pady=1)
    wIn_Img=Image.open('TestResultadoFiltrado_O1.png')
    wIn_Img = wIn_Img.resize((int((wIn_Img.width)-((wIn_Img.width)*0.5)),int((wIn_Img.height)-((wIn_Img.height)*0.5))), Image.ANTIALIAS)
    render1=ImageTk.PhotoImage(wIn_Img)
    wIn_Label = Label(frame7,image=render1)
    wIn_Label.image = render1
    wIn_Label.grid(row=3, column=5, sticky="nsew", padx=1, pady=1)
    #SpectrumImage
    sIn_Img=Image.open('TestResultadoFiltrado_S1.png')
    sIn_Img = sIn_Img.resize((int((sIn_Img.width)-((sIn_Img.width)*0.5)),int((sIn_Img.height)-((sIn_Img.height)*0.5))), Image.ANTIALIAS)
    render2=ImageTk.PhotoImage(sIn_Img)
    sIn_Label = Label(frame7,image=render2)
    sIn_Label.image=render2
    sIn_Label.grid(row=3, column=6, sticky="nsew", padx=1, pady=1)

  


#Frame, for recording controls and button
frame = tk.Frame(tab1, bg='#b3ccff', bd=1)
frame.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.1)

#Frame, for signal description
frame4 = tk.Frame(tab2, bg='#b3ccff', bd=1)
frame4.place(relx=0, rely=0, relwidth=1.2, relheight=1.3)

#Frames, for filter description
frame6 = tk.Frame(tab3, bg='#b3ccff', bd=1)#Titulo Filtros
frame6.place(relx=0, rely=0, relwidth=0.4, relheight=0.06)

frame3 = tk.Frame(tab3, bg='#b3ccff', bd=1)#Info Filtros
frame3.place(relx=0, rely=0.05, relwidth=0.4, relheight=1.3)

frame5 = tk.Frame(tab3, bg='#b3ccff', bd=1)#SpinBoxes Filtros
frame5.place(relx=0.4, rely=0, relwidth=0.8, relheight=1.3)

#Frame, for filtered results
frame7 = tk.Frame(tab4, bg='#b3ccff', bd=1)
frame7.place(relx=0, rely=0, relwidth=1.2, relheight=1.3)


#-----------------------------------------------------------Pestaña-Grabar-----------------------------------------------------------------------#
#------------------------------------FRAME #1------------------------------------------#
#Creates Button
btn = tk.Button(frame, text="Iniciar Grabación", command= lambda: StartRecording())
btn.place(relx=0, rely=0.35, relwidth=0.40, relheight=0.35)
#Creating SpinBoxes & labels 
sBox1= tk.Spinbox(frame, from_=0,to=59,wrap=True) #Horas
sBox1.place(relx=0.45, rely=0.35, relwidth=0.15, relheight=0.33)
label=Label(frame, text="Hrs", bg="#b3ccff")
label.place(relx=0.45, rely=0)
sBox2= tk.Spinbox(frame, from_=0,to=59,wrap=True) #Minutos
sBox2.place(relx=0.63, rely=0.35, relwidth=0.15, relheight=0.33)
label=Label(frame, text="Mins", bg="#b3ccff")
label.place(relx=0.63, rely=0)
sBox3= tk.Spinbox(frame, from_=0,to=59,wrap=True) #Segundos
sBox3.place(relx=0.81, rely=0.35, relwidth=0.15, relheight=0.33)
label=Label(frame, text="Segs", bg="#b3ccff")
label.place(relx=0.81, rely=0)

#-----------------------------------------------------------Pestaña-Filtros-----------------------------------------------------------------------#
#----------------------------------FRAME #6--------------------------------------------#
#Descripciones de filtros
label = Label(frame6, text="A continuación se presenta un listado de los \nfiltros disponibles con una breve descripción:", bg="#b3ccff")
label.place(relx=0, rely=0)
#----------------------------------FRAME #3--------------------------------------------#
#'Tabla' para mostrar información de filtros disponibles
label = Label(frame3, text="Título")
label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Filtro #1 Filtro Pasa Bajo")
label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Filtro #2 Filtro Pasa Alto")
label.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Filtro #3 Filtro Pasa Banda")
label.grid(row=3, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Descripción")
label.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Idealmente, un filtro pasa bajo corta  \n todas las frecuencias mayores a una frecuencia de corte νc  \n y permite el paso de las frecuencias menores,  \n sin cambio alguno (por eso se llama pasa bajo")
label.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Idealmente, un filtro pasa alto corta  \n todas las frecuencias menores a una frecuencia de corte νc  \n y permite el paso de las frecuencias mayores,  \n sin cambio alguno (por eso se llama pasa alto")
label.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)
label = Label(frame3, text="Un Filtro pasa banda, \n permite pasar algunas frecuencias sin alterarlas, eliminando otras.\n Centramos nuestro filtro en ±ν0 \n y cortamos las frecuencias νc por arriba y por debajo de ν0±νc." )
label.grid(row=3, column=1, sticky="nsew", padx=1, pady=1)

#----------------------------------FRAME #5--------------------------------------------#
#Selección de filtro y señal a filtrar
# F = ["Filtro #1","Filtro #2","Filtro #3"]
# S = ["Señal #1","Señal #2","Señal #3"]
#Creating SpinBoxes
sBox4= tk.Spinbox(frame5, from_=0,to=3,wrap=True) #Señales
sBox4.place(relx=0.12, rely=0.01, relwidth=0.1, relheight=0.02)
label=Label(frame5, text="Seleccione la señal \nque desea filtrar:", bg="#b3ccff")
label.place(relx=0, rely=0)
sBox5= tk.Spinbox(frame5, from_=0,to=3,wrap=True) #Filtros
sBox5.place(relx=0.15, rely=0.1, relwidth=0.1, relheight=0.02)
label=Label(frame5, text="Seleccione filtro para filtrar \nla señal seleccionada:", bg="#b3ccff")
label.place(relx=0, rely=0.09)
#Creating Filter Button
btn8 = tk.Button(frame5, text="Filtrar", command= lambda: FiltrarS(int(sBox4.get()),int(sBox5.get())))
btn8.place(relx=0.05, rely=0.14, relwidth=0.04, relheight=0.04)

#-----------------------------------------------------------Pestaña-Datos-----------------------------------------------------------------------#
#----------------------------------FRAME #4--------------------------------------------#
#Creates Grid for signals info.
#Columna #0(Título)
label = Label(frame4, text="Título")
label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame4, text="Señal #1")
label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame4, text="Señal #2")
label.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame4, text="Señal #3")
label.grid(row=3, column=0, sticky="nsew", padx=1, pady=1)
#Columna #1(Duración)
label = Label(frame4, text="Duraciones")
label.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
#Columna #2(Ubicación)
label = Label(frame4, text="Ubicación")
label.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
labelx = Label(frame4, text='Ubicación #1') #Señal 1
labelx.grid(row=1, column=2, sticky="nsew", padx=1, pady=1)
labelx.bind("<Button>",OpenPath)
labelx = Label(frame4, text='Ubicación #2') #Señal 2
labelx.grid(row=2, column=2, sticky="nsew", padx=1, pady=1)
labelx.bind("<Button>",OpenPath)
labelx = Label(frame4, text='Ubicación #3') #Señal 3
labelx.grid(row=3, column=2, sticky="nsew", padx=1, pady=1)
labelx.bind("<Button>",OpenPath)
#Columna #3(Botón de play)
label = Label(frame4, text="Reproducir Señal")
label.grid(row=0, column=3, sticky="nsew", padx=1, pady=1)
btn2 = tk.Button(frame4, text="Play Signal #1")
btn2.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)
btn3 = tk.Button(frame4, text="Play Signal #2")
btn3.grid(row=2, column=3, sticky="nsew", padx=1, pady=1)
btn4 = tk.Button(frame4, text="Play Signal #3")
btn4.grid(row=3, column=3, sticky="nsew", padx=1, pady=1)
#Columna #4(Botones para mostrar onda y espectro)
label = Label(frame4, text="Mostrar Datos")
label.grid(row=0, column=4, sticky="nsew", padx=1, pady=1)
btn5 = tk.Button(frame4, text="Mostrar Datos #1", command= lambda: Save_Show_Wave_Spec(1))
btn5.grid(row=1, column=4, sticky="nsew", padx=1, pady=1)
btn6 = tk.Button(frame4, text="Mostrar Datos #2", command= lambda: Save_Show_Wave_Spec(2))
btn6.grid(row=2, column=4, sticky="nsew", padx=1, pady=1)
btn7 = tk.Button(frame4, text="Mostrar Datos #3", command= lambda: Save_Show_Wave_Spec(3))
btn7.grid(row=3, column=4, sticky="nsew", padx=1, pady=1)
#Columna #5(Onda antes del filtro)
label = Label(frame4, text="Onda Original")
label.grid(row=0, column=5, sticky="nsew", padx=1, pady=1)
#Columna #7(Espectro antes del filtro)
label = Label(frame4, text="Espectro Original")
label.grid(row=0, column=6, sticky="nsew", padx=1, pady=1)

#-----------------------------------------------------------Pestaña-Resultados#1-----------------------------------------------------------------------#
#----------------------------------FRAME #7--------------------------------------------#
#Creates Grid for signals info.
#Columna #0(Título)
label = Label(frame7, text="Título")
label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
label = Label(frame7, text="Señal Filtrada #1")
label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
#Columna #1(Duración)
label = Label(frame7, text="Duración")
label.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
#Columna #2(Ubicación)
label = Label(frame7, text="Ubicación")
label.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
labelx = Label(frame7, text='Ubicación') 
labelx.grid(row=1, column=2, sticky="nsew", padx=1, pady=1)
labelx.bind("<Button>",OpenPath)
#Columna #3(Botón de play)
label = Label(frame7, text="Reproducir Señal")
label.grid(row=0, column=3, sticky="nsew", padx=1, pady=1)
btn9 = tk.Button(frame7, text="Play Filtered Signal #1")
btn9.grid(row=1, column=3, sticky="nsew", padx=1, pady=1)
#Columna #4(Botones para mostrar onda y espectro)
label = Label(frame7, text="Mostrar Datos")
label.grid(row=0, column=4, sticky="nsew", padx=1, pady=1)
btn10 = tk.Button(frame7, text="Mostrar Datos")#Añadir parametro command para mostrar datos
btn10.grid(row=1, column=4, sticky="nsew", padx=1, pady=1)
#Columna #5(Onda despues del filtro)
label = Label(frame7, text="Onda Filtrada")
label.grid(row=0, column=5, sticky="nsew", padx=1, pady=1)
#Columna #6(Espectro despues del filtro)
label = Label(frame7, text="Espectro Filtrado")
label.grid(row=0, column=6, sticky="nsew", padx=1, pady=1)




root.mainloop()
