import pprint
from . import api, console, paket, path, pkcrypt, search, protect

shell = console.Console()
telegram = search.Telegram()

while True:
    shell.path = '~/paketlib/'
    shell.input()
    t_input = shell.inputstr.strip()
    if t_input == 'help':
        print('''
help menu:
    protect [filename (.py)] - protect python code
    ip [ip] - ip search
    number [number] - phone search (+XX...)
    tguser [@tag] - telegram username search
    tgchannel [@tag] - telegram channel search
    tgchat [@tag] - telegram chat search
    tgparse [@tag] - telegram channel parsing
    userbox [authtoken] [query] - userbox search
    leakosint [token] [query] - leakosint search
    dbsearch [database] [query] - search in database
    getmessage - get message from paketapi servers
    getbootcode - get boot code from paketapi servers
    help - show this menu
''')

    elif t_input.startswith('ip'):
        t_ip = t_input.split(' ')[-1].strip()
        for a, b in search.ipLookup(t_ip).items():
            print(f'[+] {a}: {b}')

    elif t_input.startswith('protect'):
        t_fname = t_input.split(' ')[-1].strip()
        nobf_c = open(t_fname, 'r').read()
        obf_c = protect.protect(nobf_c)
        print(f'#=====================================\n#OBF BY PAKET\n{obf_c}')

    elif t_input.startswith('userbox'):
        pprint.pprint(search.SearchUserBox(t_input.split(' ', 2)[2], t_input.split(' ', 2)[1]))

    elif t_input.startswith('number'):
        num = t_input.split(' ')[-1]
        for a, b in search.PhoneNumber(num).items():
            print(f'[+] {a}: {b}')

    elif t_input.startswith('tguser'):
        tag = t_input.split(' ')[-1]
        for a, b in telegram.TelegramUsername(tag).items():
            print(f'[+] {a}: {b}')

    elif t_input.startswith('tgchannel'):
        tag = t_input.split(' ')[-1]
        for a, b in telegram.TelegramChannel(tag).items():
            print(f'[+] {a}: {b}')

    elif t_input.startswith('tgchat'):
        tag = t_input.split(' ')[-1]
        for a, b in telegram.TelegramChat(tag).items():
            print(f'[+] {a}: {b}')

    elif t_input.startswith('tgparse'):
        tag = t_input.split(' ')[-1]
        for a in telegram.TelegramCParser(tag):
            print(f'[+] {a}')

    elif t_input.startswith('leakosint'):
        search.SearchLeak(t_input.split(' ', 2)[2], t_input.split(' ', 2)[1])

    elif t_input.startswith('dbsearch'):
        search.dbsearch(t_input.split(' ', 2)[1], t_input.split(' ', 2)[2])

    elif t_input == 'getbootcode':
        print(api.getbootcode())

    elif t_input == 'getmessage':
        print(api.getmessage())
    print()

        