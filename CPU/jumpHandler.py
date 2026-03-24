from CPU.pc import pc
from CPU.flags import Flags
from RAM.dataRam import ram
from CPU.registers import registers

class Jump:

    def readJumpInstruction(midcode, address):
        match midcode:
            case "0": pc.set_next_instruction(address)           # JMP
            case "1":                                             # JZ
                if Flags.ZF == 1: pc.set_next_instruction(address)
            case "2":                                             # JNZ
                if Flags.ZF == 0: pc.set_next_instruction(address)
            case "3":                                             # JNN
                if Flags.NF == 0: pc.set_next_instruction(address)
            case "4":                                             # JN
                if Flags.NF == 1: pc.set_next_instruction(address)
            case "5":                                             # JC
                if Flags.CF == 1: pc.set_next_instruction(address)
            case "6":                                             # JNC
                if Flags.CF == 0: pc.set_next_instruction(address)
            case "7":                                             # JOF
                if Flags.OF == 1: pc.set_next_instruction(address)
            case "8":                                             # JNOF
                if Flags.OF == 0: pc.set_next_instruction(address)
            case "9":                                             # CALL
                # Push return address (current PC, already advanced) onto stack
                return_addr = format(pc.address, '016X')
                sp = format(registers.stack_pointer, '016X')
                ram.write(sp, return_addr)
                registers.stack_pointer -= 1
                # Jump to target
                pc.set_next_instruction(address)
            case "A":                                             # RET
                # Pop return address from stack
                registers.stack_pointer += 1
                sp = format(registers.stack_pointer, '016X')
                return_addr = ram.read(sp)
                pc.set_next_instruction(return_addr)
            case "9":
                pass