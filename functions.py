import sqlite3
import bcrypt
import os
import time

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('KEY')

con = sqlite3.connect("tutorial.db")
cur = con.cursor()
f = Fernet(KEY.encode('utf-8'))
res = cur.execute("SELECT * FROM account")
loginstatus = False
user_name = ''

class Check:
    def StoredUserName(
        self,
        username: str = ...
        ):
        dbname = cur.execute("SELECT username FROM account WHERE username = ?", [username])
        if dbname != None:
            return True
        else:
            return False

    def StoredAccount(
        self,
        username: str = ...,
        password: str = ...
        ):
        if self.checkName(username):
            password = password.encode('utf-8')
            dbpw = cur.execute("SELECT password FROM account WHERE username = ?", [username])
            if bcrypt.checkpw(dbpw, password):
                return True
            else:
                return False
        else:
            return False

    def StoredPassword(
        self,
        passwordsite: str = ...
        ):
        info = Get.StoredPasswords()

        if passwordsite in info:
            return True
        else:
            return False

class Get:

    def StoredPasswords(self):
        global user_name
        info = ''
        for i in cur.execute("SELECT storedpasswords FROM account WHERE username = ?", [user_name]).fetchall()[0]:
                info += i
        return info.split(', ')

    def Passwords(self):
        info = self.StoredPasswords()
        retrievedinfo = ''
        for i in range(0, len(info)-1, 2):
            retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8') + '\n'
        print(retrievedinfo)

    def Password(
        self,
        passwordsite: str = ...
        ):
        global user_name
        retrievedinfo = ''
        info = self.StoredPasswords()
        if Check.StoredPassword(user_name, passwordsite):
            for i in range(0, len(info)-1, 2):
                if passwordsite == info[i]:
                    retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8')
            print(retrievedinfo)
        else:
            print('Password for ' + passwordsite + ' doesnt exist.')

class Modify:

    class Account:
        def RegisterAccount(
            self,
            name: str = ...,
            username: str = ..., 
            password: str = ...
            ):
            if Check.StoredUserName(username):
                print('Name already in Use.')
                return 'error'
            else:
                cur.execute("INSERT INTO account VALUES(?, ?, ?, ?)", [name, username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), ''])
                con.commit()
                print('Registered successfully.')
                return 'success'

        def AccountName(
            self,
            newname: str = ...
            ):
            global user_name
            cur.execute("UPDATE account SET name = ? WHERE username = ?", [newname, user_name])
            con.commit()
            print('Name changed successfully.')
            return 'success'

        def AccountPassword(
            self,
            newpassword: str = ...
            ):
            global user_name
            cur.execute("UPDATE account SET password = ? WHERE username = ?", [newpassword, user_name])
            con.commit()
            print('Password changed successfully.')
            return 'success'

    class List:
        def newPassword(
            self,
            passwordsite: str = ...,
            password: str = ...
            ):
            global user_name
            if Check.StoredPassword(passwordsite):
                print('Password already stored.')
                return 'error'
            else:
                ecpw = f.encrypt(password.encode('utf-8'))
                info = Get.StoredPasswords()
                info += passwordsite + ', ' + str(ecpw.decode('utf-8')) + ', '
                cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [info, user_name])
                con.commit()
                print('Password for ' + passwordsite + ' added successfully.')
                return 'success'

        def removePassword(
            self,
            passwordsite: str = ...
            ):
            global user_name
            if Check.StoredPassword(passwordsite):
                info = Get.StoredPasswords()
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

        def changePassword(
            self,
            passwordsite: str = ...,
            password: str = ...
            ):
            global user_name
            if Check.StoredPassword(passwordsite):
                info = Get.StoredPasswords()
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
                print('You dont have' + passwordsite + ' registered.')
                return 'error'

