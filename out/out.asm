@256
D=A
@SP
M=D
// Parsing: push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: pop local 0
@LCL
D=M
@0
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: push constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: push constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: pop argument 2
@ARG
D=M
@1
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: pop argument 1
@ARG
D=M
@2
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: push constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: pop this 6
@THIS
D=M
@3
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: push constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: push constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: pop that 5
@THAT
D=M
@4
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: pop that 2
@THAT
D=M
@5
A=D+A
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: push constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// Parsing: pop temp 6
@R11
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// Parsing: push local 0
@LCL
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: push that 5
@THAT
D=M
@7
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
// Parsing: push argument 1
@ARG
D=M
@8
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
// Parsing: push this 6
@THIS
D=M
@9
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: push this 6
@THIS
D=M
@10
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
// Parsing: sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
// Parsing: push temp 6
@R11
D=M
@SP
A=M
M=D
@SP
M=M+1
// Parsing: add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
