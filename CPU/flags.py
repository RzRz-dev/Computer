class Flags:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(Flags, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.ZF = 0  # Zero Flag
        self.NF = 0  # Negative Flag
        self.CF = 0  # Carry Flag
        self.OF = 0  # Overflow Flag
        self.IF = 0  # Interrupt Enable Flag

    def __str__(self):
        return f"CF: {self.CF}, NF: {self.NF}, ZF: {self.ZF}, OF: {self.OF}, IF: {self.IF}"
    
flags = Flags()