class Window:
    def login(self):
        if loginstatus == True:
            print("You're already logged in.")
        else:
            os.system('cls')
            status = 0
            username = ''
            password = ''
            while status == 0:
                if len(username) > 2 and len(password) > 7:
                    answer = input('Login\nUsername: ' + username + '\nPassword: ' + password + '\n|Username| |Password| |Continue| |Quit| \n>')
                else:
                    answer = input('Login\nUsername: ' + username + '\nPassword: ' + password + '\n|Username| |Password| |Quit| \n>')

                answer = answer.lower()
                match answer:
                    case 'username':
                        username = Other.ask('username')

                    case 'password':
                        password = Other.ask('password')

                    case 'continue':
                        if len(username) > 2 and len(password) > 7:
                            Other.login(username, password)
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

    def register(self):
        if loginstatus == True:
            print("You're already logged in.")
        else:
            os.system('cls')
            status = 0
            name = ''
            username = ''
            password = ''
            while status == 0:
                if len(name) > 2 and len(username) > 2 and len(password) > 7:
                    answer = input('Register\nName: ' + name + '\nUsername: ' + username + ' (Cannot be changed)\nPassword: ' + password + '\n|Name| |Username| |Password| |Continue| |Quit| \n>')
                else:
                    answer = input('Register\nName: ' + name + '\nUsername: ' + username + ' (Cannot be changed)\nPassword: ' + password + '\n|Name| |Username| |Password| |Quit| \n>')

                answer = answer.lower()
                match answer:
                    case 'username':
                        username = Other.ask('username')

                    case 'name':
                        name = Other.ask('name')

                    case 'password':
                        password = Other.ask('password')

                    case 'continue':
                        if len(name) > 2 and len(username) > 2 and len(password) > 7:
                            if Modify.Account.RegisterAccount(name, username, password) == 'error':
                                time.sleep(2)
                                os.system('cls')
                            else:
                                status = 1
                                time.sleep(2)
                                os.system('cls')

                    case 'quit':
                            status = 1

                    case _:
                        print('Error, wrong input.')
                        time.sleep(1)
                        os.system('cls')

    def changeName(self):
        os.system('cls')
        status = 0
        name = ''
        while status == 0:
            if len(name) > 3:
                answer = input('Login\nName: ' + name + '\n|Name| |Continue| |Quit| \n>')
            else:
                answer = input('Login\nName: ' + name + '\n|Name| |Quit| \n>')

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

    def changePassword(self):
        os.system('cls')
        status = 0
        password = ''
        while status == 0:
            if len(password) > 7:
                answer = input('Login\nPassword: ' + password + '\n|Password| |Continue| |Quit| \n>')
            else:
                answer = input('Login\nPassword: ' + password + '\n|Password| |Quit| \n>')

            answer = answer.lower()
            match answer:
                case 'password':
                    password = Other.ask('password')

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

    def other(self):
        global loginstatus
        os.system('cls')
        status = 0
        while status == 0:
            if loginstatus == True:
                answer = input('ChangeName - Changes the current name of the account.\n ChangePassword - Changes the current password of the account.\n RandomPass - Generates a random password for any use.\n Quit (Quits the other page)\n>')
            else:
                answer = input('RandomPass - Generates a random password for any use.\n Quit (Quits the other page)\n>')
            answer = answer.lower()

            match answer:
                case 'changename':
                    if loginstatus == True:
                        self.changeName()
                        status = 1
                        time.sleep(1)
                        os.system('cls')

                case 'changepassword':
                    if loginstatus == True:
                        self.changePassword()
                        status = 1
                        time.sleep(1)
                        os.system('cls')

                case 'randompass':
                    os.system('cls')
                    status = 1
                    print('Randomly generated password: ' + Other.newRandomPass())

                case 'quit':
                    os.system('cls')
                    status = 1

                case _:
                    print('Error, wrong input.')
                    time.sleep(1)
                    os.system('cls')

    def passwords(self):
        global loginstatus, user_name
        if loginstatus == False:
            print("You have to be logged in to do that.")
        else:
            status = 0
            while status == 0:
                os.system('cls')
                answer = input('Accounts - Shows the list of accounts you have registered.\n AddAccount - Register a new account to the system.\n RemoveAccount - Remove an account you have registered in the system.\n ChangePassword - Change the password from an account you have registered.\n Quit (Quits the other page)\n>')
                answer = answer.lower()

                match answer:
                    case 'accounts':
                        os.system('cls')
                        Get.Passwords()
                        search = ''
                        while search != 'quit':
                            search = input('Type anything to search or quit to exit.\n>')
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
                            if accname > 3 and password > 7:
                                answer1 = input('Add Account\nAccount Name: ' + accname + 'Password: ' + password + '\n |AccountName| |Password| |Continue| |Quit| \n>')
                            else:
                                answer1 = input('Add Account\nAccount Name: ' + accname + 'Password: ' + password + '\n |AccountName| |Password| |Quit| \n>')
                            answer1 = answer1.lower()

                            match answer1:
                                case 'accountname':
                                    accname = Other.ask('name')

                                case 'password':
                                    password = Other.ask('password')

                                case 'continue':
                                    if accname > 3 and password > 7:
                                        Modify.List.newPassword(accname, password)
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

                    case 'removeaccount':
                        status1 = 0
                        os.system('cls')
                        while status1 == 0:
                            answer1 = input('What account you want to remove?\n>')
                            if Modify.List.removePassword(answer1) == 'error':
                                time.sleep(1)
                                os.system('cls')
                            else:
                                time.sleep(2)
                                os.system('cls')
                                status1 = 1
                        status = 1

                    case 'changepassword':
                        os.system('cls')
                        accname = ''
                        password = ''
                        status1 = 0
                        while status1 == 0:
                            if accname > 3 and password > 7:
                                answer1 = input('Add Account\nAccount Name: ' + accname + 'Password: ' + password + '\n |AccountName| |Password| |Continue| |Quit| \n>')
                            else:
                                answer1 = input('Add Account\nAccount Name: ' + accname + 'Password: ' + password + '\n |AccountName| |Password| |Quit| \n>')
                            answer1 = answer1.lower()

                            match answer1:
                                case 'accountname':
                                    accname = Other.ask('name')

                                case 'password':
                                    password = Other.ask('password')

                                case 'continue':
                                    if accname > 3 and password > 7:
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
    def login(
        self,
        username: str = ...,
        password: str = ...
        ):
        global user_name, loginstatus
        if Check.StoredAccount(username, password):
            user_name = username
            print('Successfully logged in.')
            loginstatus == True
            return 'success'
        else:
            print('Something went wrong, check your name or password.')
            return 'error'

    def logOut(self):
        global user_name, loginstatus
        if loginstatus == False:
            print("You have to be logged in to do that.")
        else:
            user_name = ''
            loginstatus == False

    def newRandomPass():
        if loginstatus == False:
            return print('You must be logged in to do that command.')
        else:
            newpass = Fernet.generate_key().decode('utf-8')
            return newpass

    def ask(
        self,
        type: str = ...
        ):
        answer = ''
        if type == 'username':
            while len(answer) < 2:
                os.system('cls')
                answer = input('Type the username.\n>')
                os.system('cls')

                if answer < 2:
                    print('Username must have more than 2 characters.')
                    time.sleep(2)
                    os.system('cls')

        if type == 'password':
            while len(answer) < 7:
                os.system('cls')
                answer = input('Type the password.\n>')
                os.system('cls')
                
                if answer < 7:
                    print('Password must have more than 7 characters.')
                    time.sleep(2)
                    os.system('cls')
        
        if type == 'name':
            while len(answer) < 2:
                os.system('cls')
                answer = input('Type the name.\n>')
                os.system('cls')
                
                if answer < 2:
                    print('Name must have more than 2 characters.')
                    time.sleep(2)
                    os.system('cls')
        return answer
   
def Help():
    print('Commands that exist: \n Register - Create a new account.\n Login - Log in an existing account.\n Logout - Log out from the account you loggedd in.\n Other - Other commands that might be useful.\n Passwords - Enter the passwords panel')

con.close()