import shelve

CHATS = 'server_info/chats/'
USERS = 'server_info/users/'

with shelve.open(USERS + 'MonsterJam') as user:
    for key in user.keys():
        print('%s: %s' % (key, user[key]))

with shelve.open(CHATS + 'Monster,MonsterJam') as chat:
    print(chat['messages'])
    for key in chat.key():
        print('%s: %s' % (key, chat[key]))
