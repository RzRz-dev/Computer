from Disco.Compilador.Assembler import assemble_program, opcodes


def test_assemble_program_returns_relocatable_text():
    program = """inicio: NOP
JMP inicio
"""

    result = assemble_program(program)

    assert result.splitlines() == [
        format(opcodes["NOP"], "064b"),
        format(opcodes["JMP"], "012b") + "(0)",
    ]