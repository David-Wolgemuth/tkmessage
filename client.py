import socket
from tkui import *
from message import Message

class Client(tkWindow):
    """
    Create on choose_class function
    """
    def __init__(self, master):
        tkWindow.__init__(self, master)
        self.server_IP = LOCALHOST
        self.receiver = None
        self.user_name = None
        self.last_log = Message()
        self.sessions = {}
        self.inbox = None
        self.contacts = None

    def connect_to_server(self):
        """Client connects to Server"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.server_IP, int(self.port)))

    def server_information(self):
        """Make tk.Entry and tk.Label for port, ip, and username"""
        self.class_ = CLIENT
        p_entry, p_label = self.make_port_entry()
        ip_entry = tk.Entry(self.master)
        ip_entry.insert(0, self.server_IP)
        ip_label = tk.Label(self.master, text='Server IP')
        submit = tk.Button(self.master, text='Submit',
                           command=lambda: Client.setup_connection(self, p_entry.get(),
                                                                   ip_entry.get()))
        self.append(p_entry, p_label, ip_entry, ip_label, submit)
        simple_grid(p_label, p_entry, ip_label, ip_entry, submit)

    def failed_to_connect(self):
        """Grid button which informs user of failed connection"""
        e = tk.Button(self.master, text='Failed to Connect',
                      command=lambda: e.destroy())
        self.append(e)
        e.grid()

    def setup_connection(self, port, ip):
        """Call after getting information, attempt to connect to server"""
        self.port = port
        self.server_IP = ip
        try:
            self.connect_to_server()
        except Exception as error:
            self.failed_to_connect()
            raise error
        else:
            self.destroy_widgets()
            thread = thr.Thread(target=self.receive_messages)
            thread.start()
            self.user_information()

    def user_information(self):
        valid = self.master.register(lambda x: not x.isspace() and x != ',')
        n_entry = tk.Entry(self.master, validate='key',
                           validatecommand=(valid, '%S'))
        n_entry.insert(0, DEFAULT_USERNAME)
        n_label = tk.Label(self.master, text='User Name')
        pw_entry = tk.Entry(self.master, show='*')
        pw_entry.insert(0, '12345678')
        pw_label = tk.Label(self.master, text='Password')
        new = tk.IntVar()
        new_user = tk.Checkbutton(self.master, text='Create New Account',
                                  variable=new)
        submit = tk.Button(self.master, text='Submit',
                           command=lambda: self.setup_user(n_entry.get(),
                                                           pw_entry.get(),
                                                           new.get()))
        self.append(n_entry, n_label, pw_label, pw_entry, new_user, submit)
        simple_grid(n_label, n_entry, pw_label, pw_entry, new_user, submit)

    def setup_user(self, user, password, new):
        m = Message(sender=user,
                    message=password,
                    args=LOGIN + str(new))
        self.server.send(m.encoded)

    def messenger(self):
        """Grid terminal style display and entry
        for reading/writing messages
        """
        self.make_message_box()
        m_entry, m_button = self.make_message_entry()
        inbox = tk.Button(self.master, text='Inbox',
                          command=self.display_inbox)
        self.message_box.grid(row=0, column=0, columnspan=3)
        inbox.grid(row=1, column=0, sticky=tk.W)
        m_entry.grid(row=1, column=1, sticky=tk.W+tk.E)
        m_button.grid(row=1, column=2, sticky=tk.E)
        self.display_time()
        self.append(m_entry, m_button, inbox)

    def display_inbox(self):
        self.destroy_widgets()
        self.receiver = None
        i = lambda x: x.curselection()[0]
        select = lambda x: x.get(i(x))
        self.inbox = tk.Listbox(self.master, width=50, height=8)
        to_contacts = tk.Button(self.master, text='Contacts',
                                command=self.contact_list)
        i_button = tk.Button(self.master, text='Select',
                             command=lambda: self.get_conversation(
                                 select(self.inbox)))
        self.inbox.grid()
        to_contacts.grid()
        i_button.grid()
        self.append(to_contacts, self.inbox, i_button)
        self.send_message(args=INBOX)

    def fill_inbox(self, message):
        inbox = eval(message.message)
        for chat in inbox:
            chat = ' '.join(chat.split(','))
            self.inbox.insert(tk.END, chat)

    def get_conversation(self, receiver):
        receiver = ','.join(receiver.split())
        request = Message(args=NEW_CONVO,
                          sender=self.user_name,
                          receiver=receiver)
        self.receiver = receiver
        self.server.send(request.encoded)

    def start_new_conversation(self, contacts):

        contacts = list(contacts)
        print(contacts)
        contacts.append(self.user_name)
        contacts = sorted(contacts)
        receiver = contacts[0]
        for contact in contacts[1:]:
            receiver += ',' + contact
        message = Message(args=NEW_CONVO,
                          sender=self.user_name,
                          receiver=receiver)
        self.server.send(message.encoded)

    def display_conversation(self, message):
        self.destroy_widgets()
        self.messenger()
        history = eval(message.message)
        last = None
        for m in history:
            side = RIGHT if m[1] == self.user_name else LEFT
            if not last or last[1] != m[1]:
                log = '[%s] %s' % (strftime('%I:%M%p', time.gmtime(m[0])).lower(), m[1])
                self.display_message(log, side=side)
            self.display_message(m[2], side=side)
            last = m

    def contact_list(self):

        self.destroy_widgets()
        i = lambda x: x.curselection()[0]
        select = lambda x: x.get(i(x))
        insertion = lambda x, y: x.insert(tk.END, select(y))
        valid = self.master.register(lambda x: not x.isspace() and x != ',')

        self.contacts = tk.Listbox(self.master, width=30, height=8)
        new_convo = tk.Listbox(self.master, width=30, height=4)
        new_contact = tk.Entry(self.master, validate='key',
                               validatecommand=(valid, '%S'))
        add = tk.Button(self.master, text='>   Add   >',
                        command=lambda: insertion(new_convo, self.contacts))
        sub = tk.Button(self.master, text='<  Remove <',
                        command=lambda: new_convo.delete(i(new_convo)))
        start = tk.Button(self.master, text='Start Conversation',
                          command=lambda: self.start_new_conversation(
                              new_convo.get(0, tk.END)))
        add_new = tk.Button(self.master, text='Add New Contact',
                            command=lambda: self.add_contact(new_contact.get()))

        self.contacts.grid(row=0, column=0, rowspan=4)
        new_convo.grid(row=0, column=1, rowspan=2)
        add.grid(row=2, column=1)
        sub.grid(row=3, column=1)
        start.grid(row=4, column=1)
        add_new.grid(row=4, column=0)
        new_contact.grid(row=5, column=0)

        self.append(self.contacts, new_convo, new_contact, add, sub, start,
                    add_new)
        self.send_message(args=CONTACTS)

    def add_contact(self, contact):
        self.send_message(args=CONTACTS + contact)

    def add_to_contacts(self, list_):
        if list_ == NO_USER or list_ == EXISTING_CONTACT:
            b = tk.Button(self.master, text=list_,
                          command=lambda: b.destroy())
            b.grid()
            self.append(b)
        else:
            try:
                contacts = eval(list_)
            except NameError:
                self.contacts.insert(tk.END, list_)
            else:
                for contact in contacts:
                    self.contacts.insert(tk.END, contact)

    def change_receiver(self, receiver):
        """Call on change_receivers function, sets to new recipient"""
        self.sessions[self.receiver] = self.message_box.get(1.0, tk.END)
        self.message_box.delete(1.0, tk.END)
        self.receiver = receiver
        if self.receiver in self.sessions:
            self.message_box.insert(tk.END, self.sessions[self.receiver])

    def receive_messages(self):
        """Receive and decode message from server, check for arguments"""
        in_ = self.server.recv(BUFFER)
        m = Message(encoded=in_)
        if m.args:
            if m.args == EXIT:
                self.display_message('Server has been closed.')
                self.leave_server()
            elif m.args == BAD_USERNAME:
                b = tk.Button(self.master, command=lambda: b.destroy(),
                              text=m.message)
                self.append(b)
                b.grid()
            elif m.args == ACCEPTED:
                self.user_name = m.receiver
                self.destroy_widgets()
                self.messenger()
            elif m.args == CONTACTS:
                self.add_to_contacts(m.message)
            elif m.args.startswith(CONTACTS):
                b = tk.Button(self.master, command=lambda: b.destroy(),
                              text=m.message)
                b.grid()
                self.append(b)
            elif m.args == MESSAGES:
                self.receiver = m.receiver
                self.display_conversation(m)
            elif m.args == INBOX:
                self.fill_inbox(m)
        elif m.receiver == self.receiver:
            if self.last_log.sender != m.sender:
                log = '%s [%s]' % (m.sender, strftime(
                    '%I:%M%p', time.gmtime(m.time)).lower())
                self.display_message(log, side=LEFT)
            self.display_message(' > %s' % m.message, side=LEFT)
            self.last_log = m

        if self.running:
            self.receive_messages()

    def send_message(self, entry=None, args=None):
        """Encode message and send to server,
        display message on messenger terminal
        """
        if entry:
            message = entry.get()
            entry.delete(0, tk.END)
        else:
            message = ''
        m = Message(message=message,
                    sender=self.user_name,
                    receiver=self.receiver,
                    args=args)

        if m.message:
            if self.last_log.sender != m.sender:
                log = '[%s] %s' % (strftime(
                    '%I:%M%p', time.gmtime(m.time)).lower(), self.user_name)
                self.display_message(log, side=RIGHT)
            self.display_message('%s < ' % m.message, side=RIGHT)
            self.last_log = m
        self.server.send(m.encoded)

    def leave_server(self):
        """Not currently being used"""
        if self.server:
            self.send_message(args=EXIT)
            self.server.close()
        self.running = False


if __name__ == '__main__':
    pass
