import re
import base64
import zlib
from pystyle import Colors

from Services.BaseDeobfuscator import BaseDeobfuscator

class DeCompressor(BaseDeobfuscator):

    def __init__(self, source_file, destination_file):
        super().__init__()
        self.source_file = source_file
        self.destination_file = destination_file
        self.data = self.read_file(self.source_file)
        self.redo_pattern = r"^exec\(\(_\)\(b['\"].*['\"]\)\)"
    
    def decompress(self, data):
        reversed_data = data[::-1]
        b64decoded_data = base64.b64decode(reversed_data)
        decompressed_data = zlib.decompress(b64decoded_data)
        return decompressed_data.decode("utf-8")
    
    def check(self):
        self.data = self.read_file(self.destination_file)
        return re.match(self.redo_pattern, self.data)

    def deobfuscate(self):
        clean_data = self.sanitarize(self.data)
        self.write_file(self.destination_file, self.decompress(clean_data))
        if self.check():
            self.deobfuscate()
        return ("[SUCCESS] Zlib+Base64 obfuscation was cracked successfully.", Colors.green)
