import pyaudio
import queue
import numpy as np
from gcc_phat import gcc_phat
import math


SOUND_SPEED = 343.2

MIC_DISTANCE_6P1 = 0.064
MAX_TDOA_6P1 = MIC_DISTANCE_6P1 / float(SOUND_SPEED)

MIC_DISTANCE_4 = 0.08127
MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)



class MicArray(object):

    def __init__(self, rate=16000, channels=8, chunk_size=None):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.queue = queue.Queue()
#        self.quit_event = threading.Event()
        self.channels = channels
        self.sample_rate = rate
        self.chunk_size = chunk_size if chunk_size else rate / 100
        self.frame=None

        device_index = None
        for i in range(self.pyaudio_instance.get_device_count()):
            dev = self.pyaudio_instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])
            if dev['maxInputChannels'] == self.channels:
                print('Use {}'.format(name))
                device_index = i
                break

        if device_index is None:
            raise Exception('can not find input device with {} channel(s)'.format(self.channels))

        self.stream = self.pyaudio_instance.open(
            input=True,
            start=True,
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=int(self.sample_rate),
            frames_per_buffer=int(self.chunk_size),
            stream_callback=self._callback,
            input_device_index=device_index,
        )
        print("mic array initiated")

    def _callback(self, in_data, frame_count, time_info, status):
#        print("get input",in_data)
        self.queue.put(in_data)
#        self.frame=in_data
        return None, pyaudio.paContinue

    def start(self):
#        print("start mic array")
        self.queue.queue.clear()
        self.stream.start_stream()
#        print("leave start")

    def read_direction(self):
#        print("in read direction!")
#        self.quit_event.clear()
#        print('quit event cleared')
        frames = self.queue.get()
        if frames:
#            print('frame available!')
            return self.get_direction(np.fromstring(frames, dtype='int16'))
        else:
            return None
        


    def read_chunks(self):
#        print("read chunks")
#        self.quit_event.clear()
        while 1:
            frames = self.queue.get()
#            print(frames)
            if not frames:
                break

            frames = np.fromstring(frames, dtype='int16')
            yield frames

    def stop(self):
#        self.quit_event.set()
        self.stream.stop_stream()
        self.queue.put('')

    def __enter__(self):
#        print("enter mic array")
        self.start()
#        print("leave mic array")
        return self

    def __exit__(self, type, value, traceback):
        if value:
            return False
        self.stop()

    def get_direction(self, buf):
#        print("got audio direction")
        best_guess = None
        if self.channels == 8:
            MIC_GROUP_N = 3
            MIC_GROUP = [[1, 4], [2, 5], [3, 6]]

            tau = [0] * MIC_GROUP_N
            theta = [0] * MIC_GROUP_N

            # buf = np.fromstring(buf, dtype='int16')
            for i, v in enumerate(MIC_GROUP):
                tau[i], _ = gcc_phat(buf[v[0]::8], buf[v[1]::8], fs=self.sample_rate, max_tau=MAX_TDOA_6P1, interp=1)
                theta[i] = math.asin(tau[i] / MAX_TDOA_6P1) * 180 / math.pi

            min_index = np.argmin(np.abs(tau))
            if (min_index != 0 and theta[min_index - 1] >= 0) or (min_index == 0 and theta[MIC_GROUP_N - 1] < 0):
                best_guess = (theta[min_index] + 360) % 360
            else:
                best_guess = (180 - theta[min_index])

            best_guess = (best_guess + 120 + min_index * 60) % 360
        elif self.channels == 4:
            MIC_GROUP_N = 2
            MIC_GROUP = [[0, 2], [1, 3]]

            tau = [0] * MIC_GROUP_N
            theta = [0] * MIC_GROUP_N
            for i, v in enumerate(MIC_GROUP):
                tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4], fs=self.sample_rate, max_tau=MAX_TDOA_4, interp=1)
                theta[i] = math.asin(tau[i] / MAX_TDOA_4) * 180 / math.pi

            if np.abs(theta[0]) < np.abs(theta[1]):
                if theta[1] > 0:
                    best_guess = (theta[0] + 360) % 360
                else:
                    best_guess = (180 - theta[0])
            else:
                if theta[0] < 0:
                    best_guess = (theta[1] + 360) % 360
                else:
                    best_guess = (180 - theta[1])

                best_guess = (best_guess + 90 + 180) % 360


            best_guess = (-best_guess + 120) % 360

             
        elif self.channels == 2:
            pass
#        print(best_guess)

        return best_guess

def test():
    mic_array=MicArray(16000,4,16000/4)
    while 1:
        sound_dir = mic_array.read_direction()
        if sound_dir:
            print(sound_dir)


def test_4mic():
    import signal
    import time

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
 
    with MicArray(16000, 4, 16000 / 4)  as mic:
        for chunk in mic.read_chunks():
            direction = mic.get_direction(chunk)
            print(int(direction))

            if is_quit.is_set():
                break


def test_8mic():
    import signal
    import time
    from pixel_ring import pixel_ring

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
 
    with MicArray(16000, 8, 16000 / 8)  as mic:
        for chunk in mic.read_chunks():
            direction = mic.get_direction(chunk)
            pixel_ring.set_direction(direction)
            print(int(direction))

            if is_quit.is_set():
                break

    pixel_ring.off()


if __name__ == '__main__':
    test_4mic()
#    test_8mic()
#    test()
#    print("hello")
