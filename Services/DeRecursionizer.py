import os
import re
import ast
import sys
import zlib
import argparse

from base64 import b85decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def deobfuscate(pyc, pye, httpspyobfuscatecom):
    def d(b, p):
        c = b85decode(b.encode('utf-8'))
        r = AES.new(PBKDF2(p, c[:16], dkLen=32, count=1000000), AES.MODE_GCM, nonce=c[16:32])
        return r.decrypt_and_verify(c[48:], c[32:48]).decode('utf-8')
    return(d(pyc + pye, httpspyobfuscatecom.replace('"', '')))

parser = argparse.ArgumentParser()
parser.add_argument("--source_file", "-i", type=str)
parser.add_argument("--destination_file", "-o", type=str)

args = parser.parse_args()

source_file = os.path.abspath(args.source_file)
destination_file = os.path.abspath(args.destination_file)
file = source_file

with open(file, "r", encoding="utf-8") as f:
    content_file = f.read()
    f.seek(0)
    lines = f.readlines()

if "pyobfuscate(" in content_file:
    for i, line in enumerate(lines):
        if line.strip().startswith("pyobfuscate("):
            pyobfuscate_value = lines[i]
            
            pyc_value = re.search(r"'pyc'\s*:\s*\"\"\"(.*?)\"\"\"", pyobfuscate_value, re.DOTALL).group(1)
            pye_value = re.search(r"'pye'\s*:\s*\"\"\"(.*?)\"\"\"", pyobfuscate_value, re.DOTALL).group(1)
            httpspyobfuscatecom = re.search(r"['\"]([lI]+)['\"]", pyobfuscate_value, re.DOTALL).group(0)
            content = deobfuscate(pyc_value, pye_value, httpspyobfuscatecom)
            break
else:
    hex_string = re.findall(r"fromhex\('([0-9a-fA-F]+)'(?!\))", content_file)[0]
    layer_2 = zlib.decompress(bytes.fromhex(hex_string)).decode()

    obfuscated_code = ";".join(value for value in layer_2.split(";")[:-1])

    sys.setrecursionlimit(100000000)

    variable_code = re.findall(r'(\w+)\s*=\s*None', obfuscated_code)[0]
        
    exec(obfuscated_code, globals(), locals())

    base85_code = ast.unparse(eval(variable_code))

    base85_string = re.findall(r"\.b85decode\('([^']+)'\.encode\(\)\)", base85_code)[0]

    content = b85decode(base85_string.encode()).decode()


with open(destination_file, "w", encoding="utf-8") as f:
    f.write(content)
















# Legacy
# import requests
# from pystyle import Colors

# from Services.BaseDeobfuscator import BaseDeobfuscator

# class DeRecursionizer(BaseDeobfuscator):

#     def __init__(self, source_file, destination_file):
#         super().__init__()
#         self.source_file = source_file
#         self.destination_file = destination_file
#         self.data = self.read_file(self.source_file)
#         self.url = "http://127.0.0.1:7878/derecursion"
#         self.tmp_filepath = self.source_file

#     def send_file(self):
#         try:
#             with open(self.tmp_filepath, "rb") as file:
#                 files = {"file": (self.tmp_filepath, file, "text/plain")}
#                 response = requests.post(self.url, files=files)
#                 return response
#         except Exception:
#             print("[FAIL] Unable to connect to remote host. Check your internet connection.")
#             exit(1)



#     def deobfuscate(self):
#         response = self.send_file()
#         print(response.status_code)
#         return ("[SUCCESS] Recursion obfuscation was cracked successfully.", Colors.green)
    
#     def __del__(self):
#         pass