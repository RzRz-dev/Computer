import flet as ft
from ..styles.styles import AppStyles
from ..components.code_block import CodeBlock
from ..components.ram_block import RamBlock
from ..components.mod_ram_block import ModRamBlock
from ..components.base_address_block import BaseAddressBlock
from ..components.button_panel import ButtonPanel
from RAM.dataRam import ram
from Utilities.execute import Execute
from Utilities.loader import loader

class SecondColumn:
    def __init__(self, page: ft.Page):
        self.base_address = "0"
        self.page = page
        self.execute = Execute()
        self._create_components()
        self._build_column()

    def _create_components(self):
        link_load_btn = {
            "Enlazar-Cargar": {
                "icon": ft.Icons.CATCHING_POKEMON,
                "func": self._load_link_code
            }
        }

        execute_btns={
            "Ejecutar": {
                "icon": ft.Icons.PLAY_ARROW,
                "func": self._auto_execution
            },
            "Ejecutar paso a paso": {
                "icon": ft.Icons.HOURGLASS_BOTTOM_OUTLINED,
                "func": self._step_execution
            },
            "Detener ejecución":{
                "icon": ft.Icons.BACK_HAND
            }
        }

        self.relocatable_code = CodeBlock("Código relocalizable", lines=15)
        self.ram_block = RamBlock()
        self.mod_ram_block = ModRamBlock()
        self.base_address_block = BaseAddressBlock()
        self.link_load_btn = ButtonPanel(link_load_btn)
        self.execute_btns = ButtonPanel(execute_btns)

    def _build_column(self):
        self.second_column = ft.Container(
            **AppStyles.container(),
            content=ft.Column(
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
                self.execute_btns.button_panel_comp
            ]),
            expand=2
        )

    def _load_link_code(self):
        self.base_address = self.base_address_block.base_address.value or "0"
        loader.set_base_hex(self.base_address)
        loader.load_program2(self.relocatable_code.code_editor.value)
        self.ram_block.ram_list.controls.clear()
        self.ram_block.ram_list.controls.extend([ft.Text(f" [{k}] → {v}", style=AppStyles.list_text()) for k, v in ram.storage.items()])
        self.page.update()

    def _auto_execution(self):
        self.execute.set_auto_mode_value(True)
        self.execute.set_current_isntruction(self.base_address)
        self.execute.execute_program()

    def _step_execution(self):
        self.execute.set_auto_mode_value(False)
        self.execute.set_current_isntruction(self.base_address)
        self.execute.execute_program()