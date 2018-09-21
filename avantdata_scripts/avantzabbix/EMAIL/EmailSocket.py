#import socket

#TCP_IP = '192.168.100.151'
#TCP_PORT = 25
#BUFFER_SIZE = 2048
#
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((TCP_IP, TCP_PORT))
#while True:
#	data = s.recv(BUFFER_SIZE)
#	#s.close()
#	print("Data: {0}".format(data))

import sys
import socket
import select

TCP_IP = '127.0.0.1'
TCP_PORT = 6443
BUFFER_SIZE = 1024
param = []

print 'Listening for client...'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP,TCP_PORT))
server.listen(1)
rxset = [server]
txset = []

while 1:
    rxfds, txfds, exfds = select.select(rxset, txset, rxset)
    for sock in rxfds:
        if sock is server:
            conn, addr = server.accept()
            conn.setblocking(0)
            rxset.append(conn)
            print 'Connection from address:', addr
        else:
            try:
                data = sock.recv(BUFFER_SIZE)
                if data == ";" :
                    print "Received all the data"
                    for x in param:
                        print x
                    param = []
                    rxset.remove(sock)
                    sock.close()
                else:
                    print "received data: ", data
                    param.append(data)
            except:
                print "Connection closed by remote end"
                param = []
                rxset.remove(sock)
                sock.close()
