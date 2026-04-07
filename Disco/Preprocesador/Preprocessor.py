import os
import re
import sys

INCLUDE_RE = re.compile(r'^\s*INCLUDE\s+["\']?([^"\']+)["\']?\s*(?:;.*)?$', re.IGNORECASE)


def resolve_include_path(include_name, current_dir, lib_dir):
    if not include_name.lower().endswith('.asm'):
        include_name = include_name + '.asm'

    candidate_paths = [
        os.path.join(current_dir, include_name),
        os.path.join(lib_dir, include_name) if lib_dir else None,
    ]

    for candidate in candidate_paths:
        if candidate and os.path.isfile(candidate):
            return os.path.abspath(candidate)

    raise FileNotFoundError(
        f"No se encontró el archivo incluido '{include_name}'. "
        f"Buscando en '{current_dir}' y '{lib_dir}'."
    )


def preprocess_file(input_path, lib_dir=None, included_files=None):
    """Preprocesa un archivo ASM y expande las directivas INCLUDE."""
    input_path = os.path.abspath(input_path)

    if included_files is None:
        included_files = set()

    if input_path in included_files:
        raise ValueError(f"Ciclo de inclusión detectado: {input_path}")

    included_files.add(input_path)

    if lib_dir is None:
        lib_dir = os.path.join(os.path.dirname(input_path), 'Lib')

    output_lines = []
    current_dir = os.path.dirname(input_path)

    with open(input_path, 'r', encoding='utf-8') as infile:
        for raw_line in infile:
            line = raw_line.rstrip('\n')
            match = INCLUDE_RE.match(line)
            if match:
                include_name = match.group(1).strip()
                include_path = resolve_include_path(include_name, current_dir, lib_dir)
                included_lines = preprocess_file(include_path, lib_dir=lib_dir, included_files=included_files)
                output_lines.extend(included_lines)
            else:
                output_lines.append(line)

    included_files.remove(input_path)
    return output_lines


def write_preprocessed_file(input_path, output_path=None, lib_dir=None):
    lines = preprocess_file(input_path, lib_dir=lib_dir)

    if output_path is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(os.path.dirname(input_path), f'{base_name}.preprocessed.asm')

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in lines:
            outfile.write(line + '\n')

    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Uso: python Preprocessor.py <archivo_entrada> [<archivo_salida>]')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2] if len(sys.argv) == 3 else None

    try:
        salida = write_preprocessed_file(source_file, output_path=target_file)
        print(f'Archivo preprocesado guardado en: {salida}')
    except Exception as exc:
        print(f'Error: {exc}')
        sys.exit(1)
