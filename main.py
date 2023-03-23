from functions import *

def loginWindow():
    pass

response = ''
input('Welcome to PasswordManager done by RafaBacano, press enter to start.')
os.system('cls')
while response != 'quit':
    response = input('Type Help for help\n>')
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
        
print('Goodbye')
input()