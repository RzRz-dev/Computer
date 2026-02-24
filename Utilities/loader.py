from RAM.data_ram import data_ram

class Loader:
    #This loader module will only be responsible for loading the program into the RAM
    _instance = None
    def __new__(cls, data_ram, offset=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.data_ram = data_ram
            cls.offset = offset
        return cls._instance
    

    def __init__(self, data_ram, base_hex="0"):
        self.data_ram = data_ram
        # Convert hex string to integer for dictionary keys
        self.offset = base_hex
        
    
    def load_program(self, file_path):
        with open(file_path, "r") as file:
            address = self.offset
            
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if '(' in line:
                    # Example: "00101...(1)"
                    binary_prefix, target_val = line.split('(')
                    target_line = int(target_val.replace(')', ''))
                    
                    # 1. Calculate Absolute Address: Target + Base
                    absolute_addr = target_line + self.offset
                    
                    # 2. Convert Absolute Address to 52-bit binary string
                    address_bits = format(absolute_addr, '052b')
                    
                    # 3. Combine with prefix and ensure 64-bit length
                    full_instruction = (binary_prefix + address_bits).ljust(64, '0')[:64]
                    
                    self.data_ram.write(address, full_instruction)
                else:
                    # Pure binary lines are stored as-is
                    self.data_ram.write(address, line)
                
                address += 1
            
            # Update offset so the next load doesn't overwrite
            self.offset = address     
        

loader = Loader(data_ram)