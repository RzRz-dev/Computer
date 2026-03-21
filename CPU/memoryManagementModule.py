from RAM.dataRam import ram
from CPU.registers import registers
class Load:

    def loader(opcode, register, value):

        match opcode:
            #LOAD Instruction
            case "11":
                registers.values[register] = ram.read(value)
                print("Load memory address ", value," in register ", register)

            #LOADV Instruction
            case "12":
                registers.values[register] = value
                print("Load value: ", value, "into register ", register)

            #STORE
            case "13":
                ram.write(value, registers.values[register])
                print("Store value of register ",register," in memory address ",value)

            #LEA
            case "16":
                registers.values[register] = ram.read(value)
                print("Load effective memory address ", value," in register ", register)