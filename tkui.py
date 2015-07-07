import tkinter as tk
import threading as thr
from constants import *
from time import strftime

def simple_grid(*args):
    widgets = list(args)
    for widget in widgets:
        widget.grid()

class tkWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Messenger')
        self.message_box = None
        self.running = True
        self.server = None
        self.class_ = None
        self.current_side = None
        self.port = DEFAULT_PORT
        self.widgets = []

    def destroy_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def append(self, *args):
        widgets = list(args)
        for widget in widgets:
            self.widgets.append(widget)

    def starting_window(self):
        hs = tk.Button(self.master, text='Host Server',
                       command=lambda: self.get_class(HOST_SERVER))
        js = tk.Button(self.master, text='Join Server',
                       command=lambda: self.get_class(JOIN_SERVER))
        hs.grid(row=0, column=0)
        js.grid(row=0, column=1)
        self.append(hs, js)

    def get_class(self, class_):
        pass

    def make_message_box(self):
        self.message_box = tk.Text(self.master, width=60, height=12)
        vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        vbar.grid(row=0, column=3, sticky=tk.N + tk.S)
        vbar.config(command=self.message_box.yview)
        self.message_box.config(yscrollcommand=vbar.set)
        self.append(self.message_box, vbar)

    def display_time(self):
        if self.class_ == HOST_SERVER:
            t = strftime('%Y:%m:%d  %T:%S')
            m = 'Server Opened: ' + t
        elif self.class_ == CLIENT:
            t = strftime('%A %I:%M %p')
            m = 'Joined Chat on ' + t
        self.display_message(m, side=RIGHT)

    def display_message(self, message, side=LEFT):
        if side == LEFT:
            message = '\n' + str(message)
        elif side == RIGHT:
            message = '\n' + (58 - len(message)) * ' ' + str(message)
        self.message_box.insert(tk.END, message)
        self.message_box.see(tk.END)

    def make_port_entry(self, listening=False):
        valid_port = self.master.register(lambda x, y, z: ((x.isdigit() and
                                                            len(y) < 5) or
                                                           z == '0'))
        entry = tk.Entry(self.master, validate='key', width=6,
                         validatecommand=(valid_port, '%S', '%s', '%d'))
        if listening:
            entry.insert(0, 5)
            text = 'Max Connections'
        else:
            entry.insert(0, self.port)
            text= 'Server Port Number'
        label = tk.Label(self.master, text=text)
        self.append(entry, label)
        return entry, label

    def send_message(self, entry, args=None):
        self.broadcast(message, args=None)

    def broadcast(self, entry=None, args=None):
        pass

    def make_message_entry(self, broadcast=False):
        entry = tk.Text(self.master, width=40, height=2)
        if broadcast:
            command = lambda: self.broadcast(entry)
        else:
            command = lambda: self.send_message(entry)
        button = tk.Button(self.master, text='Send Message', command=command)
        self.append(entry, button)
        return entry, button

if __name__ == '__main__':
    pass
