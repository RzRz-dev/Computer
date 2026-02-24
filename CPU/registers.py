class RegisterBank:
    #This piece of code makes the object singleton.
    _instance = None
    def __new__(cls):

        cls.values = {
            '0': 0,
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
            'A': 0,
            'B': 0,
            'C': 0,
            'D': 0,
            'E': 0,
            'F': 0
        } 

        cls.stack_pointer = 0

        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(RegisterBank, cls).__new__(cls)
        return cls._instance

registers = RegisterBank()