from CPU.alu import alu
from CPU.registers import registers
class ALUController:
    def readALUInstruction(opcode, midcode, registerA, registerB):
        register1 = registers.values[registerA]
        register2 = registers.values[registerB]
        if opcode=="20":
            match midcode:
                case "01": #ADD
                    registers.values[registerA] = alu.add(register1, register2)
                case "02": #SUB
                    registers.values[registerA] = alu.subtract(register1, register2)
                case "03": #MUL
                    registers.values[registerA] = alu.multiply(register1, register2)
                case "04": #DIV
                    registers.values[registerA] = alu.divide(register1, register2)
                case "05": #MOD
                    registers.values[registerA] = alu.modulo(register1, register2)
                case "06": #CPY
                    registers.values[registerA] = registers.values[registerB]
                case "07": #INC
                    registers.values[registerA] = alu.increment(registers.values[registerA])
                case "08": #DEC
                    registers.values[registerA] = alu.decrement(registers.values[registerA])
                case "0E": #CMP
                    alu.subtract(register1, register2)
                case "0F": #TEST
                    alu.bitwise_and(register1, register2)
                case "11": #AND
                    registers.values[registerA] = alu.bitwise_and(register1, register2)
                case "12": #OR
                    registers.values[registerA] = alu.bitwise_or(register1, register2)
                case "13": #XOR
                    registers.values[registerA] = alu.bitwise_xor(register1, register2)
                case "14": #NOT
                    registers.values[registerA] = alu.bitwise_not(register1)
                case "15": #NAND
                    registers.values[registerA] = alu.bitwise_nand(register1, register2)
                case "16": #NOR
                    registers.values[registerA] = alu.bitwise_nor(register1, register2)
        if opcode=="30":
            match midcode:
                case"01": #SHL
                    registers.values[registerA] = alu.shl(register1, register2)
                case"02": #SHR
                    registers.values[registerA] = alu.shr(register1, register2)
                case"03": #ROL
                    registers.values[registerA] = alu.rol(register1, register2)
                case"04": #ROR
                    registers.values[registerA] = alu.ror(register1, register2)