import argparse
from clearshell.decrypt import decryptsh

def main():
    parser = argparse.ArgumentParser(description="Decrypt a bash script obfuscated with eval.")
    parser.add_argument('--decrypt', nargs=2, metavar=('input_file', 'output_file'),
                        help="Specify the input and output files for decryption.")
    parser.add_argument('--move', metavar='move_path',
                        help="Specify the path to move the decrypted file.")
    args = parser.parse_args()

    if args.decrypt:
        decryptsh(args.decrypt[0], args.decrypt[1], args.move)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
