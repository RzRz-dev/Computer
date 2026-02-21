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
        
        
        
        registers.values["0000"] = 5
        registers.values["0001"] = 3

        
        if instruction == "Instruction1":

            result = alu.add(registers.values["0000"], registers.values["0001"])
            print(f"ALU Result: {result}")


        if instruction == "Instruction2":

            result = alu.subtract(registers.values["0000"], registers.values["0001"])
            print(f"ALU Result: {result}")

        
        if instruction == "Instruction3":

            result = alu.multiply(registers.values["0000"], registers.values["0001"])
            print(f"ALU Result: {result}")


        if instruction == "Instruction4":

            result = alu.divide(registers.values["0000"], registers.values["0001"])
            print(f"ALU Result: {result}")

        
        if instruction == "SetRegister":
            self.registerInstruction("0010", 10)
            self.registerInstruction("0011", 20)
            print("Registers successfully set.")
        
        if instruction == "GetRegister":
            print(registers.values)
        
    
    def registerInstruction(self, register, value):
        registers.values[register] = value
        return registers.values[register]