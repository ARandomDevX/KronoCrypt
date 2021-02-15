import os
import getpass

from cryptography.fernet import Fernet

from hashlib import scrypt
from os import urandom
from base64 import urlsafe_b64encode

import glob

banner =  r""" ____  __.                           _________                        __   
|    |/ _|______  ____   ____   ____ \_   ___ \_______ ___.__._______/  |_ 
|      < \_  __ \/  _ \ /    \ /  _ \/    \  \/\_  __ <   |  |\____ \   __\
|    |  \ |  | \(  <_> )   |  (  <_> )     \____|  | \/\___  ||  |_> >  |  
|____|__ \|__|   \____/|___|  /\____/ \______  /|__|   / ____||   __/|__|  
        \/                  \/               \/        \/     |__|         
        
        (C) BigBoy32 On Github"""
print(banner)

key = scrypt(bytes(getpass.getpass('Password: ').encode("utf-8")), salt=b"SALT", n=16384, r=8, p=1, dklen=32)
enc = Fernet(urlsafe_b64encode(key))

fn = """import os
import getpass

from cryptography.fernet import Fernet

from hashlib import scrypt
from os import urandom
from base64 import urlsafe_b64encode

files = {}

key = scrypt(bytes(getpass.getpass('Password: ').encode("utf-8")), salt=b"SALT", n=16384, r=8, p=1, dklen=32)
enc = Fernet(urlsafe_b64encode(key))

for item in files:
    if 'b' in item['metadata'][1]:
        with open(item['metedata'][0], 'wb') as f:
            f.writelines(enc.decrypt(item['data']))
            f.close()
    else:
        with open(item['metadata'][0], 'w') as f:
            f.writelines(enc.decrypt(item['data']).decode("utf-8"))
            f.close()

"""

files = []
f = []

for item in glob.glob("encrypt/*.*"):
    files.append(item)

for item in files:
    d = input('How do you want to read the file ' + item + "? [b]ytes/[n]ormal: ")

    if d == "n":
        f.append({"metadata":[item.split("\\ ".strip())[1], "d"], 'data':enc.encrypt(bytes(str(open(item, 'r').read()).encode("utf-8")))})
    else:
        f.append({"metadata":[item, "d"], 'data':enc.encrypt(bytes(str(open(item, 'rb').read()).encode("utf-8")))})

open("out.py", "w").write(fn.format(str(f)))
os.system("kronocompile.bat")

print("Delete build, move dist/out.exe and delete dist")