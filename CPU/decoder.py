from CPU.alu import alu
from CPU.registers import registers
from RAM.data_ram import data_ram
from RAM.stack import stack_ram
from CPU.pc import pc
from CPU.flags import Flags

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
                
    


        print(f"Decoding instruction: {instruction}")

        match instruction:
            #LOAD
            case instruction if instruction[0:2] == "11":
                register = instruction[2]
                address = instruction[3:]
                registers.values[register] = data_ram.read(address)

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
                print(f"Compared value in register {register1} with value in register {register2}")
            #TEST
            case instruction if instruction[0:14] == "2000000000000F":
                register1 = instruction[14]
                register2 = instruction[15]
                alu.bitwise_and(registers.values[register1], registers.values[register2])
                print(f"Tested value in register {register1} with value in register {register2}")
            #AND
            case instruction if instruction[0:14] == "20000000000011":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.bitwise_and(registers.values[register1], registers.values[register2])
                print(f"AND Result: {registers.values[register1]} in register {register1}")
            #OR
            case instruction if instruction[0:14] == "20000000000012":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.bitwise_or(registers.values[register1], registers.values[register2])
                print(f"OR Result: {registers.values[register1]} in register {register1}")
            #XOR
            case instruction if instruction[0:14] == "20000000000013":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.bitwise_xor(registers.values[register1], registers.values[register2])
                print(f"XOR Result: {registers.values[register1]} in register {register1}")
            #NOT
            case instruction if instruction[0:14] == "20000000000014":
                register = instruction[14]
                registers.values[register] = alu.bitwise_not(registers.values[register])
                print(f"NOT Result: {registers.values[register]} in register {register}")
            #NAND
            case instruction if instruction[0:14] == "20000000000015":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.bitwise_nand(registers.values[register1], registers.values[register2])
                print(f"NAND Result: {registers.values[register1]} in register {register1}")
            #NOR
            case instruction if instruction[0:14] == "20000000000016":
                register1 = instruction[14]
                register2 = instruction[15]
                registers.values[register1] = alu.bitwise_nor(registers.values[register1], registers.values[register2])
                print(f"NOR Result: {registers.values[register1]} in register {register1}")
            #SHIFTLEFT
            case instruction if instruction[0:14] == "30000000000001":
                register1 = instruction[14]
                register2 = instruction[15]
                #Left shift the value in register1 by the number of bits specified in register2
                registers.values[register1] = alu.shl(registers.values[register1], registers.values[register2])
                print(f"Left Shift Result: {registers.values[register1]}")
            #SHIFTRIGHT
            case instruction if instruction[0:14] == "30000000000002":
                register1 = instruction[14]
                register2 = instruction[15]
                #Right shift the value in register1 by the number of bits specified in register2
                registers.values[register1] = alu.shr(registers.values[register1], registers.values[register2])
                print(f"Right Shift Result: {registers.values[register1]}")
            #ROL ROTATION LEFT
            case instruction if instruction[0:14] == "30000000000003":
                register1 = instruction[14]
                register2 = instruction[15]
                #Rotate left the value in register1 by the number of bits specified in register2
                registers.values[register1] = alu.rol(registers.values[register1], registers.values[register2])
                print(f"Rotate Left Result: {registers.values[register1]}")
            #ROR ROTATION RIGHT
            case instruction if instruction[0:14] == "30000000000004":
                register1 = instruction[14]
                register2 = instruction[15]
                #Rotate right the value in register1 by the number of bits specified in register2
                registers.values[register1] = alu.ror(registers.values[register1], registers.values[register2])
                print(f"Rotate Right Result: {registers.values[register1]}")
            #JUMP
            case instruction if instruction[0:3] == "700":
                address = instruction[3:]
                pc.set_next_instruction(address)
                

            #JZ Jump if Zero flag is set
            case instruction if instruction[0:3] == "701":
                address = instruction[3:]
                if Flags.ZF == 1:
                    pc.set_next_instruction(address)

            #JNZ Jump if Zero flag is not set
            case instruction if instruction[0:3] == "702":
                address = instruction[3:]
                if Flags.ZF == 0:
                    pc.set_next_instruction(address)

            #JP Jump if Negative flag is not set
            case instruction if instruction[0:3] == "703":
                address = instruction[3:]
                if Flags.NF == 0:
                    pc.set_next_instruction(address)
                    print(f"Jump to: {address}")
            #JN Jump if Negative flag is set
            case instruction if instruction[0:3] == "704":
                address = instruction[3:]
                if Flags.NF == 1:
                    pc.set_next_instruction(address)
                    print(f"Jump to: {address}")
            #JC Jump if Carry flag is set
            case instruction if instruction[0:3] == "705":
                address = instruction[3:]
                if Flags.CF == 1:
                    pc.set_next_instruction(address)

            #JNC Jump if Carry flag is not set
            case instruction if instruction[0:3] == "706":
                address = instruction[3:]
                if Flags.CF == 0:
                    pc.set_next_instruction(address)

            #JO Jump if Overflow flag is set
            case instruction if instruction[0:3] == "707":
                address = instruction[3:]
                if Flags.OF == 1:
                    pc.set_next_instruction(address)

            #JNO Jump if Overflow flag is not set
            case instruction if instruction[0:3] == "708":
                address = instruction[3:]
                if Flags.OF == 0:
                    pc.set_next_instruction(address)

            #For the moment subroutines will not be implemented, since it needs an special register that remembers where is the last instruction to come back later
            #CALL a subroutine at address
            case instruction if instruction[0:3] == "709":
                
                #TODO Implement call instruction, call subroutine at address
                pass

            #RET Return from subroutine
            case instruction if instruction[0:16] == "70A0000000000000":
                #TODO Implement ret instruction, return from subroutine
                pass
            
            case instruction if instruction[0:16] == "0000000000000000":
                pass

            #Interrupt instructions, these functions will not be implemented in the foreseeable future, since they are related to interrupts and I do not plan on implementing interrupts in this CPU simulation, but they are declared here for completeness and future implementation.
            #CLI Clear Interrupt Flag
            case instruction if instruction[0:16] == "0000000000000001":
                Flags.IF = 0

            #STI Set Interrupt Flag
            case instruction if instruction[0:16] == "0000000000000002":
                Flags.IF = 1

            #IN Port Input
            case instruction if instruction[0:13] == "9000000000000":
                pass
            #OUT Port Output
            case instruction if instruction[0:13] == "9000000000001":
                pass


            

    


        
