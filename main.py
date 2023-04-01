from functions import *
response = ''

input('Welcome to PasswordManager done by RafaBacano, press enter to start.')
os.system('cls')
while response != 'quit':
    if loginstatus == False:
        response = input('Type Help for help\n>')
    else:
        response = input('Hello, ' + accountname + ', type help for help.\n>')

    response = response.lower()
    if response == 'help':
        Help()
    if response == 'register':
        Window.register()
    if response == 'login':
        Window.login()
    if response == 'logout':
        Other.logOut()
    if response == 'other':
        Window.other()
    if response == 'passwords':
        Window.passwords()
    if response == 'clear':
        os.system('cls')

con.close()
os.system('cls')
input('Goodbye')