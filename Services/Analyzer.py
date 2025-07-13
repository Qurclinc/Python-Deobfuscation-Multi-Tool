
class Analyzer:

    def __init__(self):
        self.obfuscation_methods = {
            -1: None,
            0: "Kramer",
            1: "Recursion",
            2: "Zlib+Base",
            3: "Marshal"
        }
        self.data = ""

#TODO: I will improve it one day I promise... 

    def analyze(self, filepath):
        with open(filepath, "r") as f:
            self.data = ''.join([i.strip() for i in f.readlines()])
        if "class Kramer" in self.data:
            return self.obfuscation_methods.get(0)
        elif "setrecursionlimit" in self.data:
            return self.obfuscation_methods.get(1)
        elif "__import__('zlib').decompress(__import__('base64')" in self.data and "__[::-1]" in self.data:
            return self.obfuscation_methods.get(2)
        elif "__import__('marshal').loads" in self.data:
            return self.obfuscation_methods.get(3)
        else:
            return self.obfuscation_methods.get(-1)