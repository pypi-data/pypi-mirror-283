import os

# Colors
white = "\033[97m"
green = "\033[92m"
red = "\033[91m"

def decryptsh(input_file, output_file, move_path=None, print_messages=True):
    def print_msg(message):
        if print_messages:
            print(message)
        else:
            return message
    
    if not os.path.exists(input_file):
        return print_msg(f"{white}[{red}+{white}] {red}File not found")
    
    with open(input_file, 'r') as in_f, open(".temp1", 'w') as temp_f:
        filedata = in_f.read()
        if "eval" not in filedata:
            return print_msg(f"{white}[{red}+{white}] {red}Cannot be decrypted!")
        newdata = filedata.replace("eval", "echo")
        temp_f.write(newdata)

    os.system("bash .temp1 > .temp2")
    os.remove(".temp1")

    with open(".temp2", 'r') as temp_f2, open(output_file, 'w') as out_f:
        filedata = temp_f2.read()
        out_f.write(filedata)
    os.remove(".temp2")

    print_msg(f"{white}[{green}+{white}] {green}File decrypted successfully")

    if move_path:
        if os.path.exists(move_path):
            destination = os.path.join(move_path, os.path.basename(output_file))
            os.system(f'mv -f "{output_file}" "{destination}"')
            return print_msg(f"{white}[{green}+{white}] {green}File decrypted and moved to your path {move_path}")
        else:
            return print_msg(f"{white}[{red}+{white}] {red}Path does not exist!")

    return True
