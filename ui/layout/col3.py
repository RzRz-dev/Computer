import flet as ft

def col3():
    return ft.Container(
        width=200,
        bgcolor="#37474F",
        content=ft.Column([
            ft.Text("Menu",size=20),
            ft.TextButton("Dashboard"),
            ft.TextButton("Analitics"),
        ]),
        expand=1
    )