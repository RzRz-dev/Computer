from RAM.dataRam import ram

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
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Convert binary string to hex, preserving full length
                num_hex_chars = len(line) // 4
                value = format(int(line, 2), f'0{num_hex_chars}X')
                
                # Store at current offset
                address = format(self.offset, '016X')
                self.data_ram.write(address, value)
                self.offset += 1


loader = Loader(ram)