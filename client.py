#!/usr/bin/env python3
import socket
import sys
import i3ipc

SOCKET_FILE = '/tmp/i3_nvim'

RESIZE_I3 = {'j' : 'resize grow height 5 px or 5 ppt',
             'k' : 'resize shrink height 5 px or 5 ppt',
             'h' : 'resize shrink width 5 px or 5 ppt',
             'l' : 'resize grow width 5 px or 5 ppt'}

msg = sys.argv[1::]
try:
    data = ' '.join(msg).encode()
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(SOCKET_FILE)
    client_socket.send(data)
    client_socket.close()
except:
    i3 = i3ipc.Connection()
    if msg[0] == 'focus':
        i3.command('focus '+msg[1])
    elif msg[0] == 'resize':
        i3.command(RESIZE_I3[msg[1]])
