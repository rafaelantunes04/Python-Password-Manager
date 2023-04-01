import os
import subprocess
confirm = input("RafaBacano Password Manager Setup\n\nBy typing Y and Enter you will install all modules\n(sqlite3, bcrypt, cryptography and dotenv),create a\ndatabase and deleting this setup, do you wish to do that?")

if confirm == 'Y' or confirm == 'y':
    subprocess.check_call(['pip', 'install', 'sqlite3', 'bcrypt', 'cryptography', 'python-dotenv'])
    from cryptography.fernet import Fernet
    import sqlite3
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE account(name, username, password, storedpasswords)")
    con.close()
    key = Fernet.generate_key()
    f = open('.env', 'w+')
    f.write('KEY="' + key.decode('utf-8') + '"')
    f.close()
    os.remove("setup.py")