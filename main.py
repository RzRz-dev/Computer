
from CPU.decoder import Decoder
#This import and the print registers.stack_pointer is just to test that the registers are working correctly. In a real CPU, the registers would be used to store data and instructions, and the stack pointer would be used to keep track of the top of the stack.
from CPU.registers import registers


def main():
    
    registers.values['1'] = 5
    registers.values['2'] = 10
    #This main will work as the buses, connecting the different components of the CPU together. In a real CPU, the buses would be responsible for transferring data between the different components, such as the ALU, the program counter, and the flags. In this simulation, we will use the main function to create instances of the different components and call their methods to simulate the operation of a CPU.
    decoder1 = Decoder()
    #decoder1.decode("2000000000000112") #This instruction will add the values in registers 1 and 2 and store the result in register 1
    #decoder1.decode("2000000000000212") #Subtract the values in registers 1 and 2 and store the result in register 1
    #decoder1.decode("2000000000000312") #Multiply the values in registers 1 and 2 and store the result in register 1
    #decoder1.decode("2000000000000412") #Divide the values in registers 1 and 2 and store the result in register 1
    #decoder1.decode("2000000000000512") #Modulo the values in registers 1 and 2 and store the result in register 1


    registers.values['5'] = 4
    decoder1.decode("2000000000000645") #Value of register 5 into register 4
    registers.values['4'] = 23
    decoder1.decode("3000000000000345") #ROL

    print(registers.values)
    print(registers.stack_pointer)

    testinst = "9000000000000123" #This instruction will load a value in memory

    print(testinst[14:16])



if __name__ == "__main__":
    main()