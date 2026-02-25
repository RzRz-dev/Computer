from CPU.decoder import Decoder
from RAM.data_ram import data_ram
from CPU.pc import ProgramCounter
from Utilities.fetch import Fetch
from CPU.registers import registers
from CPU.flags import flags

class Execute:
    def __init__(self, current_instruction=0):
        #Initialize the execute class
        #To access the data_ram, decoder, and program counter, we will need to initialize them in the constructor of the execute class.
        self.data_ram = data_ram
        self.decoder = Decoder()
        self.program_counter = ProgramCounter(current_instruction)
        self.program_counter.set_next_instruction(current_instruction)

    #This is a function that will execute the program
    def execute_program(self):
        fetcher = Fetch()
        
        print("========= Starting Program Execution =========")
        while True:
            print("Address: ",self.program_counter.get_next_instruction())
            if self.program_counter.get_next_instruction() not in data_ram.storage:
                print("End of program reached.")
                break
            
            instruction = fetcher.fetch_instruction(self.program_counter.get_next_instruction())
            Decoder().decode(instruction)
            
            self.program_counter.set_next_instruction()
            input()
            print(registers.values)
            print(str(flags))
        print("========= Program Execution Finished =========")
            
