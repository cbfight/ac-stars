import sounddevice
from matplotlib import pyplot as plt
import numpy as np
import time

class listener():
    def __init__(self):
        self.duration = 5 #seconds
        self.sr = 44100 #sample rate in hertz
        self.bs = 512 #chunk size
        self.stop_time = time.time()+5
        self.stream = sounddevice.Stream(samplerate=self.sr, blocksize= self.bs)

        with self.stream:
            while time.time() < self.stop_time:
                time.sleep(1)


foo = listener()
foo
print("done!")