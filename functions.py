import sqlite3
import bcrypt
import os
import time

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('KEY')

salt = bcrypt.gensalt()
con = sqlite3.connect("database.db")
cur = con.cursor()
f = Fernet(KEY.encode('utf-8'))
loginstatus = False
user_name = ''
accountname= ''

class Check:
    @staticmethod
    def StoredUserName(username: str):
        if (con.execute("SELECT username FROM account WHERE username = ?", [username]).fetchone()) is not None:
            dbname = (con.execute("SELECT username FROM account WHERE username = ?", [username])).fetchone()[0]
            if dbname == username:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def StoredAccount(username: str, password: str):
        if Check.StoredUserName(username):
            dbpw = (con.execute("SELECT password FROM account WHERE username = ?", [username])).fetchone()[0]
            return bcrypt.checkpw(password.encode('utf-8'), dbpw)
        else:
            return False

    @staticmethod
    def StoredPassword(passwordsite: str):
        info = Get.StoredPasswords().split(', ')
        if passwordsite in info:
            return True
        else:
            return False

class Get:

    @staticmethod
    def StoredPasswords():
        global user_name
        return con.execute("SELECT storedpasswords FROM account WHERE username = ?", [user_name]).fetchone()[0]

    @staticmethod
    def Passwords():
        info = Get.StoredPasswords().split(', ')
        retrievedinfo = ''
        for i in range(0, len(info)-1, 2):
            retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8') + '\n'
        print(retrievedinfo)

    @staticmethod
    def Password(passwordsite: str):
        global user_name
        retrievedinfo = ''
        info = Get.StoredPasswords().split(', ')
        if Check.StoredPassword( passwordsite):
            for i in range(0, len(info)-1, 2):
                if passwordsite == info[i]:
                    retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8')
            print(retrievedinfo)
        else:
            print('Password for ' + passwordsite + ' doesnt exist.')

class Modify:

    class Account:
        @staticmethod
        def RegisterAccount(name: str, username: str, password: str):
            if Check.StoredUserName(username):
                print('Name already in Use.')
                return 'error'
            else:
                con.execute("INSERT INTO account VALUES(?, ?, ?, ?)", [name, username, bcrypt.hashpw(password.encode('utf-8'), salt), ''])
                con.commit()
                print('Registered successfully.')
                return 'success'

        @staticmethod
        def AccountName(newname: str):
            global user_name
            cur.execute("UPDATE account SET name = ? WHERE username = ?", [newname, user_name])
            con.commit()
            print('Name changed successfully.')
            return 'success'

        @staticmethod
        def AccountPassword(newpassword: str):
            global user_name
            cur.execute("UPDATE account SET password = ? WHERE username = ?", [bcrypt.hashpw(newpassword.encode('utf-8'), salt), user_name])
            con.commit()
            print('Password changed successfully.')
            return 'success'

    class List:

        @staticmethod
        def newPassword(passwordsite: str,password: str):
            global user_name
            if Check.StoredPassword(passwordsite):
                print('Password already stored.')
                return 'error'
            else:
                ecpw = f.encrypt(password.encode('utf-8'))
                info = Get.StoredPasswords()
                if len(info) < 6:
                    info += passwordsite + ', ' + str(ecpw.decode('utf-8'))
                else:
                    info += ', ' + passwordsite + ', ' + str(ecpw.decode('utf-8'))
                con.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", (info, user_name))
                con.commit()
                print('Password for ' + passwordsite + ' added successfully.')
                return 'success'

        @staticmethod
        def removePassword(passwordsite: str):
            global user_name
            if Check.StoredPassword(passwordsite):
                info = Get.StoredPasswords().split(', ')
                retrievedinfo = ''
                for i in range(0, len(info)-1, 2):
                    if passwordsite != info[i]:
                        retrievedinfo += info[i] + ', ' + info[i+1]
                cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [retrievedinfo, user_name])
                con.commit()
                print(passwordsite + ' removed.')
                return 'success'
            else:
                print('Password for ' + passwordsite + ' doesnt exist.')
                return 'error'

        @staticmethod
        def changePassword(passwordsite: str, password: str):
            global user_name
            if Check.StoredPassword(passwordsite):
                info = Get.StoredPasswords().split(', ')
                retrievedinfo = ''
                ecpw = f.encrypt(password.encode('utf-8'))
                for i in range(0, len(info)-1, 2):
                    if passwordsite == info[i]:
                        info[i+1] = str(ecpw.decode('utf-8'))
                    retrievedinfo += info[i] + ', ' + info[i+1]
                cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [retrievedinfo, user_name])
                con.commit()
                print('Password for ' + passwordsite + ' changed successfully.')
                return 'success'
            else:
                print('You dont have ' + passwordsite + ' registered.')
                return 'error'

