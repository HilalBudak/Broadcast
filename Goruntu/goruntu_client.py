import cv2
import numpy as np
import socket
import sys
import getopt
import pickle
import struct
from thread import *

HOST = sys.argv[1]
PORT = int(sys.argv[2])
BUFFER_SIZE = 4096

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((HOST, PORT))
print 'connected to :',HOST,':',str(PORT)

data = b''
payload_size = struct.calcsize("L")

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
