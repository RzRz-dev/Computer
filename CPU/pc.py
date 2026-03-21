class ProgramCounter:
    _instance = None  # class-level attribute
    
    def __new__(cls, next_instruction=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.address = int(next_instruction)
            cls._instance.MASK = (1 << 64) - 1  # 64-bit mask
        return cls._instance
    
    def get_next_instruction(self):
        # Format to hex string only when outputting
        return format(self.address, '016x').upper()

    def set_next_instruction(self, next_address=None):
        if next_address is not None:
            if isinstance(next_address, str):
                self.address = int(next_address, 16)
            else:
                self.address = int(next_address)
        else:
            self.address = (self.address + 1) & self.MASK
            
# Usage
pc = ProgramCounter()
