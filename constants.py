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

def print_constants():
    print('\n%s:\n' % __doc__)
    constants = globals().copy()
    for constant in constants:
        if constant[0].isalpha() and constant != 'print_constants':
            print('%s = %s' % (constant, constants[constant]))

if __name__ == '__main__':
    print_constants()
