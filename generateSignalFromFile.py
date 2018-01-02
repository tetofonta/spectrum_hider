import math
import wave
import struct
import sys
import os
from scipy import signal

preamble = 0 * 88200
datatime = 0
samples = []
last = 0

sin_intervals = [
    (2 * math.pi) / (88200 / 29000),
    (2 * math.pi) / (88200 / 30000),
    (2 * math.pi) / (88200 / 31000),
    (2 * math.pi) / (88200 / 32000),
    (2 * math.pi) / (88200 / 33000),
    (2 * math.pi) / (88200 / 34000),
    (2 * math.pi) / (88200 / 35000),
    (2 * math.pi) / (88200 / 36000),
    (2 * math.pi) / (88200 / 37000),
    (2 * math.pi) / (88200 / 38000),
    (2 * math.pi) / (88200 / 39000),
    (2 * math.pi) / (88200 / 40000),
    (2 * math.pi) / (88200 / 41000),
    (2 * math.pi) / (88200 / 42000),
    (2 * math.pi) / (88200 / 43000),
    (2 * math.pi) / (88200 / 44000)
]


def highpass_filter(y, sr, filter_stop_freq=28000, filter_pass_freq=29000, filter_order=1001):
    # High-pass filter
    nyquist_rate = sr / 2.
    desired = (0, 0, 1, 1)
    bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
    filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

    # Apply high-pass filter
    filtered_audio = signal.filtfilt(filter_coefs, [1], y)
    return filtered_audio


def writeByte(byte, duration):
    global last
    global datatime
    datatime += duration
    phase = math.asin(last)
    mylist = []
    for i in range(0, duration): mylist.append(0)

    trues = 0
    for idx in range(0, 8):
        if ((byte >> idx) & 0x01) == 1:
            trues += 1
            for i in range(0, duration):
                mylist[i] += math.sin(i * sin_intervals[idx] + phase)

    for i in range(0, duration):
        mylist[i] /= trues
        last = mylist[i]
        mylist[i] *= 0x7FFF

    for i in mylist: samples.append(i)


def writeWord(byte, duration):
    global last
    global datatime
    datatime += duration
    phase = math.asin(last)
    mylist = []
    for i in range(0, duration): mylist.append(0)

    trues = 0
    for idx in range(0, 16):
        if ((byte >> idx) & 0x01) == 1:
            trues += 1
            for i in range(0, duration):
                mylist[i] += math.sin(i * sin_intervals[idx] + phase)

    for i in range(0, duration):
        mylist[i] /= trues
        last = mylist[i]
        mylist[i] *= 0x7FFF

    for i in mylist: samples.append(i)


out = wave.open("prova06.wav", "wb")
out.setparams((1, 2, 88200, 0, 'NONE', 'not compressed'))

file = open(sys.argv[1], "rb")
lenght = os.path.getsize(sys.argv[1])
readed = 0
while True:
    red = 'H'
    if lenght - readed >= 2:
         read = file.read(2)
         red = 'H'
    else:
         read = file.read(1)
         red = 'B'
    f = struct.unpack(red, read)[0] # B stands for unsigned char (8 bits)
    writeWord(f, 2000)
    readed += 2
    print(readed, " / ", lenght)
    if readed >= lenght:
        break
        
file.close()

output = []
for i in range(0, preamble): output.append(0)
for i in samples: output.append(i)

output = highpass_filter(output, 88200)

tooutput = []

for q in range(0, len(output)):
    ciao = int(round(output[q].item() * 0.3))
    try:
        tooutput.append(struct.pack('h', ciao))
    except:
        print(ciao)

tooutput = b''.join(tooutput)
out.writeframes(tooutput)
out.close()
