from CPU.flags import flags
from CPU.alu import alu
from CPU.pc import program_counter
from CPU.registers import registers
from CPU.cir import CurrentInstructionRegister
from RAM.data_ram import data_ram
from RAM.stack import stack_ram

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
            #LOAD
            case instruction if instruction[0:2] == "11":
                register = instruction[2]
                address = instruction[3:]
                registers.values[register] = address

                print("Load memory address "+str(address)+" in register "+str(register))
            #LOADV
            case instruction if instruction[0:2] == "12":
                register = instruction[2]
                value = instruction[3:]
                registers.values[register] = value

                print("Load value "+value+" in register "+register)
            #STORE
            case instruction if instruction[0:2] == "13":
                register = instruction[2]
                address = instruction[3:]
                data_ram.write(address, registers.values[register])

                print("Store value of register "+str(register)+" in memory address "+str(address))
            #PUSH
            case instruction if instruction[0:15] == "10000000000000":
                register = instruction[-1]
                stack_ram.push(registers.values[register])
                print("Push value of register "+str(register)+" on the stack")
                #TODO: Implement push instruction, need stack module first
            #POP
            case instruction if instruction[0:15] == "10000000000001":
                register = instruction[-1]
                stack_ram.pop()
                print("Pop value from stack into register "+str(register))
            #LEA
            case instruction if instruction[0:2] == "16":
                register = instruction[2]
                address = instruction[3:]
                registers.values[register] = data_ram.read(address)
                print("Load memory address "+str(address)+" in register "+str(register))
            #Arithmetic instructions, about these bitwise instructions
            #If I don't want to use numbers, but binary we have to modify this
            #ADD
            case instruction if instruction[0:14] == "20000000000001":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.add(registers.values[register1], registers.values[register2])
                print(f"ALU add Result: {registers.values[register1]} in register {register1}")
            #SUB
            case instruction if instruction[0:14] == "20000000000002":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.subtract(registers.values[register1], registers.values[register2])
                print(f"ALU subtract Result: {registers.values[register1]} in register {register1}")
            #MUL
            case instruction if instruction[0:14] == "20000000000003":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.multiply(registers.values[register1], registers.values[register2])
                print(f"ALU multiply Result: {registers.values[register1]} in register {register1}")
            #DIV
            case instruction if instruction[0:14] == "20000000000004":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.divide(registers.values[register1], registers.values[register2])
                print(f"ALU divide Result: {registers.values[register1]} in register {register1}")
            #MOD
            case instruction if instruction[0:14] == "20000000000005":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.modulo(registers.values[register1], registers.values[register2])
                print(f"ALU modulo Result: {registers.values[register1]} in register {register1}")
            #CPY Copy command, copy value from second register to first another
            case instruction if instruction[0:14] == "20000000000006":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = registers.values[register2]
                print(f"Copied value from register {register2} to register {register1}: {registers.values[register1]}")
            #INC
            case instruction if instruction[0:14] == "20000000000007":
                register = instruction[14]
                registers.values[register] = alu.increment(registers.values[register])
                print(f"Incremented value in register {register}: {registers.values[register]}")
            #DEC
            case instruction if instruction[0:14] == "20000000000008":
                register = instruction[14]
                registers.values[register] = alu.decrement(registers.values[register])
                print(f"Decremented value in register {register}: {registers.values[register]}")
            #CMP
            case instruction if instruction[0:14] == "2000000000000E":
                register1 = instruction[14]
                register2 = instruction[15]
                alu.subtract(registers.values[register1], registers.values[register2])
                #TODO: Implement cmp instruction, substraction, it only set flags, it has to be implemented in ALU
            #TEST
            case instruction if instruction[0:14] == "2000000000000F":
                register1 = instruction[14]
                register2 = instruction[15]
                #TODO Implement test instruction, and instruction that only set flags, has to be implemented in ALU    
            #AND
            case instruction if instruction[0:14] == "20000000000011":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = registers.values[register1] & registers.values[register2]
                print(f"AND Result: {registers.values[register1]} in register {register1}")
            #OR
            case instruction if instruction[0:14] == "20000000000012":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = registers.values[register1] | registers.values[register2]
                print(f"OR Result: {registers.values[register1]} in register {register1}")
            #XOR
            case instruction if instruction[0:14] == "20000000000013":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = registers.values[register1] ^ registers.values[register2]
                print(f"XOR Result: {registers.values[register1]} in register {register1}")
            #NOT
            case instruction if instruction[0:14] == "20000000000014":
                register = instruction[14]
                registers.values[register] = ~registers.values[register]
                print(f"NOT Result: {registers.values[register]} in register {register}")
            #NAND
            case instruction if instruction[0:14] == "20000000000015":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = ~(registers.values[register1] & registers.values[register2])
                print(f"NAND Result: {registers.values[register1]} in register {register1}")
            #NOR
            case instruction if instruction[0:14] == "20000000000016":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = ~(registers.values[register1] | registers.values[register2])
                print(f"NOR Result: {registers.values[register1]} in register {register1}")
            #SHIFTLEFT
            case instruction if instruction[0:14] == "30000000000001":
                register1 = instruction[14]
                register2 = instruction[15]
                #Left shift the value in register1 by the number of bits specified in register2
                registers.values[register1] = registers.values[register1] << registers.values[register2]
                print(f"Left Shift Result: {registers.values[register1]}")
                print(bin(registers.values[register1]))
            #SHIFTRIGHT
            case instruction if instruction[0:14] == "30000000000002":
                register1 = instruction[14]
                register2 = instruction[15]
                #Right shift the value in register1 by the number of bits specified in register2
                registers.values[register1] = registers.values[register1] >> registers.values[register2]
                print(f"Right Shift Result: {registers.values[register1]}")
                print(bin(registers.values[register1]))
            #ROL ROTATION LEFT
            case instruction if instruction[0:14] == "30000000000003":
                register1 = instruction[14]
                register2 = instruction[15]
                #Rotate left the value in register1 by the number of bits specified in register2
                registers.values[register1] = (registers.values[register1] << registers.values[register2]) | (registers.values[register1] >> (32 - registers.values[register2]))
                print(f"Rotate Left Result: {registers.values[register1]}")
            #ROR ROTATION RIGHT
            case instruction if instruction[0:14] == "30000000000004":
                register1 = instruction[14]
                register2 = instruction[15]
                #Rotate right the value in register1 by the number of bits specified in register2
                registers.values[register1] = (registers.values[register1] >> registers.values[register2]) | (registers.values[register1] << (32 - registers.values[register2]))
                print(f"Rotate Right Result: {registers.values[register1]}")
            #JUMP
            case instruction if instruction[0:3] == "700":
                address = instruction[3:]
                #TODO Implement jmp instruction, jump to address, memory addressing needs to be implemented first.
                pass
            #JZ Jump if Zero flag is set
            case instruction if instruction[0:3] == "701":
                address = instruction[3:]
                #TODO Implement jz instruction, jump if zero flag is set, memory addressing needs to be implemented first-
                pass
            #JNZ Jump if Zero flag is not set
            case instruction if instruction[0:3] == "702":
                address = instruction[3:]
                #TODO Implement jnz instruction, jump if zero flag is not set
                pass
            #JP Jump if Positive flag is set
            case instruction if instruction[0:3] == "703":
                address = instruction[3:]
                #TODO Implement jp instruction, jump if positive flag is set
                pass
            #JN Jump if Negative flag is set
            case instruction if instruction[0:3] == "704":
                address = instruction[3:]
                #TODO Implement jn instruction, jump if negative flag is set
                pass
            #JC Jump if Carry flag is set
            case instruction if instruction[0:3] == "705":
                address = instruction[3:]
                #TODO Implement jc instruction, jump if carry flag is set
                pass
            #JNC Jump if Carry flag is not set
            case instruction if instruction[0:3] == "706":
                #TODO Implement jnc instruction, jump if carry flag is not set
                pass
            #JO Jump if Overflow flag is set
            case instruction if instruction[0:3] == "707":
                #TODO Implement jo instruction, jump if overflow flag is set
                pass
            #JNO Jump if Overflow flag is not set
            case instruction if instruction[0:3] == "708":
                #TODO Implement jno instruction, jump if overflow flag is not set
                pass
            #CALL a subroutine at address
            case instruction if instruction[0:3] == "709":
                #TODO Implement call instruction, call subroutine at address
                pass
            #RET Return from subroutine
            case instruction if instruction[0:16] == "70A0000000000000":
                #TODO Implement ret instruction, return from subroutine
                pass
            
            case instruction if instruction[0:16] == "0000000000000000":
                #TODO Stop the program
                pass

            #Interrupt instructions, these functions will not be implemented in the foreseeable future, since they are related to interrupts and I do not plan on implementing interrupts in this CPU simulation, but they are declared here for completeness and future implementation.
            #CLI Clear Interrupt Flag
            case instruction if instruction[0:16] == "0000000000000001":
                pass
            #STI Set Interrupt Flag
            case instruction if instruction[0:16] == "0000000000000002":
                pass
            #IN Port Input
            case instruction if instruction[0:13] == "9000000000000":
                pass
            #OUT Port Output
            case instruction if instruction[0:13] == "9000000000001":
                pass


            

    

    def execute(self, instruction, ):
        pass

        
            

    def registerInstruction(self, register, value):
        registers.values[register] = value
        return registers.values[register]