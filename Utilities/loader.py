from RAM.dataRam import data_ram

class Loader:
    _instance = None
    
    def __new__(cls, data_ram, base_hex="0"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.data_ram = data_ram
            # Convert the incoming base (e.g., "14") to int for math
            cls.offset = int(base_hex, 16)
        return cls._instance

    def __init__(self, data_ram, base_hex="0"):
        # Ensure offset is an int for calculation logic
        if isinstance(base_hex, str):
            self.offset = int(base_hex, 16)
        else:
            self.offset = base_hex
    
    def load_program(self, file_path):
        with open(file_path, "r") as file:
            pass


loader = Loader(data_ram)