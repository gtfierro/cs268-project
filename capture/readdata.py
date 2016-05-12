import os
import csv
import socket
import msgpack
import uuid
import time
import requests
import json
import sys

node = sys.argv[1]
print node
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
sock.connect((node, 5555, 0, 0))

collect = sys.argv[2]
if collect == "collect":
    sock.send("save_report(10)\n")
    #print sock.recv(1024)
    sock.close()
    sys.exit(0)

else:
    sock.send("replay()\n")

RECORDS = []
columns = ["time","IP","seqno","pkt","tx","MIsent","MIrecv","RSsent","RSRECV","hop_cnt","dis","dio","dao","rank"]
print ','.join(columns)
with open('{0}_log.csv'.format(node),'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)
    csvfile.flush()

unpacker = msgpack.Unpacker()
while True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if 137 not in map(ord, data):
            print data
            continue
        sock.send("OK")
        unpacker.feed(data)
        #print type(data), len(data), data
        for stats in unpacker:
            if stats is None: break
            print stats
            #if stats.get('seq',None) == 0xffff:
            #    sys.exit(0)
            lastseq = stats.get('seq')
            RECORDS.append([int(time.time()), node, stats.get('seq',0), stats.get('pkt',0), 
                                              stats.get('tx',0), stats.get('mi_sent',0), 
                                              stats.get('mi_recv',0), stats.get('rs_sent',0),
                                              stats.get('rs_recv',0),stats.get('hop_cnt',0),
                                              stats.get('dis_tx',0), stats.get('dio_tx',0), 
                                              stats.get('dao_tx',0), stats.get('rank', 0)])
            print ','.join(map(str, RECORDS[-1]))
            with open('{0}_log.csv'.format(node),'ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(RECORDS[-1])
                csvfile.flush()
    except KeyboardInterrupt:
        with open('{0}_log_full.csv'.format(node),'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(RECORDS)
            csvfile.flush()
        raise
    except Exception as e:
        print e
        pass
