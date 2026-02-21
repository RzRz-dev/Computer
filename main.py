
from CPU.decoder import Decoder
from CPU.registers import registers


def main():
    
    #This main will work as the buses, connecting the different components of the CPU together. In a real CPU, the buses would be responsible for transferring data between the different components, such as the ALU, the program counter, and the flags. In this simulation, we will use the main function to create instances of the different components and call their methods to simulate the operation of a CPU.
    decoder1 = Decoder()
    decoder1.decode("Instruction1")
    decoder1.decode("Instruction2")
    decoder1.decode("Instruction3")
    decoder1.decode("Instruction4")
    decoder1.decode("SetRegister")
    decoder1.decode("GetRegister")

    print(registers.stack_pointer)



if __name__ == "__main__":
    main()