from constants import *
from server import Server, tk
from client import Client
import os

class ChooseClass(Server, Client):
    def __init__(self, master):
        Server.__init__(self, master)
        Client.__init__(self, master)
        self.starting_window()

    def get_class(self, class_):
        self.destroy_widgets()
        self.class_ = class_
        print('Class: ', class_)
        if class_ == HOST_SERVER:
            Server.get_information(self)
        elif class_ == JOIN_SERVER:
            Client.server_information(self)

root = tk.Tk()
app = ChooseClass(root)
app.starting_window()
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
root.mainloop()
