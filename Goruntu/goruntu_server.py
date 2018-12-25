import socket
import sys
import getopt
import cv2
import pickle
import numpy as np
import struct
from thread import *

HOST = sys.argv[1]
PORT = int(sys.argv[2])
IP_GROUP = {'127.0.0.1','IP'}
ENABLE_GROUP = int(sys.argv[3])

print('Video server started')
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

cap = cv2.VideoCapture(0)

def client_thread(conn):
    while True:
        ret,frame = cap.read()
        data = pickle.dumps(frame)
        conn.sendall(struct.pack("L", len(data)) + data)

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
