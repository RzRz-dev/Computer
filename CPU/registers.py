class RegisterBank:
    _instance = None

    def __new__(cls):

        cls.values = {
            '0000': 0,
            '0001': 0,
            '0010': 0,
            '0011': 0,
            '0100': 0,
            '0101': 0,
            '0110': 0,
            '0111': 0,
            '1000': 0,
            '1001': 0,
            '1010': 0,
            '1011': 0,
            '1100': 0,
            '1101': 0,
            '1110': 0,
            '1111': 0
        } 

        cls.stack_pointer = 0

        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(RegisterBank, cls).__new__(cls)
        return cls._instance

registers = RegisterBank()