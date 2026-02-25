from RAM.data_ram import data_ram

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
            current_addr_int = self.offset
            
            for line in file:
                line = line.strip()
                if not line: continue

                # Value logic
                if '(' in line:
                    prefix, target = line.split('(')
                    target_line = int(target.replace(')', ''))
                    abs_target = target_line + self.offset
                    full_bin = (prefix + format(abs_target, '052b')).ljust(64, '0')[:64]
                    hex_val = format(int(full_bin, 2), '016X')
                else:
                    hex_val = format(int(line.ljust(64, '0')[:64], 2), '016X')

                # --- THE KEYS (ADDRESSES) ---
                # Force the key to be exactly 16 characters long, padded with 0
                hex_key = format(current_addr_int, '016X')
                
                self.data_ram.write(hex_key, hex_val)
                current_addr_int += 1
            
            self.offset = current_addr_int


loader = Loader(data_ram)