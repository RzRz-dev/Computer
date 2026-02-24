

from RAM.data_ram import data_ram
from Utilities.loader import Loader
from Utilities.execute import Execute

def main():
    # Define the base in Hex
    base_hex = int("0F", 16)  # This is 20 in decimal

    # Loader handles the hex conversion internally now
    loader = Loader(data_ram, base_hex)
    loader.load_program("program.txt")
    loader.load_program("program1.txt")


    # Execute also takes the hex base
    Execute(base_hex).execute_program()

    # View the RAM (keys will be integers for easy math)
    print("Final RAM state:", data_ram.storage)


if __name__ == "__main__":
    main()
