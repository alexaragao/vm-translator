@256
D=A
@SP
M=D
// push constant 7 | line 6
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8 | line 7
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// add | line 8
@SP
M=M-1
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
