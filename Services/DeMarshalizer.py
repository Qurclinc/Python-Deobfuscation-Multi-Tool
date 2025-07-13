import marshal
import importlib.util
import requests
import os
from pystyle import Colorate, Colors

from Services.BaseDeobfuscator import BaseDeobfuscator

class DeMarhsalizer(BaseDeobfuscator):

    def __init__(self, source_file, destination_file):
        super().__init__()
        self.source_file = source_file
        self.destination_file = destination_file
        self.data = self.read_file(self.source_file)
        self.url = "http://46.30.47.219:7878/demarshalize"
        self.tmp_filepath = "./tmp.pyc"
        self.magic = importlib.util.MAGIC_NUMBER + b'\x00\x00\x00\x00\x04\x94\x90d\xd4`\x00\x00'
        # self.magic = b'\xcb\r\r\n\x00\x00\x00\x00\x04\x94\x90d\xd4`\x00\x00'

    def send_file(self):
        try:
            with open(self.tmp_filepath, "rb") as pyc:
                files = {"file": (self.tmp_filepath, pyc, "application/octet-stream")}
                response = requests.post(self.url, files=files)
                return response
        except Exception:
            print(Colorate.Color(Colors.red, "[FAIL] Unable to connect to remote host. Check your internet connection."))
            exit(1)

    def get_response(self, response):
        if response.status_code == 200:
            with open(self.destination_file, "wb") as f:
                f.write(response.content)
        else:
            return ("[FAIL] Marshal obfuscation wasn't cracked.", Colors.red)

        return ("[SUCCESS] Marshal obfuscation was cracked successfully.", Colors.green)
    
    def write_binary_file(self, code_obj):
        with open(self.tmp_filepath, "wb") as pyc:
            pyc.write(self.magic)
            marshal.dump(code_obj, pyc)

    def deobfuscate(self):
        data = eval(f"b'{self.sanitarize(self.data)}'")
        if "[::-1]" in self.data:
            reversed_data = data[::-1]
        else:
            reversed_data = data
        code_obj = marshal.loads(reversed_data)

        self.write_binary_file(code_obj)
        

        response = self.send_file()
        return self.get_response(response)

    def __del__(self):
        try:
            os.remove(self.tmp_filepath)
        except FileNotFoundError:
            pass