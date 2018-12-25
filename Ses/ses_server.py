import socket
import wave
import pyaudio
import sys
from thread import *

CHUNK = 8196
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

HOST = sys.argv[1]
PORT = int(sys.argv[2])
IP_GROUP = {'127.0.0.1','IP'}
ENABLE_GROUP = int(sys.argv[3])

print('Audio server started')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')


def client_thread(conn):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stream.start_stream()

    while True:
        try:
            data = stream.read(CHUNK)
        except Exception as e:
            print e
            data = '\x00' * CHUNK

        conn.sendall(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()

if ENABLE_GROUP == 1:
    print "Group Broadcasting Active"
elif ENABLE_GROUP == 0:
    print "Public Broadcasting Active"

while True:
    conn, addr = s.accept()

    if ENABLE_GROUP == 0:
        print("Connection accepted from : " + addr[0] + ":" + str(addr[1]))
        start_new_thread(client_thread, (conn,))
    elif ENABLE_GROUP == 1:
        available = False
        for IP in IP_GROUP:
            if addr[0] == IP:
                available = True

        if available == True:
            print("Connection accepted from : " + addr[0] + ":" + str(addr[1]))
            start_new_thread(client_thread, (conn,))
        elif available == False:
            print("Connection refused : " + addr[0] + ":" + str(addr[1]))
            conn.close()

s.close()
