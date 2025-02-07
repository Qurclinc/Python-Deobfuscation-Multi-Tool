import argparse
import os
from pystyle import Colors, Colorate

from Services.Analyzer import Analyzer
from Services.DeKramerizer import DeKramerizer
from Services.DeCompresser import DeCompressor
from Services.DeMarshalizer import DeMarhsalizer

def crack(result, source_file, destination_file):
    if result == "Kramer":
        deobfuscator = DeKramerizer(source_file, destination_file)
    elif result == "Zlib+Base64":
        deobfuscator = DeCompressor(source_file, destination_file)
    elif result == "Marshal":
        deobfuscator = DeMarhsalizer(source_file, destination_file)
    else:
        return ("[INFO] It's not obfuscated", Colors.cyan)
    return deobfuscator.deobfuscate()

def main():
    parser = argparse.ArgumentParser(description="Python deobfuscation multi-tool is ready to serve you. It's able to deobfuscate both signle files and whole projects.")
    parser.add_argument("--source_file", "-i", type=str, help="Path to obfuscated file (depends on your OS.)")
    parser.add_argument("--destination_file", "-o", type=str, help="Path to deobfuscated file (depends on your OS.)")
    parser.add_argument("--root", "-r", type=str, help="Path to root folder with obfuscated code (depends on your OS.)")
    args = parser.parse_args()

    analyzer = Analyzer()

    if args.source_file and args.destination_file and not(args.root):

        source_file = os.path.abspath(args.source_file)
        destination_file = os.path.abspath(args.destination_file)

        result = ""

        while result != None:
            try:
                result = analyzer.analyze(source_file)
                iteration = crack(result, source_file, destination_file)
                print(Colorate.Color(iteration[1], iteration[0]))
                source_file = destination_file
            except FileNotFoundError:
                print(Colorate.Color(Colors.red, "File not found"))
        
    elif args.root and not(args.source_file) and not(args.destination_file):
        root_folder = os.path.abspath(args.root)
        for root, dirs, files in os.walk(root_folder):
                for file in files:
                    source_file = destination_file = os.path.abspath(os.path.join(root, file))
                    if str(source_file).split(".")[-1] == "py":
                        result = ""
                        while result != None:
                            try:
                                result = analyzer.analyze(source_file)
                                iteration = crack(result, source_file, destination_file)
                                print(Colorate.Color(iteration[1], f"{iteration[0]} for file {source_file}"))
                                source_file = destination_file
                            except FileNotFoundError:
                                print(Colorate.Color(Colors.red, "File not found"))
                    
    else:
        print(Colorate.Color(Colors.red, "[FAIL] You cannot use all parameters at once."))
        exit(0)

    

if __name__ == "__main__":
    main()