import sqlite3
import os

from cryptography.fernet import Fernet

confirm = input("Are you sure you want to run the setup? (This file is going to be deleted)\n Y/N ")

if confirm == 'Y':
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE account(name, username, password, storedpasswords)")
    con.close()
    key = Fernet.generate_key()
    f = open('.env', 'w+')
    f.write('KEY="' + key.decode('utf-8') + '"')
    f.close()
    os.remove("setup.py")
else:
    quit