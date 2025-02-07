import re

class Analyzer:

    def __init__(self):
        self.obfuscation_methods = {
            -1: None,
            0: "Kramer",
            1: "Zlib+Base64",
            2: "Marshal"
        }
        self.data = ""

    def analyze(self, filepath):
        with open(filepath, "r") as f:
            self.data = ''.join([i.strip() for i in f.readlines()])
        if "class Kramer" in self.data:
            return self.obfuscation_methods.get(0)
        elif "__import__('zlib').decompress(__import__('base64').b64decode(__[::-1]" in self.data:
            return self.obfuscation_methods.get(1)
        elif "__import__('marshal').loads" in self.data:
            return self.obfuscation_methods.get(2)
        else:
            return self.obfuscation_methods.get(-1)