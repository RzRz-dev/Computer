class CurrentInstructionRegister:
    _instance = None
    def __new__(cls, instruction=None):
        cls.instruction = instruction
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(CurrentInstructionRegister, cls).__new__(cls)
        return cls._instance


    def __init__(self, instruction=None):
        self.instruction = instruction

    def current_instruction(self):
        return self.instruction
    
    def receive_instruction(self, instruction):
        self.instruction = instruction