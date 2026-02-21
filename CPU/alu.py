
class ALU:
    from CPU.flags import Flags
    
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(ALU, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass
    
    def add(self, a, b):
        flags = self.Flags()
        print(id(flags))
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

alu = ALU()