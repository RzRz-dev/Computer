

from RAM.data_ram import data_ram
from Utilities.loader import Loader
from Utilities.execute import Execute

def main():

    # Define the base in Hex
    base_hex = int("0F", 16)  # This is 15

    #Loader, makes the space in ram for the load of data
    loader = Loader(data_ram, base_hex)
    # This loads the program into the ram
    loader.load_program("program.txt")

    # Execute sequentially all the instructions stored in RAM.
    Execute(base_hex).execute_program()

    # View the RAM 
    print("Final RAM state:", data_ram.storage)


if __name__ == "__main__":
    main()
