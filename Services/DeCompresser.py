import re
import base64
import zlib
from pystyle import Colors

from Services.BaseDeobfuscator import BaseDeobfuscator

class DeCompressor(BaseDeobfuscator):

    def __init__(self, source_file, destination_file, base=None):
        super().__init__()
        self.source_file = source_file
        self.destination_file = destination_file
        self.data = self.read_file(self.source_file)
        if base is None:
            self.base = self._identify_base()
        else:
            self.base = base
        self.redo_pattern = r"^exec\(\(_\)\(b['\"].*['\"]\)\)"
    
    def _identify_base(self):
        try:
            return int(re.search(r"b\d{2}decode", self.data).group()[1:3])
        except Exception as ex:
            print("NO BASE XD")
            exit(0)

    def decompress(self, data, encoded=False):
        reversed_data = data[::-1]
        if self.base == 64:
            decoded_data = base64.b64decode(reversed_data)
        elif self.base == 32:
            decoded_data = base64.b32decode(reversed_data)
        elif self.base == 16:
            decoded_data = base64.b16decode(reversed_data)
        elif self.base == 85:
            decoded_data = base64.b85decode(reversed_data)
        decompressed_data = zlib.decompress(decoded_data)
        if encoded:
            print(decoded_data)
            return decompressed_data
        else:
            return decompressed_data.decode()
    
    def check(self):
        self.data = self.read_file(self.destination_file)
        return re.match(self.redo_pattern, self.data)

    def deobfuscate(self, encoded=False):
        clean_data = self.sanitarize(self.data)
        self.write_file(self.destination_file, self.decompress(clean_data, encoded))
        if self.check():
            self.deobfuscate()
        return (f"[SUCCESS] Zlib+Base{self.base} obfuscation was cracked successfully.", Colors.green)
