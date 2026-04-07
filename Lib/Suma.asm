JMP endLibrary

suma:
POP R6
POP R7
POP R8
ADD R7,R8
PUSH R7
PUSH R6
RET

endLibrary: