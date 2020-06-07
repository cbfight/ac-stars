import sounddevice as sd
from matplotlib import pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation
from multiprocessing import Process, Queue
import queue as not_mp_q

duration = 60000 #milliseconds
fig, ax, trace = 0,0,0 #initializing?

def main():
    print('main method')
    stack = Queue()
    q = Process(target = listen_handler, args=(stack,))
    z = Process(target = plot_handler, args=(stack,))
    z.start()
    q.start()
    q.join()
    z.join()

def plot_handler(q):
    global stack
    stack = q
    plotter()

def listen_handler(q):
    global stack
    stack = q
    streaming_input()

def plotter():
    global fig, ax, trace
    print('plotter method')
    fig, ax1=plt.subplots()
    trace = ax1.plot(np.zeros((23,1)))
    ax1.set_xlim(-22050,22050)
    ax1.set_ylim(-2,2)
    animated = FuncAnimation(fig, animate_plot,blit=True)
    plt.show()

def animate_plot(frame):
    global stack
    while True:
        try:
            data = stack.get_nowait()
        except not_mp_q.Empty:
            print('queue is empty!')
            break
        for column,line in enumerate(trace):
            #line.set_ydata(data[:,0])
            xdata,ydata = fft(data)
            xdata = np.multiply(xdata,44100)
            line.set_data(xdata,ydata)
    return trace

def stream_callback(inframe, framecount, time, status):
    global stack
    stack.put(inframe)
    
def streaming_input():
    print('streaming input method')
    sound_in = sd.InputStream(samplerate=44100,
                              blocksize=512,
                              device=0,
                              channels=1,
                              dtype=np.float32,
                              callback=stream_callback)
    with sound_in:
       sd.sleep(duration) #5 seconds duration

def fft(data):
    waveform = data.tolist()
    amplitude = np.fft.fft2(waveform)
    frequency = np.fft.fftfreq(len(waveform))
    return frequency,amplitude

if __name__ == '__main__':
    main()