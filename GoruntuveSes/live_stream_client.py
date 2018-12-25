import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import pyaudio
import Queue
from thread import *
import threading

HOST = sys.argv[1]
PORT = int(sys.argv[2])
CHUNK = 8196
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WIDTH = 2
BUFFER_SIZE = 4096

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientsocket.connect((HOST, PORT))
    print 'connected to :',HOST,':',str(PORT)
except Exception as e:
    print e
    sys.exit()

audiosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    audiosocket.connect((HOST, PORT+1))
    print 'connected to :',HOST,':',str(PORT+1)
except Exception as e:
    print e
    sys.exit()


def video_thread(clientsocket):
    data = b''
    payload_size = struct.calcsize("L")

    data = clientsocket.recv(BUFFER_SIZE)

    while True:
        while len(data) < payload_size:
            data += clientsocket.recv(BUFFER_SIZE)
        packed_msg_size = data[:payload_size]

        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += clientsocket.recv(BUFFER_SIZE)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data)
        cv2.imshow('Video Feed', frame)
        cv2.waitKey(10)

def audio_thread(audiosocket):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
    q = Queue.Queue()

    frames = []

    stream.start_stream()

    audio_data = audiosocket.recv(CHUNK)

    while audio_data != '':
        q.put(audio_data)
        if not q.empty():
            stream.write(q.get())

        audio_data = audiosocket.recv(CHUNK)
        frames.append(audio_data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    audiosocket.close()


thread1 = threading.Thread(target=audio_thread, args=(audiosocket,))
thread2 = threading.Thread(target=video_thread, args=(clientsocket,))

# Will execute both in parallel
thread1.start()
thread2.start()

# Joins threads back to the parent process, which is this program
thread1.join()
thread2.join()
