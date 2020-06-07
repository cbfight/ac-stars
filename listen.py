from matplotlib import pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation
from multiprocessing import Process, Queue
import queue as not_mp_q

duration = 60000 #milliseconds

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
    plotter(q)

def listen_handler(q):
    streaming_input(q)

def plotter(queue):
    print('plotter method')
    fig, ax1=plt.subplots()
    plt.grid()
    trace = ax1.plot(np.zeros((23,1)))
    ax1.set_xlim(-22050,22050) #nyquist window in hz
    ax1.set_ylim(-2,2) 
    animated = FuncAnimation(fig, lambda frame: animate_plot(frame, queue, trace), blit=True)
    plt.show()

def animate_plot(frame, queue, trace):
    while True:
        try:
            data = queue.get_nowait()
        except not_mp_q.Empty:
            #print('queue is empty!')
            break
        for column,line in enumerate(trace):
            #line.set_ydata(data[:,0])
            xdata,ydata = fft(data)
            xdata = np.multiply(xdata,44100)
            line.set_data(xdata,ydata)
    return trace
    
def streaming_input(queue):
    print('streaming input method')
    import sounddevice as sd
    sound_in = sd.InputStream(samplerate=44100,
                              blocksize=512,
                              device=0,
                              channels=1,
                              dtype=np.float32,
                              callback=lambda inframe, framecount, time, status: queue.put(inframe))
    with sound_in:
       sd.sleep(duration) #5 seconds duration

def fft(data):
    waveform = data.tolist()
    amplitude = np.fft.fft2(waveform)
    frequency = np.fft.fftfreq(len(waveform))
    return frequency,amplitude

if __name__ == '__main__':
    main()