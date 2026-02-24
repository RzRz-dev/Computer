class ProgramCounter:
    _instance = None  # class-level attribute
    
    def __new__(cls, next_instruction=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.next_instruction_address = next_instruction
        return cls._instance
    
    def get_next_instruction(cls):
        return cls.next_instruction_address

    def set_next_instruction(cls, current_address=None):
        if current_address is not None:
            cls.next_instruction_address = current_address
        else:
            cls.next_instruction_address = cls.advance()
        print("From PC next instruction is: ", cls.next_instruction_address)

    def advance(cls):
        cls.next_instruction_address += 1
        return cls.next_instruction_address

pc = ProgramCounter()