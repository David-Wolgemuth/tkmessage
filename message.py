
def get_element(decoded):
    element = ''
    for i, char in enumerate(decoded):
        if char != ' ':
            element += char
        else:
            decoded = decoded[i + 1:]
            if element == 'None':
                element = None
            return element, decoded

class Message:
    def __init__(self, message=None, args=None, sender=None, receiver=None,
                 encoded=None):
        """
        encoded message follows this format:
            b'arguments SenderName ReceiverName Message'

        possible arguments: 'exited' 'server_closed' 'time_sent'
        the spaces in the encoded message are necessary
        (user-names cannot have spaces)
        """
        if isinstance(message, str):
            self.message = message
            self.encoded = None
            print('string')
        elif isinstance(message, bytes):
            self.encoded = message
            self.message = None
            print('bytes')
        else:
            self.message = None
            self.encoded = encoded

        self.args = args
        self.sender = sender
        self.receiver = receiver
        if self.encoded:
            self.decode_message()
        else:
            self.encode_message()

    def encode_message(self):
        string = '%s %s %s %s' % (self.args, self.sender,
                                  self.receiver, self.message)
        self.encoded = str.encode(string)

    def decode_message(self):
        decoded = self.encoded.decode()
        self.args, decoded = get_element(decoded)
        self.sender, decoded = get_element(decoded)
        self.receiver, decoded = get_element(decoded)
        self.message = decoded


if __name__ == '__main__':
    e = Message(sender='The_Sender',
                receiver='The_Recipient',
                message='The_Message: What else would you like to Know?',
                args='The_Arguments')
    print(e.encoded)
    x = Message(encoded=b'None David None Hola?\n')

    print(x.sender)
    print(x.message)