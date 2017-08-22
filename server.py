#!/usr/bin/env python3
import os
import os.path
import socket
import selectors
import threading
import neovim
import i3ipc

SOCKET_FILE = '/tmp/i3_nvim'

WINCMD = {'up'   :'k',
          'down' :'j',
          'left' :'h',
          'right':'l'}

RESIZE_VIM = {'j' : '+',
              'k' : '-',
              'h' : '<',
              'l' : '>'}

RESIZE_I3 = {'j' : 'resize grow height 5 px or 5 ppt',
             'k' : 'resize shrink height 5 px or 5 ppt',
             'h' : 'resize shrink width 5 px or 5 ppt',
             'l' : 'resize grow width 5 px or 5 ppt'}

class NvimWatcher:
    def __init__(self):
        self.i3 = i3ipc.Connection()
        self.listening_socket = socket.socket(socket.AF_UNIX,
            socket.SOCK_STREAM)
        if os.path.exists(SOCKET_FILE):
            os.remove(SOCKET_FILE)
        self.listening_socket.bind(SOCKET_FILE)
        self.listening_socket.listen(1)
        self.nvim_list = dict()
        # self.nvim_list_lock = threading.RLock()

    def launch_server(self):
        selector = selectors.DefaultSelector()

        def accept(sock):
            conn, addr = sock.accept()
            selector.register(conn, selectors.EVENT_READ, read)

        def read(conn):
            data = conn.recv(1024)
            if data:
                msg = data.decode().split()
                if msg[0] == 'register':
                    self.nvim_list.update({int(msg[1]):(neovim.attach('socket', path=msg[2]), msg[2])})
                elif msg[0] == 'unregister':
                    if int(msg[1]) in self.nvim_list:
                        self.nvim_list.pop(int(msg[1]))
                else:
                    try:
                        tree = self.i3.get_tree()
                    except BrokenPipeError:
                        self.i3 = i3ipc.Connection()
                        tree = self.i3.get_tree()
                    wid = next((x.window for x in tree.leaves()
                            if x.focused and x.window in self.nvim_list), None)
                    if wid:
                        nvim, nv_path = self.nvim_list[wid]
                        if not os.path.exists(nv_path):
                            self.nvim_list.pop(wid)
                            nvim = None
                    else:
                        nvim = None
                if msg[0] == 'focus':
                    if nvim:
                        wn = nvim.eval('winnr()')
                        nvim.command('wincmd '+WINCMD[msg[1]])
                        if wn == nvim.eval('winnr()'):
                            self.i3.command('focus '+msg[1])
                    else:
                        self.i3.command('focus '+msg[1])
                elif msg[0] == 'resize':
                    if nvim:
                        if ((msg[1]=='j' or msg[1]=='k') and (
                                nvim.eval('CountHSplits()') > 1) or
                            (msg[1]=='h' or msg[1]=='l') and (
                                nvim.eval('CountVSplits()') > 1)):
                            nvim.command('4wincmd '+RESIZE_VIM[msg[1]])
                        else:
                            self.i3.command(RESIZE_I3[msg[1]])
                    else:
                        self.i3.command(RESIZE_I3[msg[1]])
            elif not data:
                selector.unregister(conn)
                conn.close()

        selector.register(self.listening_socket, selectors.EVENT_READ, accept)

        while True:
            for key, event in selector.select():
                callback = key.data
                callback(key.fileobj)

    def run(self):
        threading.Thread(target=self.launch_server).start()

if __name__ == '__main__':
    nvim_watcher = NvimWatcher()
    nvim_watcher.run()
