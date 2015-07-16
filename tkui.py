import tkinter as tk
import threading as thr
from constants import *
from time import strftime

def simple_grid(*args):
    """All widgets .grid()"""
    widgets = list(args)
    for widget in widgets:
        widget.grid()

class tkWindow:
    """
    The Base tkinter window for the Server and Client
    Classes with common tkinter-related methods.
    """
    def __init__(self, master):
        self.master = master
        self.master.title('Messenger')
        self.message_box = None
        self.running = True
        self.server = None
        self.class_ = None
        self.port = DEFAULT_PORT
        self.widgets = []

    def destroy_widgets(self):
        """Destroy all widgets"""
        for widget in self.widgets:
            widget.destroy()

    def append(self, *args):
        """Append all widgets to self.widgets"""
        widgets = list(args)
        for widget in widgets:
            self.widgets.append(widget)

    def starting_window(self):
        """Window, choose to host or join server"""
        hs = tk.Button(self.master, text='Host Server',
                       command=lambda: self.get_class(HOST_SERVER))
        js = tk.Button(self.master, text='Join Server',
                       command=lambda: self.get_class(JOIN_SERVER))
        hs.grid(row=0, column=0)
        js.grid(row=0, column=1)
        self.append(hs, js)

    def get_class(self, class_):
        """Call on starting window button"""
        pass

    def make_message_box(self):
        """Main message box which displays current conversation/terminal"""
        self.message_box = tk.Text(self.master, width=60, height=12)
        vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        vbar.grid(row=0, column=3, sticky=tk.N + tk.S)
        vbar.config(command=self.message_box.yview)
        self.message_box.config(yscrollcommand=vbar.set)
        self.append(self.message_box, vbar)

    def display_time(self):
        """Call when server opens or client joins"""
        if self.class_ == HOST_SERVER:
            t = strftime('%Y:%m:%d  %T:%S')
            m = 'Server Opened: ' + t
        elif self.class_ == CLIENT:
            t = strftime('%A %I:%M %p')
            m = 'Joined Chat on ' + t
        self.display_message(m, side=RIGHT)

    def display_message(self, message, side=LEFT):
        """Add text to main text box"""
        if side == LEFT:
            message = '\n' + str(message)
        elif side == RIGHT:
            message = '\n' + (58 - len(message)) * ' ' + str(message)
        self.message_box.insert(tk.END, message)
        self.message_box.see(tk.END)

    def make_port_entry(self, listening=False):
        """Return tk.Entry and tk.Label to receive desired port"""
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
            text = 'Server Port Number'
        label = tk.Label(self.master, text=text)
        self.append(entry, label)
        return entry, label

    def send_message(self, entry=None, args=None):
        """Call to send message from client"""
        pass

    def broadcast(self, entry=None, args=None):
        """Call to broadcast message from server"""
        pass

    def make_message_entry(self, broadcast=False):
        """Return tk.Entry and tk.Button for writing message"""
        entry = tk.Entry(self.master, width=40)
        if broadcast:
            command = lambda junk=None: self.broadcast(entry)
        else:
            command = lambda junk=None: self.send_message(entry)
        button = tk.Button(self.master, text='Send Message', command=command)
        self.master.bind('<Return>', command)
        self.append(entry, button)
        return entry, button

if __name__ == '__main__':
    pass
