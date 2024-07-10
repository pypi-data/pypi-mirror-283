# clearshell 1.2.0

`clearshell` is a Python package designed to decrypt bash scripts obfuscated with `eval`. This tool allows you to easily decrypt these scripts either from the command line or within your Python code.

## Features

- Decrypts bash scripts obfuscated with `eval`.
- Optionally moves the decrypted file to a specified directory.
- Usable both from the command line and as an importable Python module.

## Installation

You can install the `clearshell` package using `pip`:

```bash
pip install clearshell
```

## Command-Line Usage

To decrypt a bash script and save the output:

```bash
clearshell --decrypt input_file.sh decrypted_file.sh
```

To decrypt a bash script and move the decrypted file to a specified directory:

```bash
clearshell --decrypt input_file.sh decrypted_file.sh --move /path/to/destination
```

### Examples

**Basic Decryption:**

```bash
clearshell --decrypt obfuscated.sh decrypted.sh
```

**Decryption with Move:**

```bash
clearshell --decrypt obfuscated.sh decrypted.sh --move /path/to/destination
```

## Python Module Usage

You can also use `clearshell` directly within your Python scripts.

### Examples

**Basic Decryption:**

```python
import clearshell

input_file = "obfuscated.sh"
output_file = "decrypted.sh"

if clearshell.decryptsh(input_file, output_file):
    print("Decrypted successfully")
else:
    print("Decryption failed")
```

**Decryption with Move:**

```python
import clearshell

input_file = "obfuscated.sh"
output_file = "decrypted.sh"
move_path = "/path/to/destination"

if clearshell.decryptsh(input_file, output_file, move_path):
    print("Decrypted and moved successfully")
    print(f"Moved to: {move_path}")
else:
    print("Decryption failed")
```

## Thank You

Thank you for using `clearshell`. We hope it helps you in your scripting and security endeavors. If you have any feedback or suggestions, feel free to contribute to the project on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Author

Developed by [Fidal](https://github.com/mr-fidal).

---

Thank you for using `clearshell`! Have a great day!
