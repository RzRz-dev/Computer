from RAM.data_ram import data_ram


class Fetch:
    def __init__(self, ):
        self.data_ram = data_ram
        

    def fetch_instruction(self, address):
        instruction = data_ram.read(address)
        instruction_hex = hex(int(instruction, 2))[2:].upper()
        return instruction_hex

    