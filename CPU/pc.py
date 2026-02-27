class ProgramCounter:
    _instance = None  # class-level attribute

    def __new__(cls, next_instruction=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.address = int(next_instruction)
        return cls._instance
    
    def get_next_instruction(self):
        # Format to hex string only when outputting
        return format(self.address, '016x').upper()

    def set_next_instruction(self, current_address=None):
        if current_address is not None:
            # Handle if the input is a hex string or an int
            if isinstance(current_address, str):
                self.address = int(current_address, 16)-1
            else:
                self.address = int(current_address)-1
        else:
            self.advance()
            
        print("From PC next instruction is: ", self.get_next_instruction())

    def advance(self):
        # Directly increment the integer address by 1
        self.address += 1
        return self.get_next_instruction()

# Usage
pc = ProgramCounter()
