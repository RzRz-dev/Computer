
from CPU.decoder import Decoder
#This import and the print registers.stack_pointer is just to test that the registers are working correctly. In a real CPU, the registers would be used to store data and instructions, and the stack pointer would be used to keep track of the top of the stack.
from CPU.registers import registers
from RAM.data_ram import data_ram
from CPU.flags import flags


def main():
    

    decoder1 = Decoder()

    decoder1.decode("121000000000000F")
    decoder1.decode("12200000000000F1")
    decoder1.decode("2000000000000810") 

    print(flags.CF, flags.ZF, flags.NF, flags.OF, flags.IF)

    print(registers.values)
    print(registers.stack_pointer)
    
    
    print(len("121FFFFFFFFFFFFF"))


if __name__ == "__main__":
    main()