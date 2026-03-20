from RAM.dataRam import ram
from CPU.registers import RegisterBank
class Load:

    def loader(opcode, register, value):
        register = RegisterBank.values
        match opcode:
            case "11":
                print("From load.py \n", "Register: ", register, "\n Value: ", value)
                
                ram.read(value)
            case "12":
                print("From load.py \n", "Register: ", register, "\n Value: ", value)
            case "13":
                print("From load.py \n", "Register: ", register, "\n Value: ", value)
            case "16":
                print("From load.py \n", "Register: ", register, "\n Value: ", value)
                