class Window:

    @staticmethod
    def login():
        if loginstatus == True:
            print("You're already logged in.")
        else:
            os.system('cls')
            status = 0
            username = ''
            password = ''
            while status == 0:
                if len(username) >= 2 and len(password) >= 7:
                    answer = input('Login\nUsername: ' + username + '\nPassword: ' + password + '\n|Username| |Password| |Continue| |Quit| \n>')
                else:
                    answer = input('Login\nUsername: ' + username + '\nPassword: ' + password + '\n|Username| |Password| |Quit| \n>')

                answer = answer.lower()
                match answer:
                    case 'username':
                        username = Other.ask('username')
                        os.system('cls')

                    case 'password':
                        password = Other.ask('password')
                        os.system('cls')

                    case 'continue':
                        if len(username) >= 2 and len(password) >= 7:
                            if Other.login(username, password) == 'success':
                                status = 1
                                time.sleep(2)
                                os.system('cls')
                            else:
                                time.sleep(1)
                                os.system('cls') 
                        else:
                            print('Error, wrong input.')
                            time.sleep(1)
                            os.system('cls') 

                    case 'quit':
                        os.system('cls')
                        status = 1

                    case _:
                        print('Error, wrong input.')
                        time.sleep(1)
                        os.system('cls')

    @staticmethod
    def register():
        if loginstatus == True:
            print("You're already logged in.")
        else:
            os.system('cls')
            status = 0
            name = ''
            username = ''
            password = ''
            while status == 0:
                if len(name) >= 2 and len(username) >= 2 and len(password) >= 7:
                    answer = input('Register\nName: ' + name + '\nUsername: ' + username + ' (Cannot be changed)\nPassword: ' + password + '\n|Name| |Username| |Password| |Continue| |Quit| \n>')
                else:
                    answer = input('Register\nName: ' + name + '\nUsername: ' + username + ' (Cannot be changed)\nPassword: ' + password + '\n|Name| |Username| |Password| |Quit| \n>')

                answer = answer.lower()
                match answer:
                    case 'username':
                        username = Other.ask('username')
                        os.system('cls')

                    case 'name':
                        name = Other.ask('name')
                        os.system('cls')

                    case 'password':
                        password = Other.ask('password')
                        os.system('cls')

                    case 'continue':
                        if len(name) >= 2 and len(username) >= 2 and len(password) >= 7:
                            if Modify.Account.RegisterAccount(name, username, password) == 'error':
                                time.sleep(1)
                                os.system('cls')
                            else:
                                status = 1
                                time.sleep(2)
                                os.system('cls')

                    case 'quit':
                            status = 1
                            os.system('cls')

                    case _:
                        print('Error, wrong input.')
                        time.sleep(1)
                        os.system('cls')

    @staticmethod
    def changeName():
        os.system('cls')
        status = 0
        name = ''
        while status == 0:
            if len(name) > 3:
                answer = input('Change Name\nName: ' + name + '\n|Name| |Continue| |Quit| \n>')
            else:
                answer = input('Change Name\nName: ' + name + '\n|Name| |Quit| \n>')

            answer = answer.lower()
            match answer:
                case 'name':
                    name = Other.ask('name')

                case 'continue':
                    if len(name) > 3:
                        Modify.Account.AccountName(name)
                        status = 1
                        time.sleep(2)
                        os.system('cls')

                case 'quit':
                    os.system('cls')
                    status = 1

                case _:
                    print('Error, wrong input.')
                    time.sleep(1)
                    os.system('cls')
    
    @staticmethod
    def changePassword():
        os.system('cls')
        status = 0
        password = ''
        while status == 0:
            if len(password) > 7:
                answer = input('Change Password\nPassword: ' + password + '\n|Password| |Continue| |Quit| \n>')
            else:
                answer = input('Change Password\nPassword: ' + password + '\n|Password| |Quit| \n>')

            answer = answer.lower()
            match answer:
                case 'password':
                    password = Other.ask('password')
                    os.system('cls')

                case 'continue':
                    if len(password) > 7:
                        Modify.Account.AccountPassword(password)
                        status = 1
                        time.sleep(2)
                        os.system('cls')

                case 'quit':
                    os.system('cls')
                    status = 1

                case _:
                    print('Error, wrong input.')
                    time.sleep(1)
                    os.system('cls')
    
    @staticmethod
    def other():
        global loginstatus
        os.system('cls')
        status = 0
        while status == 0:
            if loginstatus == True:
                answer = input('ChangeName - Changes the current name of the account.\nChangePassword - Changes the current password of the account.\nRandomPass - Generates a random password for any use.\nQuit (Quits the other page)\n>')
            else:
                answer = input('RandomPass - Generates a random password for any use.\nQuit (Quits the other page)\n>')
            answer = answer.lower()

            match answer:
                case 'changename':
                    if loginstatus == True:
                        Window.changeName()
                        status = 1
                        time.sleep(1)
                        os.system('cls')

                case 'changepassword':
                    if loginstatus == True:
                        Window.changePassword()
                        status = 1
                        time.sleep(1)
                        os.system('cls')

                case 'randompass':
                    os.system('cls')
                    status = 1
                    print('Randomly generated password: ' + str(Other.newRandomPass()))

                case 'quit':
                    os.system('cls')
                    status = 1

                case _:
                    print('Error, wrong input.')
                    time.sleep(1)
                    os.system('cls')
    
    @staticmethod
    def passwords():
        global loginstatus, user_name, accountname
        if loginstatus == False:
            print("You have to be logged in to do that.")
        else:
            status = 0
            while status == 0:
                os.system('cls')
                answer = input('\x1B[4m' + 'Hello, '+ accountname + '\x1B[0m' + '\nAccounts - Shows the list of accounts you have registered.\nAddAccount - Register a new account to the system.\nRemoveAccount - Remove an account you have registered in the system.\nChangePassword - Change the password from an account you have registered.\nQuit (Quits the other page)\n>')
                answer = answer.lower()

                match answer:
                    case 'accounts':
                        os.system('cls')
                        Get.Passwords()
                        search = ''
                        while search != 'quit':
                            search = input('Type anything to search, empty to show everything or quit to exit.\n>')
                            os.system('cls')
                            if search == '':
                                Get.Passwords()
                            else:
                                Get.Password(search)

                    case 'addaccount':
                        os.system('cls')
                        answer1 = ''
                        accname = ''
                        password = ''
                        status1 = 0
                        while status1 == 0:
                            if len(accname) >= 3 and len(password) >= 7:
                                answer1 = input('Add Account\nName: ' + accname + '\nPassword: ' + password + '\n|Name| |Password| |Continue| |Quit| \n>')
                            else:
                                answer1 = input('Add Account\nName: ' + accname + '\nPassword: ' + password + '\n|Name| |Password| |Quit| \n>')
                            answer1 = answer1.lower()

                            match answer1:
                                case 'name':
                                    accname = Other.ask('name')
                                    os.system('cls')

                                case 'password':
                                    password = Other.ask('password')
                                    os.system('cls')

                                case 'continue':
                                    if len(accname) >= 3 and len(password) >= 7:
                                        if Modify.List.newPassword(accname, password) == 'success':
                                            status1 = 1
                                            time.sleep(2)
                                        else:
                                            time.sleep(1)
                                    os.system('cls')

                                case 'quit':
                                    os.system('cls')
                                    status1 = 1

                                case _:
                                    print('Error, wrong input.')
                                    time.sleep(1)
                                    os.system('cls')

                    case 'removeaccount':
                        status1 = 0
                        os.system('cls')
                        while status1 == 0:
                            answer1 = input('What account you want to remove?\n>')
                            if answer1 != 'quit':
                                if Modify.List.removePassword(answer1) == 'error':
                                    time.sleep(1)
                                    os.system('cls')
                                else:
                                    time.sleep(2)
                                    os.system('cls')
                                    status1 = 1
                            else:
                                os.system('cls')
                                status1 = 1

                    case 'changepassword':
                        os.system('cls')
                        accname = ''
                        password = ''
                        status1 = 0
                        while status1 == 0:
                            if len(accname) >= 3 and len(password) >= 7:
                                answer1 = input('Change Password\nName: ' + accname + '\nPassword: ' + password + '\n|Name| |Password| |Continue| |Quit| \n>')
                            else:
                                answer1 = input('Change Password\nName: ' + accname + '\nPassword: ' + password + '\n|Name| |Password| |Quit| \n>')
                            answer1 = answer1.lower()

                            match answer1:
                                case 'name':
                                    accname = Other.ask('name')
                                    os.system('cls')

                                case 'password':
                                    password = Other.ask('password')
                                    os.system('cls')

                                case 'continue':
                                    if len(accname) >= 3 and len(password) >= 7:
                                        if Modify.List.changePassword(accname, password) == 'error':
                                            time.sleep(1)
                                            os.system('cls')
                                        else:
                                            status1 = 1
                                            time.sleep(2)
                                            os.system('cls')

                                case 'quit':
                                    os.system('cls')
                                    status1 = 1

                                case _:
                                    print('Error, wrong input.')
                                    time.sleep(1)
                                    os.system('cls')

                    case 'quit':
                        os.system('cls')
                        status = 1

                    case _:
                        print('Error, wrong input.')
                        time.sleep(1)
                        os.system('cls')
             
