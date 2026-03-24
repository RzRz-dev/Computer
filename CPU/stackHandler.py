from RAM.dataRam import ram
from CPU.registers import registers

class Stack:

    def readStackInstruction(midcode, register):
        match midcode:
            case "1":  # PUSH
                sp = format(registers.stack_pointer, '016X')
                ram.write(sp, registers.values[register])
                registers.stack_pointer -= 1

            case "2":  # POP
                registers.stack_pointer += 1
                sp = format(registers.stack_pointer, '016X')
                registers.values[register] = ram.read(sp)