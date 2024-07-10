import argparse
import os
from clearshell import decryptsh

WHITE = '\033[97m'
RED = '\033[91m'
GREEN = '\033[92m'

def main():
    parser = argparse.ArgumentParser(description='Decrypt obfuscated bash scripts.')
    parser.add_argument('--decrypt', type=str, help='The input obfuscated bash script file', required=True)
    parser.add_argument('output_file', type=str, help='The output decrypted bash script file')
    parser.add_argument('--move', type=str, help='Optional path to move the decrypted file to')

    args = parser.parse_args()

    try:
        if args.move:
            result = decryptsh(args.decrypt, args.output_file, args.move)
            print(f"{WHITE}[{GREEN}+{WHITE}] {GREEN}Decrypted and moved successfully to {result}{WHITE}")
        else:
            result = decryptsh(args.decrypt, args.output_file)
            print(f"{WHITE}[{GREEN}+{WHITE}] {GREEN}Decrypted successfully{WHITE} - saved at {result}")
    except Exception as e:
        print(f"{WHITE}[{RED}+{WHITE}] {RED}An error occurred: {e}{WHITE}")

if __name__ == "__main__":
    main()
