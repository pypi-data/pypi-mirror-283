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
        input_file, output_file = args.decrypt
        move_path = args.move
        result = decryptsh(input_file, output_file, move_path)
        if isinstance(result, str):
            print(result)
        elif result:
            if move_path:
                print(f"Decrypted and moved to: {move_path}")
            else:
                print("Decrypted successfully")
        else:
            print("Decryption failed")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
