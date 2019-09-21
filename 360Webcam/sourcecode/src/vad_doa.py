
import sys
import webrtcvad
import numpy as np
from mic_array import MicArray
from pixel_ring import pixel_ring
from gpiozero import LED
import time

power = LED(5)
power.on()

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms


def main():
    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)

    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            a=[];
            for chunk in mic.read_chunks():
                # Use single channel audio to detect voice activity
                if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                    speech_count += 1
                    sys.stdout.write('1')
                else:
                    sys.stdout.write('0')

                sys.stdout.flush()

                chunks.append(chunk)
                if len(chunks) == doa_chunks:
                    if speech_count > (doa_chunks / 2):
                        frames = np.concatenate(chunks)
                        direction = mic.get_direction(frames)
                        if len(a)>2:
                            angle=[np.bincount(a).argmax()]
                            b=angle[0]
                        
                            position = int((b) / (360 / 12))
                            pixels = [0, 0, 0, 10] * 12
                            pixels[position * 4 + 2] = 10
                            pixel_ring.show(pixels)
                            print('\n{}'.format(int(b)))
                            a.remove(a[0])
                        else:
                            new_angle=angle_to_index_angle(direction);
                            a.append(new_angle);
                    speech_count = 0
                    chunks = []

    except KeyboardInterrupt:
        pass
        
    pixel_ring.off()

def angle_to_index_angle(angle):
    a=(int(angle/10))*10
    return a

if __name__ == '__main__':
    main()
