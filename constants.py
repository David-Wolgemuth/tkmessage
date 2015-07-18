DEFAULT_PORT = 8989
LOCALHOST = 'localhost'
BUFFER = 1024
LEFT = 'left'
RIGHT = 'right'
EXIT = 'exit'
HOST_SERVER = 'Server'
JOIN_SERVER = 'join_server'
CLIENT = 'Client'
DEFAULT_USERNAME = 'MonsterJam'
LOGIN = 'Login'
BAD_USERNAME = 'Bad_Username_or_Password'
ACCEPTED = 'Username_and_Password_Accepted'
CONTACTS = 'Contacts'
INBOX = 'Inbox'
NO_USER = 'Username Does Not Exist'
EXISTING_CONTACT = 'Contact Already in Contact List'
NEW_CONVO = 'New_Conversation'
MESSAGES = 'messages'
PASSWORD = 'password'

def print_constants():
    print('\n%s:\n' % __doc__)
    constants = globals().copy()
    for constant in constants:
        if constant[0].isalpha() and constant != 'print_constants':
            print('%s = %s' % (constant, constants[constant]))

if __name__ == '__main__':
    print_constants()
