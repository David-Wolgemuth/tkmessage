import time

class Message:
    def __init__(self, message='', args='', sender='', receiver='',
                 encoded=None):
        """
        encoded message follows this format:
            b'arguments SenderName ReceiverName Message'

        possible arguments: 'exited' 'server_closed' 'time_sent'
        the spaces in the encoded message are necessary
        (user-names cannot have spaces)
        """
        self.message = message
        self.args = args
        self.sender = sender
        self.receiver = receiver
        self.encoded = encoded
        self.time = None
        self.decoded = None
        if self.encoded:
            self.decode_message()
        else:
            self.encode_message()

    def encode_message(self):
        self.time = int(time.time())
        string = '%s %s %s %s %s' % (self.time, self.args, self.sender,
                                  self.receiver, self.message)
        self.encoded = str.encode(string)

    def get_element(self):
        element = ''
        for i, char in enumerate(self.decoded):
            if char != ' ':
                element += char
            else:
                self.decoded = self.decoded[i + 1:]
                return element

    def decode_message(self):
        self.decoded = self.encoded.decode()
        t = self.get_element()
        self.time = int(t)
        self.args = self.get_element()
        self.sender = self.get_element()
        self.receiver = self.get_element()
        self.message = self.decoded

    def print(self):
        p = ('\nMessage from %s to %s\nTime: %s'
             '\nArgs: %s\nMessage: %s' %
             (self.sender, self.receiver, self.time,
              self.args, self.message))
        print(p)

if __name__ == '__main__':
    e = Message(sender='The_Sender',
                args='The_Arguments')
    print(e.encoded)
    x = Message(encoded=e.encoded)
    x.print()