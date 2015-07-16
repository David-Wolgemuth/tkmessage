import socket
import select
from message import Message
from tkui import *
from constants import *
import shelve
import time
import pdb

class Server(tkWindow):
    def __init__(self, master):
        tkWindow.__init__(self, master)
        self.connections = {}
        self.listen_max = 5

    def get_information(self):
        """Grid tk.Entry, tk.Label for port and max listening"""
        self.class_ = HOST_SERVER
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
        self.master.geometry('+%s+%s' % (10, 500))
        self.make_message_box()
        m_entry, m_button = self.make_message_entry(broadcast=True)
        exit_ = tk.Button(self.master, text='Close Server',
                          command=lambda: self.close_server())
        self.message_box.grid(row=0, column=0, columnspan=3)
        exit_.grid(row=1, column=0)
        m_entry.grid(row=1, column=1)
        m_button.grid(row=1, column=2)
        self.display_time()
        self.append(m_entry, m_button, exit_)

    def make_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', int(self.port)))
        self.server.listen(10)
        self.connections[HOST_SERVER] = self.server

    def accept_clients(self):
        connections = list(self.connections.values())
        readers, writers, error = select.select(connections, [], [])
        for sock in readers:
            if sock == self.server:
                client, address = self.server.accept()
                rm_thread = thr.Thread(target=self.relay_messages,
                                       args=(client,))
                rm_thread.start()
                time.sleep(1)
        if self.running:
            self.accept_clients()

    def user_login(self, message, client):
        usernames = shelve.open('server_info/usernames')
        name = message.sender
        log = ''
        args = ''
        if message.args[-1] == '1':  # New Username
            if name not in usernames:
                usernames[name] = message.message
                log = 'Username and Password Created for %s' % name
                with shelve.open('server_info/users/' + name) as user:
                    user[CONTACTS] = []
                    user[INBOX] = {}
                args = ACCEPTED
                self.connections[name] = client
            else:
                log = 'Username Already Exists'
                args = BAD_USERNAME

        elif message.args[-1] == '0':  # Existing Username
            if name not in usernames:
                log = 'Username Does Not Exist'
                args = BAD_USERNAME
            else:
                if usernames[name] == message.message:  # Checking Passwords
                    log = '%s Logged In' % name
                    args = ACCEPTED
                    self.connections[name] = client
                else:
                    log = 'Incorrect Username / Password'
                    args = BAD_USERNAME

        m = Message(sender=HOST_SERVER,
                    receiver=name,
                    message=log,
                    args=args)
        client.send(m.encoded)

        usernames.close()
        return log

    def user_logs(self, username, info_requested):
        with shelve.open('server_info/users/' + username) as user:
            info = Message(sender=HOST_SERVER,
                               args=info_requested,
                               message=str(user[info_requested]))
            self.connections[username].send(info.encoded)

    def relay_messages(self, client):
        in_ = client.recv(BUFFER)
        if not in_:
            for key, value in self.connections.items():
                if value == client:
                    self.connections.pop(key)
                    return
        m = Message(encoded=in_)
        ct = strftime('%T:%S ')
        log = ct
        r = m.receiver if m.receiver else 'Server'
        if m.args:
            if m.args.startswith(LOGIN):
                log += self.user_login(m, client)  # Returns String
            elif m.args == CONTACTS or m.args == INBOX:
                self.user_logs(m.sender, m.args)
                log += '%s sent %s' % (m.sender, m.args)
            elif m.args.startswith(CONTACTS):
                new = m.args[len(CONTACTS):]
                with shelve.open('server_info/usernames') as usernames:
                    if new not in usernames:
                        a = Message(args=CONTACTS,
                                    message=NO_USER)
                        client.send(a.encoded)
                    else:
                        with shelve.open('server_info/users/' + m.sender,
                                         writeback=True) as user:
                            user[CONTACTS].append(new)
                            a = Message(args=CONTACTS, message=new)
                            client.send(a.encoded)
        else:
            log += '%s >> %s\n%s' % (m.sender, r, m.message)
        self.display_message(log)
        if m.receiver:
            self.connections[m.receiver].send(in_)
        if self.running:
            self.relay_messages(client)

    def broadcast(self, entry=None, args=None):
        log = '%s Server ' % strftime('%T:%S')
        if entry:
            message = entry.get()
            entry.delete(0, tk.END)
            log += '>> '
        elif args == EXIT:
            log += 'Closing >> '
            message = ''
        else:
            raise ValueError('function must include tk.Entry or string arguments')
        for client in self.connections:
            m = Message(sender=HOST_SERVER, message=message, args=args)
            if client != HOST_SERVER:
                try:
                    self.connections[client].send(m.encoded)
                except:
                    log += '\n\t**ERROR** Unable to send to %s.' % client
                else:
                    log += '%s | ' % client
        log += '\n%s' % m.message
        self.display_message(log)

    def close_server(self):
        self.broadcast(args=EXIT)
        self.server.close()
        self.display_message('Server Closed')
        self.running = False

if __name__ == '__main__':
    pass
