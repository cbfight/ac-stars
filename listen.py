import sounddevice
from matplotlib import pyplot as plt
import numpy as np
import time
import queue
from matplotlib.animation import FuncAnimation

class listener():
    def __init__(self):
        self.duration = 5 #seconds
        self.sr = 44100 #sample rate in hertz
        self.bs = 512 #chunk size
        self.stop_time = time.time()+5
        self.stream = sounddevice.InputStream(samplerate=self.sr, blocksize=self.bs, callback=self.callback)
        self.q = queue.Queue()
        self.init_data = np.zeros((self.bs,1))
        self.fig, self.ax = plt.subplots()
        self.trace = self.ax.plot(self.init_data)
        self.animation = FuncAnimation(self.fig, self.update_plot, blit=True)
    def start_listening(self):
        with self.stream:
            plt.show()
            while time.time() < self.stop_time:
                time.sleep(1)
    def callback(self, indata, frames, time, status):
        'recieves chunks from stream, puts in queue'
        self.q.put(indata.copy())
    def update_plot(self,frame):
        while True:
            try:
                data = self.q.get_nowait()
            except queue.Empty:
                break
            for column, line in enumerate(self.trace):
                line.set_ydata(data[:,0])
        return self.trace

        


foo = listener()
print('listening!')
foo.start_listening()
print("done listening!")