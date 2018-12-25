import socket
import sys
import pyaudio
import Queue

CHUNK = 8196
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WIDTH = 2

HOST = sys.argv[1]
PORT = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print 'Connected to :',HOST

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
    q = Queue.Queue()

    frames = []

    stream.start_stream()

    data = s.recv(CHUNK)

    while data != '':
        q.put(data)
        if not q.empty():
            stream.write(q.get())

        data = s.recv(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()


if __name__ == '__main__':
    main()
