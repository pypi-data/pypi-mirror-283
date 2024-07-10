import re
import os

def decryptsh(input_file, output_file, move_path=None):
    with open(input_file, 'r') as f:
        encrypted_script = f.read()

    decrypted_script = encrypted_script
    eval_pattern = re.compile(r'eval\s+"(.*?)"', re.DOTALL)
    matches = eval_pattern.findall(encrypted_script)
    for match in matches:
        decrypted_code = bytes.fromhex(match).decode('utf-8')
        decrypted_script = decrypted_script.replace(f'eval "{match}"', decrypted_code)

    with open(output_file, 'w') as f:
        f.write("# Decrypted by clearshell\n\n")
        f.write(decrypted_script)

    if move_path:
        os.makedirs(move_path, exist_ok=True)
        final_path = os.path.join(move_path, output_file)
        os.rename(output_file, final_path)
        return final_path
    else:
        return os.path.abspath(output_file)
