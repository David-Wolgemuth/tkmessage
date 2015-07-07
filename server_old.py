import socket
import select
import threading

PORT = 8989
BUFFER = 1024

class Server:
    def __init__(self):
        self.server = None
        self.running = True
        self.make_socket()
        self.connections = [self.server]
        self.accept_clients()

    def make_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', PORT))
        sock.listen(2)
        self.server = sock

    def accept_clients(self):
        readers, writers, error = select.select(self.connections, [], [])
        for sock in readers:
            if sock == self.server:
                client, address = self.server.accept()
                rm_thread = threading.Thread(target=self.receive_messages,
                                             args=(client, ))
                rm_thread.start()
                print(len(self.connections))
                self.connections.append(client)
        self.accept_clients()

    def send_messages(self, client):
        message = input()
        self.quit(message, client)
        client.send(str.encode(message))
        if self.running:
            self.send_messages(client)

    def broadcast(self, message):
        for client in self.connections:
            print('Broadcasting to: ', client)
            if client != self.server:
                client.send(message)

    def receive_messages(self, client):
        print('Receiving from: ', client)
        message = client.recv(BUFFER)
        if message:
            self.quit(message, client)
            print(message.decode())
            self.broadcast(message)
        if self.running:
            self.receive_messages(client)

    def quit(self, message, client_):
        if message == 'q':
            for client in self.connections[1:]:
                client.send(b'quit')
                self.server.close()
                self.running = False
        elif message == b'q':
            print('%s has left.' % client_)
            self.connections.remove(client_)


class Client:
    def __init__(self):
        self.running = True
        self.server = None
        self.setup()

    def setup(self):
        self.connect_to_server()
        thread = threading.Thread(target=self.receive_messages)
        thread.start()
        self.send_messages()

    def connect_to_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('localhost', PORT))

    def send_messages(self):
        message = input(' o> ')
        self.quit(message)
        self.server.send(str.encode(message))
        if self.running:
            self.send_messages()

    def receive_messages(self):
        message = self.server.recv(BUFFER)
        if message:
            self.quit(message)
            print(message.decode())
        if self.running:
            self.receive_messages()

    def quit(self, message):
        if message == b'q':
            print('Server socket has closed.')
            self.running = False
        elif message == 'q':
            self.server.send(b'q')
            self.server.close()
            self.running = False

if __name__ == '__main__':
    import sys
    arg = sys.argv
    if len(arg) == 1:  # No extra argument on Terminal creates server
        sock = Server()
    else:  # Any extra argument on Terminal creates client, ex: 'python3 server_old.py client'
        sock = Client()
    print('Press ENTER to quit')