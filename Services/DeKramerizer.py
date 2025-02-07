# This code is based on https://github.com/WizardlyCat/kramer-deobfuscator

import re
from binascii import unhexlify
import chardet

from pystyle import Colors, Colorate

from Services.BaseDeobfuscator import BaseDeobfuscator

strings = "abcdefghijklmnopqrstuvwxyz0123456789"

class Kyrie:
    @staticmethod
    def _dkyrie(text: str) -> str:
        r = ""
        for a in text:
            if a in strings:
                i = strings.index(a) + 1
                if i >= len(strings):
                    i = 0
                a = strings[i]
            r += a
        return r

    @staticmethod
    def _decrypt(text: str, key: int) -> str:
        return "".join(chr(ord(t) - key) if t != "ζ" else "\n" for t in text)

class Key:
    @staticmethod
    def decrypt(e: str, key: int) -> str:
        decrypted = Kyrie._decrypt(e, key)
        return Kyrie._dkyrie(decrypted)

def deobfuscate(content: str, key: int) -> str:
    hex_lines = content.split("/")
    decoded_lines = []
    for line in hex_lines:
        try:
            decoded_line = unhexlify(line).decode("utf-8", errors="ignore")
            decoded_lines.append(decoded_line)
        except ValueError:
            continue
    joined_content = "".join(decoded_lines)
    return Key.decrypt(joined_content, key)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    detected = chardet.detect(raw_data)
    # print(f"Detected encoding: {detected['encoding']}")
    return raw_data.decode(detected['encoding'], errors="ignore")


class DeKramerizer(BaseDeobfuscator):

    def __init__(self, source_filepath, destination_filepath):
        super().__init__()
        self.encrypted_file = source_filepath
        self.decrypted_file = destination_filepath
        self.data = self.read_file(self.encrypted_file)
        self.decryption_key = self.__determine_key()

    def __determine_key(self):
        try:
            return int(re.findall(r"-\d{6}", self.data)[0][1:])
        except TypeError:
            print(Colorate.Color(Colors.red, "[FAIL] Unable to determine deobfuscation key."))
            exit(1)
    
    def deobfuscate(self):
        try:
            encrypted_content = detect_encoding(self.encrypted_file)
        except UnicodeDecodeError:
            print(Colorate.Color(Colors.red, "[FAIL] Unable to detect encoding or read the file."))
            exit(1)

        decrypted_content = deobfuscate(encrypted_content, self.decryption_key)
        self.write_file(self.decrypted_file, decrypted_content)
        return ("[SUCCESS] Kramer obfuscation was cracked successfully.", Colors.green)
        
        



