import pyaudio
import struct
import math
import pyautogui
import time

INITIAL_TAP = float(input("Enter amplitude : "))
global t1
t1 = time.time()
##########################################################################################################################
print('INITIAL_TAP :', INITIAL_TAP)
print('-------------------------------------------------------------------------')
delay = float(input("Enter delay(second)[for example if you want 0.5 second input is 0.5] : "))

print('-------------------------------------------------------------------------')
keys1 = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ]
keys2 = [')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', ]
keys3 = ['8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', ]
keys4 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', ]
keys5 = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', ]
keys6 = ['add', 'alt', 'altleft', 'altright', 'backspace', ]
keys7 = ['capslock', 'clear', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
         'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', ]

print('KEYS : ' + str(keys1) + '\n' + str(keys2) + '\n' + str(keys3) + '\n' + str(keys4) + '\n' + str(
    keys5) + '\n' + str(keys6) + '\n' + str(keys7) + '\n')
Press_key = input('Which key you want to press(for example a):  ')

print('-------------------------------------------------------------------------')
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0 / 32768.0)
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME
INDEX = 0


def get_rms(block):
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    return math.sqrt(sum_squares / count)


class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP
        self.noisycount = MAX_TAP_BLOCKS + 1
        self.quietcount = 0
        self.errorcount = 0
        self.index = INDEX

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        for i in range(self.pa.get_device_count()):
            dev = self.pa.get_device_info_by_index(i)
            print(dev['index'], dev['name'], 'hostApi=', dev['hostApi'])
        dev_index = int(input('please select index of {name=Stereo Mix (Conexant SmartAudio} with hostApi=0   :   '))
        # dev_index=2
        # for i in range(self.pa.get_device_count()):
        # dev = self.pa.get_device_info_by_index(i)
        # print(dev)
        # dev_index=int(input('please select index of {name=Stereo Mix (Conexant SmartAudio} with hostApi=0  : '))
        # if (dev['name'] == 'Stereo Mix (Conexant SmartAudio' and dev['hostApi'] == 0):
        # dev_index = dev['index'];
        # print('dev_index', dev_index)
        return dev_index

    def open_mic_stream(self):
        device_index = self.find_input_device()

        stream = self.pa.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              input_device_index=device_index,
                              frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self):  # DETECTED
        global t1
        print('t1', t1)
        t2 = time.time()
        print('time', t2)
        print('minus', time.time() - t1)
        if time.time() - t1 <delay:
            return
        t1 = t2

        print("tapped", self.index)
        pyautogui.press(Press_key)
        self.index += 1

    def listen(self):

        block = self.stream.read(INPUT_FRAMES_PER_BLOCK)

        amplitude = get_rms(block)
        print(amplitude)
        if amplitude > self.tap_threshold:
            self.tapDetected()


if __name__ == "__main__":
    tap_taster = TapTester()
    while True:
        tap_taster.listen()
