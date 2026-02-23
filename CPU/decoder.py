from CPU.flags import flags
from CPU.alu import alu
from CPU.pc import program_counter
from CPU.registers import registers
from CPU.cir import CurrentInstructionRegister

class Decoder:


    #This code makes every class a singleton, meaning that only one instance of each class can exist at a time.
    #In this CPU simulation, we want to ensure that there is only one ALU and one set of Flags, as they represent the state of the CPU.
    _instance = None

    def __init__(self):
        pass    
    
    def __new__(cls):
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(Decoder, cls).__new__(cls)
        return cls._instance

    
    def decode(self, instruction):
                
        instruction = CurrentInstructionRegister(instruction).current_instruction()

        print(f"Decoding instruction: {instruction}")


        match instruction:
            #Memory instructions
            case "LOAD":
                #TODO: Implement load instruction, need ram module first
                pass
            case "LOADV":
                self.load("A", 2000)
                #TODO: Implement loadv instruction, need to implement registers handling first
            case "STORE":
                #TODO: Implement store instruction, need ram module first
                pass
            case "PUSH":
                #TODO: Implement push instruction, need ram module first
                pass
            case "POP":
                #TODO: Implement pop instruction, need ram module first
                pass
            case "LEA":
                #TODO: Implement lea instruction, need ram module first
                # LEA loads a memory address into a register, so we need to implement memory addressing first
                pass
            #Arithmetic instructions
            case "ADD":
                result = alu.add(registers.values["0"], registers.values["1"])
                print(f"ALU Result: {result}")
            case "SUB":
                result = alu.subtract(registers.values["0"], registers.values["1"])
                print(f"ALU Result: {result}")
            case "MUL":
                result = alu.multiply(registers.values["0"], registers.values["1"])
                print(f"ALU Result: {result}")
            case "DIV":
                result = alu.divide(registers.values["0"], registers.values["1"])
                print(f"ALU Result: {result}")
            case "MOD":
                result = alu.modulo(registers.values["0"], registers.values["1"])
                print(f"ALU Result: {result}")
            #Copy command on 2 registers
            case "CPY":
                registers.values["2"] = registers.values["0"]
                print(f"Copied value from register 0 to register 2: {registers.values['2']}")
            #Increment and decrement commands on a register
            case "INC":
                registers.values["0"] += 1
                print(f"Incremented value in register 0: {registers.values['0']}")
            case "DEC":
                registers.values["0"] -= 1
                print(f"Decremented value in register 0: {registers.values['0']}")
            case "CMP":
                #TODO: Implement cmp instruction, substraction, it only set flags
                pass
            case "TEST":
                #TODO Implement test instruction, and instruction that only set flags
                pass
            case "AND":
                #TODO Implement and instruction, bitwise and
                pass
            case "OR":
                #TODO Implement or instruction, bitwise or
                pass
            case "XOR":
                #TODO Implement xor instruction, bitwise xor
                pass
            case "NOT":
                #TODO Implement not instruction, bitwise not
                pass
            case "NAND":
                #TODO Implement nand instruction, bitwise nand
                pass
            case "NOR":
                #TODO Implement nor instruction, bitwise nor
                pass
            case "SHL":
                #TODO Implement shl instruction, bitwise shift left
                pass
            case "SHR":
                #TODO Implement shr instruction, bitwise shift right
                pass
            case "ROL":
                #TODO Implement rol instruction, bitwise rotate left
                pass
            case "ROR":
                #TODO Implement ror instruction, bitwise rotate right
                pass
            case "JMP":
                #TODO Implement jmp instruction, jump to address
                pass
            case "JZ":
                #TODO Implement jz instruction, jump if zero flag is set
                pass
            case "JNZ":
                #TODO Implement jnz instruction, jump if zero flag is not set
                pass
            case "JP":
                #TODO Implement jp instruction, jump if positive flag is set
                pass
            case "JN":
                #TODO Implement jn instruction, jump if negative flag is set
                pass
            case "JC":
                #TODO Implement jc instruction, jump if carry flag is set
                pass
            case "JNC":
                #TODO Implement jnc instruction, jump if carry flag is not set
                pass
            case "JO":
                #TODO Implement jo instruction, jump if overflow flag is set
                pass
            case "JNO":
                #TODO Implement jno instruction, jump if overflow flag is not set
                pass
            case "CALL":
                #TODO Implement call instruction, call subroutine at address
                pass
            case "RET":
                #TODO Implement ret instruction, return from subroutine
                pass
            case "CLI":
                #TODO Implement cli instruction, clear interrupt flag
                pass
            case "STI":
                #TODO Implement sti instruction, set interrupt flag
                pass
            case "NOP":
                #TODO Implement nop instruction, no operation
                pass
            case "IN":
                #TODO Implement in instruction, input from port
                #Note: I do not think this instruction is needec, but is declared because it was defined, since it is an I/O related instruction, and the computer won't need it, I do not think this will be implemented in the foreseeable future.
                pass
            case "OUT":
                #TODO Implement out instruction, output to port
                #Note: Same as IN instruction. 
                pass


            

    

    def execute(self, instruction, ):
        pass

        
            

    def registerInstruction(self, register, value):
        registers.values[register] = value
        return registers.values[register]