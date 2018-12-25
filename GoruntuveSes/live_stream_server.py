import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import pyaudio
import Queue
from thread import *

HOST = sys.argv[1]
PORT = int(sys.argv[2])
CHUNK = 8196
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WIDTH = 2
IP_GROUP = {'127.0.0.1','IP'}
ENABLE_GROUP = int(sys.argv[3])

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Video Socket created')
s.bind((HOST, PORT))
print('Video Socket bind complete')
s.listen(10)
print('Video Socket now listening')


audiosocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Audio Socket created')
audiosocket.bind((HOST, PORT+1))
print('Audio Socket bind complete')
audiosocket.listen(10)
print('Audio Socket now listening')


cap = cv2.VideoCapture(0)

def video_thread(conn):
    while True:
        ret,frame = cap.read()
        data = pickle.dumps(frame)
        conn.sendall(struct.pack("L", len(data)) + data)

    conn.close()

def audio_thread(conn2):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stream.start_stream()

    while True:
        try:
            audio_data = stream.read(CHUNK)
        except Exception as e:
            print e
            audio_data = '\x00' * CHUNK

        conn2.sendall(audio_data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    conn2.close()


if ENABLE_GROUP == 1:
    print "Group Broadcasting Active"
elif ENABLE_GROUP == 0:
    print "Public Broadcasting Active"

while True:
    conn, addr = s.accept()
    conn2, addr2 = audiosocket.accept()

    if ENABLE_GROUP == 0:
        print("(Video Socket)Connection accepted from : " + addr[0] + ":" + str(addr[1]))
        start_new_thread(video_thread, (conn,))

        print("(Audio Socket)Connection accepted from : " + addr2[0] + ":" + str(addr2[1]))
        start_new_thread(audio_thread, (conn2,))
    elif ENABLE_GROUP == 1:
        available = False
        for IP in IP_GROUP:
            if addr[0] == IP:
                available = True

        if available == True:
            print("(Video Socket)Connection accepted from : " + addr[0] + ":" + str(addr[1]))
            start_new_thread(video_thread, (conn,))

            print("(Audio Socket)Connection accepted from : " + addr2[0] + ":" + str(addr2[1]))
            start_new_thread(audio_thread, (conn2,))
        elif available == False:
            print("Connection refused : " + addr[0] + ":" + str(addr[1]))
            conn.close()
            conn2.close()

s.close()
auidosocket.close()
