import flet as ft
from ..components.code_block import CodeBlock
from ..components.button_panel import ButtonPanel
from ..styles.styles import AppStyles

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
                "func": lambda e: print("Compile")
            },
            "Limpiar": {
                "icon": ft.Icons.CLEANING_SERVICES,
                "func": lambda e: print("Clean")
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