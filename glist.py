import sounddevice as sd
import numpy
assert numpy
import threading
import traceback

class SoundDuplicator():
    
    def __init__(self, input_dev_ID:int, output_IDs:tuple, error_callback, channels = 2):
        self.input_ID = input_dev_ID
        self.output_IDs = output_IDs
        self.channels = channels
        self.running = False
        self.error_callback = error_callback

    def __del__(self):
        self.kill_threads()

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)

        outdata[:] = indata

    def duplicate(self, ID:int, input_device, output_device, samplerate, blocksize, dtype, latency):
        try:
            print("thread started: ID: " + str(ID) + ", Device ID: " + str(output_device))
            with sd.Stream(device=(input_device, output_device), samplerate=samplerate, blocksize=blocksize, dtype=dtype, latency=latency,channels=2, callback=self.callback):
                print("Broadcasting to device: " + str(output_device) + ", from device: " + str(input_device))
                while self.running == True:
                    pass
        except Exception as exc:
            self.error_callback(traceback.format_exc())

    def kill_threads(self):
        self.running = False

        
    def start_duplication(self):
        self.running = True

        dev_num = len(self.output_IDs)
        self.output = [None] * dev_num

        for i in range(len(self.output_IDs)):
            if self.output_IDs[i] != -1:
                self.output[i] = threading.Thread(target = self.duplicate, args = (i, self.input_ID, self.output_IDs[i], None, 4100, None, None), daemon=True)
                self.output[i].start()
                    
        
        
        
