import re

class BaseDeobfuscator:

    def __init__(self):
        self.pattern = r"(?<=\()b['\"].*['\"]"
        

    def sanitarize(self, strings):
        return re.search(self.pattern, strings).group()[2:-1]

    def read_file(self, filepath):
        with open(filepath, "r") as f:
            return "".join([i.strip() for i in f.readlines()])
        
    def write_file(self, filepath, data):
        with open(filepath, "w") as f:
            f.write(data)

    def deobfuscate(self):
        pass
