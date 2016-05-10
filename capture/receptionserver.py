import os
import csv
import socket
import msgpack
import uuid
import time
import requests
import json

UDP_IP = "::"
UDP_PORT = 7777

sock = socket.socket(socket.AF_INET6,
    socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

RECORDS = []
columns = ["time","IP","seq"]
print ','.join(columns)
with open('log.csv','wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)
while True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        seq = msgpack.unpackb(data)
        RECORDS.append([int(time.time()), addr[0], seq])
        print ','.join(map(str, RECORDS[-1]))
        with open('log.csv','ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(RECORDS[-1])
    except KeyboardInterrupt:
        with open('log_total.csv','wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(RECORDS)
        raise
    except Exception as e:
        print e
        pass
