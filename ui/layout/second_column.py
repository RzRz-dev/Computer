import flet as ft
from ..styles.styles import AppStyles
from ..components.code_block import CodeBlock
from ..components.ram_block import RamBlock
from ..components.mod_ram_block import ModRamBlock
from ..components.base_address_block import BaseAddressBlock
from ..components.button_panel import ButtonPanel
from RAM.dataRam import ram
from Utilities.execute import Execute
from Disco.Compilador.link_loader import LinkLoader
from CPU.registers import registers
from CPU.pc import pc
from CPU.flags import flags

class SecondColumn:
    def __init__(self, page: ft.Page):
        self.base_address = "0"
        self.page = page
        self.execute = Execute()
        self._create_components()
        self._build_column()
        self.band = False

    def _create_components(self):
        link_load_btn = {
            "Enlazar-Cargar": {
                "icon": ft.Icons.CATCHING_POKEMON,
                "func": self._load_link_code
            }
        }

        execute_btns={
            "Ejecutar RAM": {
                "icon": ft.Icons.PLAY_ARROW,
                "func": self._auto_execution
            },
            "Ejecutar paso a paso": {
                "icon": ft.Icons.HOURGLASS_BOTTOM_OUTLINED,
                "func": self._step_execution
            },
            "Detener ejecución":{
                "icon": ft.Icons.BACK_HAND
            },
            "Reestablecer máquina": {
                "icon": ft.Icons.REFRESH,
                "func": self._reset_machine
            }
        }

        self.relocatable_code = CodeBlock("Código relocalizable", lines=15)
        self.ram_block = RamBlock(on_execute=self._auto_execution)
        self.mod_ram_block = ModRamBlock(on_modify=self._mod_ram_write)
        self.base_address_block = BaseAddressBlock()
        self.entry_point_field = ft.TextField(
            label="Entrada (HEX)",
            hint_text="Ej: 0F",
            capitalization=ft.TextCapitalization.CHARACTERS,
            width=190,
            value=self.base_address,
        )
        self.execution_state = ft.TextField(
            label="Estado de registros y banderas",
            multiline=True,
            read_only=True,
            min_lines=8,
            max_lines=12,
            expand=True,
            value="Aún no se ha ejecutado ningún programa.",
        )
        self.link_load_btn = ButtonPanel(link_load_btn)
        self.execute_btns = ButtonPanel(execute_btns)

    def _build_column(self):
        self.second_column = ft.Container(
            **AppStyles.container(),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                self.relocatable_code.code_block_comp,
                ft.Row(
                    controls=[
                        self.base_address_block.base_address_block,
                        self.link_load_btn.button_panel_comp
                    ]
                ),
                self.ram_block.ram_block_comp,
                self.mod_ram_block.mod_ram_block_comp,
                self.entry_point_field,
                ft.Container(
                    **AppStyles.list_view(),
                    padding=10,
                    content=self.execution_state,
                ),
                self.execute_btns.button_panel_comp
            ]),
            expand=2
        )

    def _load_link_code(self, _=None):
        base_hex = (self.base_address_block.base_address.value or "0").strip()
        try:
            base_address = int(base_hex, 16)
        except ValueError:
            self._show_message("La dirección base debe ser HEX válida", ft.Colors.RED_400)
            return

        code = (self.relocatable_code.code_editor.value or "").strip()
        if not code:
            self._show_message("No hay código relocalizable para enlazar", ft.Colors.RED_400)
            return

        try:
            loader = LinkLoader(base_address=base_address, memory=ram)
            entry_point = loader.link_load(code)
        except Exception as exc:
            self._show_message(f"Error al enlazar/cargar: {exc}", ft.Colors.RED_400)
            return

        self.base_address = format(entry_point, "X")
        self.entry_point_field.value = self.base_address
        self.base_address_block.base_address.value = self.base_address
        self.ram_block.refresh()
        self.page.update()
        self._show_message(f"Programa cargado. Entry point: 0x{self.base_address}", ft.Colors.GREEN_400)

    def _init_execution(self, _=None):
        global entry_hex
        entry_hex = (self.entry_point_field.value or self.base_address or "0").strip()
        try:
            entry_point = int(entry_hex, 16)
        except ValueError:
            self._show_message("La dirección de entrada debe ser HEX válida", ft.Colors.RED_400)
            return
        self.band = True
        self.execute = Execute(entry_point)
        
    def _auto_execution(self, _=None):
        
        self._init_execution()
        
        self.execute.set_auto_mode_value(True)
        self.execute.execute_program_auto()
        self.execution_state.value = self.execute.get_final_state_text()
        self.ram_block.refresh()
        self.page.update()
        self.band = False
        self._show_message(f"Ejecución finalizada desde 0x{entry_hex.upper()}", ft.Colors.GREEN_400)

    def _step_execution(self, _=None):
        
        if self.band == False:
            self._init_execution()
        if self.execute.exceute_step() == 1:
            band = False
            pass
        self.execution_state.value = self.execute.get_final_state_text()
        self.ram_block.refresh()
        self.page.update()

    def _mod_ram_write(self, _=None):
        address_hex = self.mod_ram_block.address_field.value
        word_hex = self.mod_ram_block.word_content.value
        success, message = self.ram_block.write_direct(address_hex, word_hex)

        if not success:
            self._show_message(message, ft.Colors.RED_400)
            return

        self.ram_block.refresh()
        self.page.update()
        self._show_message(message, ft.Colors.GREEN_400)

    def _reset_machine(self, _=None):
        """Reset the entire machine to its initial state"""
        # Reset CPU components
        registers.reset()
        ram.reset()
        pc.reset()
        flags.reset()
        
        # Reset UI state
        self.base_address = "0"
        self.band = False
        self.execute = Execute()
        
        # Reset UI fields
        self.entry_point_field.value = self.base_address
        self.base_address_block.base_address.value = self.base_address
        self.execution_state.value = "Aún no se ha ejecutado ningún programa."
        self.relocatable_code.code_editor.value = ""
        self.mod_ram_block.address_field.value = ""
        self.mod_ram_block.word_content.value = ""
        
        # Refresh components
        self.ram_block.refresh()
        self.page.update()
        
        self._show_message("Máquina reestablecida a estado inicial", ft.Colors.BLUE_400)

    def _show_message(self, message: str, color: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()