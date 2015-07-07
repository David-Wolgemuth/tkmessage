import socket
import select
from message import Message
from tkui import *
from constants import *

class Server(tkWindow):
    def __init__(self, master):
        tkWindow.__init__(self, master)
        self.connections = {}
        self.listen_max = 5

    def get_information(self):
        p_entry, p_label = self.make_port_entry()
        l_entry, l_label = self.make_port_entry(listening=True)
        submit = tk.Button(self.master, text='Submit',
                           command=lambda: Server.setup(self, p_entry.get(), l_entry.get()))
        p_label.grid(row=0, column=0)
        p_entry.grid(row=0, column=1)
        l_label.grid(row=1, column=0)
        l_entry.grid(row=1, column=1)
        submit.grid(row=2, columnspan=2)
        self.append(p_entry, p_label, l_entry, l_label, submit)

    def failed_to_establish(self):
        e = tk.Button(self.master, text='Failed to Establish Server',
                      command=lambda: e.destroy())
        self.append(e)
        e.grid()

    def setup(self, port, listening):
        self.port = port
        self.listen_max = listening
        try:
            self.make_socket()
        except Exception as error:
            self.failed_to_establish()
            raise error
        else:
            thread = thr.Thread(target=self.accept_clients)
            thread.start()
            self.destroy_widgets()
            self.terminal()

    def terminal(self):
        self.make_message_box()
        m_entry, m_button = self.make_message_entry(broadcast=True)
        exit_ = tk.Button(self.master, text='Close Server',
                          command=lambda: self.close_server())
        self.message_box.grid(row=0, column=0, columnspan=3)
        exit_.grid(row=1, column=0)
        m_entry.grid(row=1, column=1)
        m_button.grid(row=1, column=2)
        self.append(m_entry, m_button, exit_)

    def make_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', int(self.port)))
        self.server.listen(10)
        self.connections[HOST_SERVER] = self.server

    def accept_clients(self):
        connections = list(self.connections.values())
        print(self.connections.keys())
        readers, writers, error = select.select(connections, [], [])
        for sock in readers:
            if sock == self.server:
                client, address = self.server.accept()
                name = client.recv(BUFFER)
                m = Message(name)
                self.connections[m.sender] = client
                self.display_message(m.sender)
                rm_thread = thr.Thread(target=self.relay_messages,
                                       args=(client,))
                rm_thread.start()
        if self.running:
            self.accept_clients()

    def relay_messages(self, client):
        in_ = client.recv(BUFFER)
        print('in>>', in_)
        m = Message(encoded=in_)
        if m.args and EXIT in m.args:
            self.connections.pop(m.sender)
        self.display_message('%s >> %s' % (m.sender, [HOST_SERVER if m.receiver == None
                                                      else m.receiver][0]))
        print('message', m.message)
        self.display_message(m.message)
        if m.receiver:
            self.connections[m.receiver].send(in_)
        if self.running:
            self.relay_messages(client)

    def broadcast(self, message=None, args=None):
        if message:
            log = 'Message From Server: ' + str(message[:-1])
            log += '\nSend to: '
        elif args == EXIT:
            message = log = 'Server Closing'
        else:
            return
        for client in self.connections:
            m = Message(sender=HOST_SERVER, message=message, args=args)
            if client != HOST_SERVER:
                try:
                    self.connections[client].send(m.encoded)
                except:
                    log += '\n\t**ERROR** Unable to send to %s.' % client
                else:
                    log += client + ', '
        self.display_message(log)

    def close_server(self):
        self.broadcast(args=EXIT)
        self.server.close()
        self.running = False

if __name__ == '__main__':
    pass
