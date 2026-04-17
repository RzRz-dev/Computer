import os

import flet as ft
from ..components.code_block import CodeBlock
from ..components.button_panel import ButtonPanel
from ..styles.styles import AppStyles
from Disco.Compilador.Assembler import assemble_program
from Disco.Compilador.Preprocessor import preprocess_program

class FirstColumn():
    def __init__(self, page: ft.Page, relocatable_code_block):
        self.page = page
        self.relocatable_code_block = relocatable_code_block
        self._create_components()
        self._build_column()

    def _create_components(self):
        self.high_level_code = CodeBlock(title="Código de alto nivel")
        self.assembly_code = CodeBlock(title="Código Assembly")
        
        high_level_btns = {
            "Abrir": {
                "icon": ft.Icons.UPLOAD_FILE,
                "func": self._pick_text_file
            },
            "Preprocesar": {
                "icon": ft.Icons.AUTO_FIX_HIGH,
                "func": self._preprocess_high_level_code
            },
            "Compilar": {
                "icon": ft.Icons.BUILD,
                "func": self._compile
            },
            "Limpiar": {
                "icon": ft.Icons.CLEANING_SERVICES,
                "func": self._clear_file_picker
            }
        }

        assembly_btns = {
            "Ensamblar": {
                "icon": ft.Icons.BUILD,
                "func": self._assemble
            },
            "Limpiar": {
                "icon": ft.Icons.CLEANING_SERVICES,
                "func": self._clear_assembly
            }
        }

        self.high_level_panel_btns = ButtonPanel(high_level_btns)
        self.assembly_code_panel_btns = ButtonPanel(assembly_btns)
        self.selected_file = ft.Text(style=AppStyles.file_text())

    def _build_column(self):
        self.first_column = ft.Container(
            **AppStyles.container(),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    self.high_level_code.code_block_comp,
                    self.selected_file,
                    self.high_level_panel_btns.button_panel_comp,
                    self.assembly_code.code_block_comp,
                    self.assembly_code_panel_btns.button_panel_comp
                ]
            ),
            expand=True
        )

    async def _pick_text_file(self, _: ft.Event[ft.Button]):
        self.files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )

        if not self.files:
            self.selected_file.value = "Carga cancelada"
            self.selected_file.color = "#F44336"
            self.high_level_code.code_editor.value = ""
            self.page.update()
            return

        selected = self.files[0]
        self.selected_file.value = f"Archivo cargado: {selected.name} ({selected.size} bytes)"
        self.selected_file.color = "#4CAF50"
        self.high_level_code.code_editor.value = (
            selected.bytes.decode("utf-8", errors="replace") if selected.bytes else ""
        )
        self.page.update()
            
    def _clear_file_picker(self):
        self.files = None
        self.selected_file.value = ""
        self.high_level_code.code_editor.value = ""
        self.page.update()

    def _compile(self):
        self.relocatable_code_block.code_editor.value = self.high_level_code.code_editor.value
        self.page.update()

    def _preprocess_high_level_code(self, _=None):
        program = (self.high_level_code.code_editor.value or "").strip()

        if not program:
            self.assembly_code.code_editor.value = ""
            self.page.update()
            return

        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            preprocessed_program = preprocess_program(program, current_dir=project_root)
        except Exception as exc:
            self.assembly_code.code_editor.value = ""
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al preprocesar: {exc}"), bgcolor=ft.Colors.RED_400)
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.assembly_code.code_editor.value = preprocessed_program
        self.page.update()

    def _assemble(self, _=None):
        assembly_code = (self.assembly_code.code_editor.value or "").strip()

        if not assembly_code:
            self.relocatable_code_block.code_editor.value = ""
            self.page.update()
            return

        try:
            relocatable_code = assemble_program(assembly_code)
        except Exception as exc:
            self.relocatable_code_block.code_editor.value = ""
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al ensamblar: {exc}"), bgcolor=ft.Colors.RED_400)
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.relocatable_code_block.code_editor.value = relocatable_code
        self.page.update()

    def _clear_assembly(self, _=None):
        self.assembly_code.code_editor.value = ""
        self.relocatable_code_block.code_editor.value = ""
        self.page.update()