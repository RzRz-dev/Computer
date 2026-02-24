class DataRAM:
    #This piece of code makes the object singleton.
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            # If it doesn't exist yet, create it
            cls._instance = super(DataRAM, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.storage = {}
    
    def read(self, address):
        return self.storage.get(address, 0)  
    
    def write(self, address, value):
        self.storage[address] = value

        

data_ram = DataRAM()