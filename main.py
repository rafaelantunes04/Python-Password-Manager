import sqlite3
import bcrypt
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('KEY')

con = sqlite3.connect("tutorial.db")
cur = con.cursor()
f = Fernet(KEY.encode('utf-8'))
res = cur.execute("SELECT * FROM account")
loginstatus = False


def checkName(
    username: str = ...
    ):
    dbname = cur.execute("SELECT username FROM account WHERE username = ?", [username])
    if dbname != None:
        return True
    else:
        return False

def checkAccount(
    username: str = ...,
    password: str = ...
    ):
    if checkName(username):
        password = password.encode('utf-8')
        dbpw = cur.execute("SELECT password FROM account WHERE username = ?", [username])
        if bcrypt.checkpw(dbpw, password):
            return True
        else:
            return False
    else:
        return False

def getPasswords(
    username: str = ...,
    ):
    if checkName(username):
        info = ''
        for i in cur.execute("SELECT storedpasswords FROM account WHERE username = ?", [username]).fetchall()[0]:
                info += i
        return info.split(', ')
    else:
        return print('Name doesnt exist.')

def checkExistingPasswordName(
    username: str = ...,
    passwordsite: str = ...
    ):
    info = getPasswords(username)
    
    if passwordsite in info:
        return True
    else:
        return False

def createAccount(
    name: str = ...,
    username: str = ..., 
    password: str = ...
    ):
    if checkName(username):
        cur.execute("INSERT INTO account VALUES(?, ?, ?, ?)", [name, username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), ''])
        con.commit()
        return print('Registered successfully.')
    else:
        return print('Name already in Use.')

def logIn(
    username: str = ...,
    password: str = ...
    ):
    if checkAccount(username, password):
        print('Successfully logged in.')
        return loginstatus == True
    else:
        print('Something went wrong, check your name or password.')
        return loginstatus == False

def changeName(
    username: str = ...,
    newname: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        cur.execute("UPDATE account SET name = ? WHERE username = ?", [newname, username])
        con.commit()
        return print('Name changed successfully.')

def changeUserPassword(
    username: str = ...,
    newpassword: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        cur.execute("UPDATE account SET password = ? WHERE username = ?", [newpassword, username])
        con.commit()
        return print('Password changed successfully.')

def addPassword(
    username: str = ...,
    passwordsite: str = ...,
    password: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        if checkExistingPasswordName(username, passwordsite):
            ecpw = f.encrypt(password.encode('utf-8'))
            info = getPasswords(username)
            if passwordsite in info:
                return print('Password for ' + passwordsite + ' is  stored successfully.')
            else:
                info += passwordsite + ', ' + str(ecpw.decode('utf-8')) + ', '
                cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [info, username])
                con.commit()
                return print('Password for ' + passwordsite + ' added successfully.')


def getPasswordFrom(
    username: str = ...,
    passwordsite: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        info = getPasswords(username)
        retrievedinfo = ''

        if passwordsite == '':
            for i in range(0, len(info)-1, 2):
                retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8') + '\n'
            return print(retrievedinfo)
        else:
            if checkExistingPasswordName(username, passwordsite):
                for i in range(0, len(info)-1, 2):
                    if passwordsite == info[i]:
                        retrievedinfo += info[i] + ': ' + f.decrypt(info[i+1]).decode('utf-8')
                return print(retrievedinfo)
            else:
                return print('Password for ' + passwordsite + ' doesnt exist.')

def remPassword(
    username: str = ...,
    passwordsite: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        if checkExistingPasswordName(username, passwordsite):
            info = getPasswords(username)
            retrievedinfo = ''

            for i in range(0, len(info)-1, 2):
                if passwordsite != info[i]:
                    retrievedinfo += info[i] + ', ' + info[i+1]
            cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [retrievedinfo, username])
            con.commit()
            return print(passwordsite + ' removed.')
        else:
            return print('Password for ' + passwordsite + ' doesnt exist.')

def changePassword(
    username: str = ...,
    passwordsite: str = ...,
    password: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        if checkExistingPasswordName(username, passwordsite):
            info = getPasswords(username)
            retrievedinfo = ''
            ecpw = f.encrypt(password.encode('utf-8'))
            for i in range(0, len(info)-1, 2):
                if passwordsite == info[i]:
                    info[i+1] = str(ecpw.decode('utf-8'))
                retrievedinfo += info[i] + ', ' + info[i+1]
            cur.execute("UPDATE account SET storedpasswords = ? WHERE username = ?", [retrievedinfo, username])
            con.commit()
            return print('Password for ' + passwordsite + ' changed successfully.')
        else:
            return print('You dont have' + passwordsite + ' registered.')

def newRandomPass(
    username: str = ...,
    passwordsite: str = ...
    ):
    if loginstatus == False:
        return print('You must be logged in to do that command.')
    else:
        newpass = Fernet.generate_key().decode('utf-8')
        if checkExistingPasswordName(username, passwordsite):
            changePassword(username, passwordsite, newpass)
            return print('Your new password for ' + passwordsite + ' is ' + newpass + '.')
        else:
            addPassword(username, passwordsite, newpass)
            return print('Your new password for ' + passwordsite + ' is ' + newpass + '.')

con.close()