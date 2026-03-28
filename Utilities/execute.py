from CPU.decoder import Decoder
from RAM.dataRam import ram
from CPU.pc import ProgramCounter
from Utilities.fetch import Fetch
from CPU.registers import registers
from CPU.flags import flags

STACK_BASE = 0xFFFF

class Execute:
    def __init__(self, current_instruction=0):
        self.ram = ram
        self.decoder = Decoder()
        self.fetcher = Fetch()
        self.program_counter = ProgramCounter(current_instruction)
        self.program_counter.set_next_instruction(current_instruction)
        self.auto_mode = False
        self._init_stack()

    def _init_stack(self):
        registers.stack_pointer = STACK_BASE
        ram.write(format(STACK_BASE, '016X'), 'DEADBEEFDEADBEEF')
        print(f"Stack initialized at 0x{STACK_BASE:04X}")

    def execute_program(self):
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

            if not self.auto_mode:
                user_input = input("Press Enter to step: ").strip().lower()
    
        self._print_final_state()
        print("========= Program Execution Finished =========")

    def _print_final_state(self):
        print("\n========= Final State =========")

        print("\n--- Registers ---")
        for reg, val in registers.values.items():
            print(f"  R{reg} = {val}  (dec: {int(val, 16)})")

        print(f"\n  SP = {format(registers.stack_pointer, '016X')}")
        print(f"  PC = {self.program_counter.get_next_instruction()}")
        print(f"\n--- Flags ---")
        print(f"  {flags}")

        print("\n--- RAM ---")
        for addr in sorted(ram.storage.keys()):
            # Skip stack sentinel to avoid noise
            if int(addr, 16) == STACK_BASE:
                continue
            print(f"  [{addr}] = {ram.storage[addr]}")

    def set_current_isntruction(self, current_instruction):
        self.program_counter = ProgramCounter(current_instruction)
        self.program_counter.set_next_instruction(current_instruction)

    def set_auto_mode_value(self, value):
        self.auto_mode = value