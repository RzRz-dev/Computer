JMP endLibrary

; ========================
; ARRAY OPERATIONS
; ========================

; getElementArray: Obtiene elemento del array en índice especificado
; Stack on entry: [arr_addr, size, index]
; Returns: R14 = arr[index], or -1 if out of bounds
; Uses: R0=arr_addr, R1=size, R2=index, R14=result
getElementArray:
	POP R15           ; return address
	POP R2            ; index
	POP R1            ; size
	POP R0            ; array base address

	; Validate 0 <= index < size
	CMP R2, 0
	JN getElemFail    ; if index < 0, fail
	CMP R2, R1
	JNC getElemFail   ; if index >= size, fail

	; Calculate address: R0 = arr + index
	ADD R0, R2
	MOV R14, R0      ; R14 = arr[index]
	JMP getElemEnd

getElemFail:
	LOADV R14, -1     ; error code

getElemEnd:
	PUSH R14          ; result
	PUSH R15          ; return address
	RET

; setElementArray: Modifica elemento del array en índice especificado
; Stack on entry: [arr_addr, size, index, value]
; Returns: nothing
; Uses: R0=arr_addr, R1=size, R2=index, R3=value
setElementArray:
	POP R15           ; return address
	POP R3            ; value
	POP R2            ; index
	POP R1            ; size
	POP R0            ; array base address

	; Validate 0 <= index < size
	CMP R2, 0
	JN setElemEnd     ; if index < 0, skip
	CMP R2, R1
	JNC setElemEnd    ; if index >= size, skip

	; Calculate address: R0 = arr + index
	ADD R0, R2
	STORE R3, R0      ; arr[index] = value

setElemEnd:
	PUSH R15          ; return address
	RET

; findElementArray: Busca elemento por valor en el array
; Stack on entry: [arr_addr, size, value]
; Returns: R14 = index if found, -1 if not found
; Uses: R0=arr_addr, R1=size, R2=value, R3=index, R4=current_value
findElementArray:
	POP R15           ; return address
	POP R2            ; value to find
	POP R1            ; size
	POP R0            ; array base address

	LOADV R3, 0       ; i = 0

findLoop:
	CMP R3, R1        ; compare i with size
	JNC findNotFound  ; if i >= size, not found

	; Load array[i]
	CPY R4, R0        ; R4 = arr base
	ADD R4, R3        ; R4 = &arr[i]
	LOAD R4, R4       ; R4 = arr[i]

	; Compare with target value
	CMP R4, R2
	JZ findFound      ; if equal, found it

	; Increment counter
	ADD R3, 1
	JMP findLoop

findFound:
	CPY R14, R3       ; R14 = index
	JMP findEnd

findNotFound:
	LOADV R14, -1     ; R14 = -1 (not found)

findEnd:
	PUSH R14          ; result
	PUSH R15          ; return address
	RET

; ========================
; MATRIX OPERATIONS
; ========================

; getElementMatrix: Obtiene elemento de la matriz en posición [i][j]
; Stack on entry: [matrix_addr, rows, cols, i, j]
; Returns: R14 = matrix[i][j], or -1 if out of bounds
; Uses: R0=matrix_addr, R1=rows, R2=cols, R3=i, R4=j, R5=index
getElementMatrix:
	POP R15           ; return address
	POP R4            ; j
	POP R3            ; i
	POP R2            ; cols
	POP R1            ; rows
	POP R0            ; matrix base address

	; Validate 0 <= i < rows
	CMP R3, 0
	JN getMatFail     ; if i < 0, fail
	CMP R3, R1
	JNC getMatFail    ; if i >= rows, fail

	; Validate 0 <= j < cols
	CMP R4, 0
	JN getMatFail     ; if j < 0, fail
	CMP R4, R2
	JNC getMatFail    ; if j >= cols, fail

	; Calculate linear index: index = i * cols + j
	CPY R5, R3        ; R5 = i
	MUL R5, R2        ; R5 = i * cols
	ADD R5, R4        ; R5 = i * cols + j

	; Load value: matrix_addr[index]
	ADD R0, R5
	LOAD R14, R0      ; R14 = matrix[i][j]
	JMP getMatEnd

getMatFail:
	LOADV R14, -1     ; error code

getMatEnd:
	PUSH R14          ; result
	PUSH R15          ; return address
	RET

; setElementMatrix: Modifica elemento de la matriz en posición [i][j]
; Stack on entry: [matrix_addr, rows, cols, i, j, value]
; Returns: nothing
; Uses: R0=matrix_addr, R1=rows, R2=cols, R3=i, R4=j, R5=value, R6=index
setElementMatrix:
	POP R15           ; return address
	POP R5            ; value
	POP R4            ; j
	POP R3            ; i
	POP R2            ; cols
	POP R1            ; rows
	POP R0            ; matrix base address

	; Validate 0 <= i < rows
	CMP R3, 0
	JN setMatEnd      ; if i < 0, skip
	CMP R3, R1
	JNC setMatEnd     ; if i >= rows, skip

	; Validate 0 <= j < cols
	CMP R4, 0
	JN setMatEnd      ; if j < 0, skip
	CMP R4, R2
	JNC setMatEnd     ; if j >= cols, skip

	; Calculate linear index: index = i * cols + j
	CPY R6, R3        ; R6 = i
	MUL R6, R2        ; R6 = i * cols
	ADD R6, R4        ; R6 = i * cols + j

	; Store value: matrix[index] = value
	ADD R0, R6
	STORE R5, R0      ; matrix[i][j] = value

setMatEnd:
	PUSH R15          ; return address
	RET

endLibrary:
