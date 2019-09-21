import webrtcvad
import numpy as np
import threading
import pyaudio
import queue
from gcc_phat import gcc_phat
import math
from mic_array import MicArray


RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms
SOUND_SPEED = 343.2

MIC_DISTANCE_6P1 = 0.064
MAX_TDOA_6P1 = MIC_DISTANCE_6P1 / float(SOUND_SPEED)

MIC_DISTANCE_4 = 0.08127
MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)


class DOA_capture(object):

    def __init__(self,):
        self.vad = webrtcvad.Vad(3)
        self.speech_count = 0
        self.chunks = []
        self.doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
        self.direction = 0
        self.availability=0

    def run(self):
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            # this method first recognise speech audio chunck, 
            # accumulate them up to 20, and predict the DOA based on the speech chunk
            for chunk in mic.read_chunks():
#                print(chunk)
                # Use single channel audio to detect voice activity
                if self.vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
#                    print("speech")
                    self.speech_count += 1


                self.chunks.append(chunk)
#                print(len(self.chunks))
#                print("self chunk: {}, DOA chunk: {}".format(len(self.chunks),self.doa_chunks))
                if len(self.chunks) == self.doa_chunks:
#                    print("enough chunk")
                    if self.speech_count > (self.doa_chunks / 2):
                        frames = np.concatenate(self.chunks)
                        self.direction = mic.get_direction(frames)
                        self.availability=1
    #                        print('\n{}'.format(int(direction)))

                    self.speech_count = 0
                    self.chunks=[]



def main():
    DOA_algorithm= DOA_capture()
    T=threading.Thread(target=DOA_algorithm.run)
    T.start()
    print("thread started successfully")
    while DOA_algorithm.availability:
        print("Voice coming from {}".format(int(DOA_algorithm.direction)))
#        DOA_algorithm.availability=0

if __name__ == '__main__':
    main()
