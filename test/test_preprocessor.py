from Disco.Compilador.Preprocessor import preprocess_program


def test_preprocess_program_resolves_define_and_include(tmp_path):
    lib_dir = tmp_path / "Lib"
    lib_dir.mkdir()
    (lib_dir / "common.asm").write_text("LOAD R2, VALUE\n", encoding="utf-8")

    program = 'DEFINE VALUE 7\nINCLUDE "common"\nLOAD R1, VALUE\n'

    result = preprocess_program(program, current_dir=str(tmp_path), lib_dir=str(lib_dir))

    assert result.splitlines() == [
        "LOAD R2 , 7",
        "LOAD R1 , 7",
    ]


def test_preprocess_program_does_not_leak_macros_between_calls():
    first = preprocess_program("DEFINE VALUE 9\nLOAD R1, VALUE\n")
    second = preprocess_program("LOAD R1, VALUE\n")

    assert first.splitlines() == ["LOAD R1 , 9"]
    assert second.splitlines() == ["LOAD R1 , VALUE"]
