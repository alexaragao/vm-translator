import sys

args = sys.argv

# Exige um path para um arquivo .vm
if len(args) != 2:
    exit(1)

file_path = args[1]

with open("out/out.asm", "w") as output:
    assembly_code = ""
    current_macro_index = 0

    with open(file_path, "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()  # Remove unwanted characters from line

            if len(line) == 0:  # Ignore empty lines
                continue
            if line[:2] == "//":  # Ignore comments
                continue

            command = line[:line.index(" ")] if " " in line else line

            assembly_code += f"// Parsing: {line}\n"
            if command == "push":
                # Extract data from line
                command, segment, value = line.split(" ")

                if segment == "constant":
                    assembly_code += f"@{value}\nD=A\n"
                else:
                    tmp = ""
                    maps = {
                        "local": "LCL",
                        "argument": "ARG",
                        "this": "THIS",
                        "that": "THAT",
                        "static": "16",
                    }
                    if segment == "static":
                        tmp = f"@VM.{current_macro_index}\n"
                        current_macro_index += 1
                    elif segment == "pointer":
                        tmp = f"@R13\n"
                    elif segment == "temp":
                        tmp = f"@R11\n"
                    else:
                        tmp += f"@{maps[segment]}\nD=M\n@{current_macro_index}\nA=D+A\n"
                        current_macro_index += 1
                    assembly_code += f"{tmp}D=M\n"

                assembly_code += f"@SP\nA=M\nM=D\n@SP\nM=M+1\n"

            elif command == "pop":
                command, segment, value = line.split(" ")

                tmp = ""
                maps = {
                    "local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT",
                    "static": "16",
                }
                if segment == "constant":
                    tmp = f"@{value}\n"
                if segment == "static":
                    tmp = f"@VM.{current_macro_index}\n"
                    current_macro_index += 1
                elif segment == "pointer":
                    tmp = f"@R13\n"
                elif segment == "temp":
                    tmp = f"@R11\n"
                else:
                    tmp += f"@{maps[segment]}\nD=M\n@{current_macro_index}\nA=D+A\n"
                    current_macro_index += 1

                assembly_code += f"{tmp}D=A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"

            else:
                # Unary operators
                if command != "neg" and command != "not":
                    assembly_code += "@SP\nM=M-1\nA=M\nD=M\n"

                assembly_code += "@SP\nM=M-1\n@SP\nA=M\n"

                if command == 'add':  # Arithmetic operators
                    assembly_code += f'M=M+D\n'
                elif command == 'sub':
                    assembly_code += f'M=M-D\n'
                elif command == 'and':
                    assembly_code += f'M=M&D\n'
                elif command == 'or':
                    assembly_code += f'M=M|D\n'
                elif command == 'neg':
                    assembly_code += f'M=-M\n'
                elif command == 'not':
                    assembly_code += f'M=!M\n'

    output.write(assembly_code)
