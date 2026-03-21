

from RAM.dataRam import ram
from Utilities.loader import Loader
from Utilities.execute import Execute
from CPU.registers import registers

def main():

    # Define the base in Hex
    base_hex = int("0F", 16)  # This is 15

    #Loader, makes the space in ram for the load of data
    loader = Loader(ram, base_hex)
    # This loads the program into the ram
    loader.load_program("program1.txt")

    # Execute sequentially all the instructions stored in RAM.
    Execute(base_hex).execute_program()

    # View the RAM and Registers 

    print("Final RAM state:", ram.storage)
    print("Final registers:", registers.values)


if __name__ == "__main__":
    main()