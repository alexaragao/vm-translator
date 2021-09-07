# Mapeamentos

## Labels
```asm
// label LOOP

(LOOP)
```

## Jumps ("Saltos")
### Saltos incondicionais
```asm
// goto LOOP

@LOOP
0;JMP
```

### Saltos condicionais
```asm
// if-goto LOOP

@SP
AM=M-1
D=M
@LOOP
D;JNE
```

## Function
```asm
// label LOOP

(LOOP)
```

## Calls
```asm
// label LOOP

(LOOP)
```