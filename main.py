import sys, os

args = sys.argv

# Exige um path para um arquivo .vm
if len(args) != 2:
    exit(1)

file_path = args[1]
FILE_BASE_NAME = os.path.basename(file_path)
FILE_NAME, FILE_EXTENSION = os.path.splitext(FILE_BASE_NAME)

CURRENT_TRANS_IF_GOTO = 0
CURRENT_TRANS_GOTO = 1
CURRENT_TRANS_LABEL = 2
CURRENT_TRANS_RETURN = 3
CURRENT_TRANS_FUNCTION = 4
CURRENT_TRANS_CALL = 5

POP_STACK = "@SP\nM=M-1\nA=M\nD=M"

OUTPUT_FILEPATH = os.path.dirname(file_path) + "/" + FILE_NAME + ".asm"

with open(OUTPUT_FILEPATH, "w") as output:
    assembly_code = ""
    current_translating = None
    
    current_bool_index = 0
    current_call = 0
    current_macro_index = None
    current_function_name = None

    with open(file_path, "r") as file:
        lines = file.readlines()

        for (nrow, line) in enumerate(lines):
            line = line.strip()  # Remove unwanted characters from line

            if len(line) == 0:  # Ignore empty lines
                continue
            if line[:2] == "//":  # Ignore comments
                continue

            if "//" in line:
                line = line[:line.index("//")].strip()

            command = line[:line.index(" ")] if " " in line else line

            # assembly_code += f"// {line} | line {nrow}\n"
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
                        tmp = f"@{FILE_NAME}.{value}\n"
                    elif segment == "pointer":
                        tmp = f"@R13\n"
                    elif segment == "temp":
                        tmp = f"@R11\n"
                    else:
                        tmp += f"@{maps[segment]}\nD=M\n@{value}\nA=D+A\n"
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
                    tmp = f"@{FILE_NAME}.{value}\n"
                elif segment == "pointer":
                    tmp = f"@R13\n"
                elif segment == "temp":
                    tmp = f"@R11\n"
                else:
                    tmp += f"@{maps[segment]}\nD=M\n@{value}\nA=D+A\n"

                assembly_code += f"{tmp}D=A\n@R13\nM=D\n{POP_STACK}\n@R13\nA=M\nM=D\n"

            elif command == "function":
                command, functionName, nLocalVars = line.split(" ")
                current_translating = CURRENT_TRANS_FUNCTION
                assembly_code += f"({functionName})\n"
                current_function_name = functionName
                pass
                
            elif command == "return":
                current_translating = CURRENT_TRANS_RETURN
                assembly_code += f"@LCL\nD=M\n@R13\nM=D\n@R13\nD=M\n@5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n{POP_STACK}\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n"

                for (id, segment) in enumerate(["@THAT", "@THIS", "@ARG", "@LCL"]):
                    assembly_code += f"@R13\nD=M\n@{str(1+id)}\nD=D-A\nA=D\nD=M\n{segment}\nM=D\n"
                    
                assembly_code += f"@R14\nA=M\n0;JMP\n"
                pass
                
            elif command == "if-goto":
                command, labelName = line.split(" ")
                current_translating = CURRENT_TRANS_IF_GOTO
                assembly_code += f'{POP_STACK}\n@{FILE_NAME}${labelName}\nD;JNE\n'
                pass
            
            elif command == "goto":
                command, labelName = line.split(" ")
                current_translating = CURRENT_TRANS_GOTO
                assembly_code += f"@{FILE_NAME}${labelName}\n0;JMP\n"
                pass
            
            elif command == "label":
                command, labelName = line.split(" ")
                if current_macro_index == CURRENT_TRANS_FUNCTION:
                    assembly_code += f"({current_function_name}${labelName})\n"
                else:
                    assembly_code += f"({FILE_NAME}${labelName})\n"
                pass

            elif command == "call":
                command, functionName, nargs = line.split(" ")
                CALL_UUID = f"{functionName}_CALL_{current_call}"
                assembly_code += f"@{CALL_UUID}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                for segment in ["@LCL", "@ARG", "@THIS", "@THAT"]:
                    assembly_code += f"{segment}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                assembly_code += f"@SP\nD=M\n@LCL\nM=D\n@{5 + int(nargs)}\nD=D-A\n@ARG\nM=D\n@{functionName}\n0;JMP\n({CALL_UUID})\n"

                current_call += 1
            else:
                # Unary operators
                if command != "neg" and command != "not":
                    assembly_code += f"{POP_STACK}\n"

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
                elif command == 'eq':
                    assembly_code += f'D=M-D\n@BOOL{current_bool_index}\nD;JEQ\n'
                    assembly_code += f'@SP\nA=M\nM=0\n@ENDBOOL{current_bool_index}\n0;JMP\n'
                    assembly_code += f'(BOOL{current_bool_index})\n@SP\nA=M\nM=-1\n(ENDBOOL{current_bool_index})\n'
                
                    current_bool_index += 1

                elif command == 'gt':
                    assembly_code += f'D=M-D\n@BOOL{current_bool_index}\nD;JGT\n'
                    assembly_code += f'@SP\nA=M\nM=0\n@ENDBOOL{current_bool_index}\n0;JMP\n'
                    assembly_code += f'(BOOL{current_bool_index})\n@SP\nA=M\nM=-1\n(ENDBOOL{current_bool_index})\n'
                
                    current_bool_index += 1
                
                elif command == 'lt':
                    assembly_code += f'D=M-D\n@BOOL{current_bool_index}\nDPerdão professora, já fiz tanta coisa hoje que acabei esquecendo;JLT\n'
                    assembly_code += f'@SP\nA=M\nM=0\n@ENDBOOL{current_bool_index}\n0;JMP\n'
                    assembly_code += f'(BOOL{current_bool_index})\n@SP\nA=M\nM=-1\n(ENDBOOL{current_bool_index})\n'
                    
                    current_bool_index += 1
                assembly_code += "@SP\nM=M+1\n"

    # output.write("@256\nD=A\n@SP\nM=D\n")
    output.write(assembly_code)
