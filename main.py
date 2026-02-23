
from CPU.decoder import Decoder
#This import and the print registers.stack_pointer is just to test that the registers are working correctly. In a real CPU, the registers would be used to store data and instructions, and the stack pointer would be used to keep track of the top of the stack.
from CPU.registers import registers


def main():
    
    #This main will work as the buses, connecting the different components of the CPU together. In a real CPU, the buses would be responsible for transferring data between the different components, such as the ALU, the program counter, and the flags. In this simulation, we will use the main function to create instances of the different components and call their methods to simulate the operation of a CPU.
    decoder1 = Decoder()
    decoder1.decode("ADD")
    decoder1.decode("SUB")
    decoder1.decode("MUL")
    decoder1.decode("DIV")
    decoder1.decode("LOADV")

    print(registers.values)
    print(registers.stack_pointer)



if __name__ == "__main__":
    main()