from CPU.decoder import Decoder
from RAM.data_ram import data_ram
from CPU.pc import ProgramCounter
from Utilities.fetch import Fetch
from CPU.registers import registers
from CPU.flags import flags

class Execute:
    def __init__(self, current_instruction=0):
        self.data_ram = data_ram
        self.decoder = Decoder()
        self.program_counter = ProgramCounter(current_instruction)
        self.program_counter.set_next_instruction(current_instruction)

    def execute_program(self):
        fetcher = Fetch()
        # Track whether we are in manual step-through or automatic mode
        auto_mode = False
        
        print("========= Starting Program Execution =========")
        print("Tip: Press 'Enter' to step, or type 'auto' for continuous execution.")
        
        while True:
            current_addr = self.program_counter.get_next_instruction()
            print("Address: ", current_addr)
            
            if current_addr not in data_ram.storage:
                print("End of program reached.")
                break
            
            # Fetch and Decode
            instruction = fetcher.fetch_instruction(current_addr)
            self.decoder.decode(instruction)
            
            # Update PC
            self.program_counter.set_next_instruction()
            
            # Handle user input / Pause logic
            if not auto_mode:
                user_input = input("Press Enter to step (or type 'auto'): ").strip().lower()
                if user_input == "auto":
                    auto_mode = True

            print(registers.values)
            print(str(flags))
            
        print("========= Program Execution Finished =========")