class Other:
    @staticmethod
    def login(username: str, password: str):
        global user_name, loginstatus, accountname
        if Check.StoredAccount(username, password):
            user_name = username
            accountname = con.execute("SELECT name FROM account WHERE username = ?", [user_name]).fetchone()[0]
            print('Successfully logged in.')
            loginstatus = True
            return 'success'
        else:
            print('Something went wrong, check your name or password.')
            return 'error'

    @staticmethod
    def logOut():
        global user_name, loginstatus, accountname
        if loginstatus == False:
            print("You have to be logged in to do that.")
        else:
            print("You have been logged out.")
            user_name = ''
            accountname = ''
            loginstatus = False

    @staticmethod
    def newRandomPass():
        newpass = Fernet.generate_key().decode('utf-8')
        return newpass

    @staticmethod
    def ask(type: str):
        answer1 = ''
        if type == 'username':
            while len(answer1) < 2:
                os.system('cls')
                answer1 = input('Type the username.\n>')

                if len(answer1) < 2:
                    print('Username must have atleast 2 characters.')
                    time.sleep(2)
                os.system('cls')

        if type == 'password':
            while len(answer1) < 7:
                os.system('cls')
                answer1 = input('Type the password.\n>')
                
                if len(answer1)  < 7:
                    print('Password must have atleast 7 characters.')
                    time.sleep(2)
                    os.system('cls')
        
        if type == 'name':
            while len(answer1) < 2:
                os.system('cls')
                answer1 = input('Type the name.\n>')
                
                if len(answer1)  < 2:
                    print('Name must have atleast 2 characters.')
                    time.sleep(2)
                    os.system('cls')
        return answer1

def Help():
    print('Commands that exist: \n Register - Create a new account.\n Login - Log in an existing account.\n Logout - Log out from the account you loggedd in.\n Other - Other commands that might be useful.\n Passwords - Enter the passwords panel.\n Clear - Clears the console.')
