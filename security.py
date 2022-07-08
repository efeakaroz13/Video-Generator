import subprocess
import platform
from cryptography.fernet import Fernet


class AUTHMACADDR:
    def __init__(self):
        uname = platform.uname()
        self.system = uname.system
        self.nodename = uname.node
        self.release = uname.release
        self.version = uname.version
        self.machine = uname.machine
        self.processor = uname.processor
        try:
            self.macaddress = subprocess.check_output("./macaddress.exe", shell=True)
        except:
            self.macaddress = ""

        self.userinfo = {
            "system": self.system,
            "node": self.nodename,
            "release": self.release,
            "verison": self.version,
            "machine": self.machine,
            "processor": self.processor,
            "macaddress": self.macaddress,
        }

    def login(self):

        if self.macaddress == b"f8:ff:c2:00:f0:b8\n":

            print(self.userinfo)
        else:
            pass
            """
            key = Fernet.generate_key()
            fernet = Fernet(key)
            with open("main.py", "rb") as file:
                original = file.read()

            encrypted = fernet.encrypt(original)

            with open("main.py", "wb") as encrypted_file:
                encrypted_file.write(encrypted)

            with open("security.py", "rb") as file2:
                original2 = file2.read()

            encrypted2 = fernet.encrypt(original2)

            with open("security.py", "wb") as encrypted_file2:
                encrypted_file2.write(encrypted2)

            """
