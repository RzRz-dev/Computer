class ProgramCounter:

    def __init__(self, value=0):
        self.value = value

    def increment(self):
        self.value += 1

    def set_next(self, value):
        self.value = value

    def get_next(self):
        return self.value
    
program_counter = ProgramCounter()