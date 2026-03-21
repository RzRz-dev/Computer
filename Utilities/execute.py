from CPU.decoder import Decoder
from RAM.dataRam import ram
from CPU.pc import ProgramCounter
from Utilities.fetch import Fetch
from CPU.registers import registers
from CPU.flags import flags

class Execute:
    def __init__(self, current_instruction=0):
        self.ram = ram
        self.decoder = Decoder()
        self.fetcher = Fetch()
        self.program_counter = ProgramCounter(current_instruction)
        self.program_counter.set_next_instruction(current_instruction)

    def execute_program(self):
        auto_mode = False
        print("========= Starting Program Execution =========")
        print("Tip: Press 'Enter' to step, or type 'auto' for continuous execution.")

        while True:
            current_addr = self.program_counter.get_next_instruction()
            print(f"\nAddress: {current_addr}")

            if current_addr not in self.ram.storage:
                print("End of program reached.")
                break

            self.program_counter.set_next_instruction()

            instruction = self.fetcher.fetch_instruction(current_addr)
            Decoder.decode(instruction)

            print(f"Registers: {registers.values}")
            print(f"Flags: {flags}")

            if not auto_mode:
                user_input = input("Press Enter to step (or type 'auto'): ").strip().lower()
                if user_input == "auto":
                    auto_mode = True

        print("========= Program Execution Finished =========")