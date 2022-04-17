#!/usr/bin/env python3
import sys
import socket
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5001
FILENAME = 'tcp_log.csv'
HEADER_CSV = 'ID Device,MAC,ID Protocol,leng msg,Val: 1,Batt_level,Timestamp,Temp,Press,Hum,Co,RMS,Amp x,Frec x,Amp y,Frec y,Amp z,Frec z'
# LENGTH
ID_DEVICE = 2
MAC = 6
ID_PROTOCOL = 1
LENG_MSG = 2
DATA_1 = 1
DATA_2 = 1
DATA_3 = 4
DATA_4 = 1
DATA_5 = 4
DATA_6 = 1
DATA_N = 4

def open_file(file):
    try:
        f = open(file, 'r')
    except:
        f = open(file, 'w')
        f.write(HEADER_CSV+'\n')
    else:
        check = f.read(len(HEADER_CSV)) == HEADER_CSV
        if check:
            f = open(file, 'a')
        else:
            f = open(file, 'w')
            f.write(HEADER_CSV+'\n')
    finally:
        return f

def write_line(file, data):
    n = 0
    print(data)

    ###### HEADER ######
    # ID Device - 2 bytes
    file.write(str(int.from_bytes(data[n:n+ID_DEVICE], byteorder='little')))
    n += ID_DEVICE

    # MAC - 6 bytes
    file.write(','+str(data[n:n+1].hex()))
    file.write(':'+str(data[n+1:n+2].hex()))
    file.write(':'+str(data[n+2:n+3].hex()))
    file.write(':'+str(data[n+3:n+4].hex()))
    file.write(':'+str(data[n+4:n+5].hex()))
    file.write(':'+str(data[n+5:n+6].hex()))
    n += MAC

    # ID Protocol - 1 bytes
    protocol = int.from_bytes(data[n:n+ID_PROTOCOL], byteorder='little')
    file.write(','+str(protocol))
    n += ID_PROTOCOL

    # leng msg - 2 bytes
    file.write(','+str(int.from_bytes(data[n:n+LENG_MSG], byteorder='little')))
    n += LENG_MSG

    ###### DATA ######

    # Val: 1 - 1 bytes
    file.write(','+str(int.from_bytes(data[n:n+DATA_1], byteorder='little')))
    n += DATA_1

    # Batt_level - 1 bytes
    file.write(','+str(int.from_bytes(data[n:n+DATA_2], byteorder='little')))
    n += DATA_2

    # Timestamp - 4 bytes
    time = datetime.fromtimestamp(int.from_bytes(data[n:n+DATA_3], byteorder='little'))
    file.write(','+time.strftime('%d/%m/%Y %H:%M:%S'))
    n += DATA_3

    if protocol != 0:
        # Temp - 1 bytes
        file.write(','+str(int.from_bytes(data[n:n+DATA_4], byteorder='little')))
        n += DATA_4

        # Press - 4 bytes
        file.write(','+str(int.from_bytes(data[n:n+DATA_5], byteorder='little')))
        n += DATA_5

        # Hum - 1 bytes
        file.write(','+str(int.from_bytes(data[n:n+DATA_6], byteorder='little')))
        n += DATA_6

        # Co - 4 bytes
        file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
        n += DATA_N

        if protocol != 1:
            # RMS - 4 bytes
            file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
            n += DATA_N

            if protocol != 2:
                # Amp x - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
                n += DATA_N

                # Frec x - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
                n += DATA_N

                # Amp y - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
                n += DATA_N

                # Frec y - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
                n += DATA_N

                # Amp z - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))
                n += DATA_N

                # Frec z - 4 bytes
                file.write(','+str(int.from_bytes(data[n:n+DATA_N], byteorder='little')))

    file.write('\n')

def server(port=PORT, file=FILENAME, host=HOST):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)  # 1 accepted connections
    conn, addr = s.accept()  # waits for a new connection
    f = open_file(file)

    print('Client connected: ', addr)
    while True:
        data = conn.recv(11+44)  # HEADER: 11 - DATA: 44
        if not data:
            break
        conn.sendall(b'0')
        write_line(f, data)
    conn.close()
    f.close()

if __name__ == '__main__':
    arg = sys.argv
    if len(arg) == 4:
        server(arg[1], arg[2], arg[3])
    elif len(arg) == 3:
        server(arg[1], arg[2])
    elif len(arg) == 2:
        server(arg[1])
    else:
        server()