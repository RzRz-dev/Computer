from CPU.pc import pc
from CPU.flags import Flags
class Jump:
    
    def readJumpInstruction(midcode, address):
        match midcode:
            case "0": #JUMP
                pc.set_next_instruction(address)
            case "1": #JZ
                if Flags.ZF == 1:
                    pc.set_next_instruction(address)
            case "2": #JNZ
                if Flags.ZF == 0:
                    pc.set_next_instruction(address)
            case "3":
                if Flags.NF == 0:
                    pc.set_next_instruction(address)
            case "4":
                if Flags.NF == 1:
                    pc.set_next_instruction(address)
            case "5":
                if Flags.CF == 1:
                    pc.set_next_instruction(address)
            case "6":
                if Flags.CF == 0:
                    pc.set_next_instruction(address)
            case "7":
                if Flags.OF == 1:
                    pc.set_next_instruction(address)
            case "8":
                if Flags.OF == 0:
                    pc.set_next_instruction(address)
            case "9":
                pass