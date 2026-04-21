import flet as ft
from interfaz import *

def main(page: ft.Page):
    page.title        = "Practica 3. Teoria de la Computacion"
    page.bgcolor      = BG
    page.padding      = 0
    page.fonts        = {}
    page.theme = ft.Theme(color_scheme_seed=NEON)

    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    width=12, height=12,
                    bgcolor=NEON,
                    border_radius=6,
                    shadow=ft.BoxShadow(blur_radius=12, color=NEON),
                ),
                ft.Text("TEORÍA FORMAL DE LENGUAJES", size=17,
                        weight="w800", color=WHITE,
                        font_family="monospace"),
                ft.Container(expand=True),
                ft.Text("AUTÓMATAS · CADENAS · CERRADURAS",
                        size=10, color=NEON, font_family="monospace"),
            ],
            vertical_alignment="center",
            spacing=14,
        ),
        bgcolor=BG,
        border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER)),
        padding=ft.padding.symmetric(horizontal=36, vertical=22),
    )

    # Tabs
    tab_sub = build_tab_subcadenas(page)
    tab_kle = build_tab_kleene(page)
    tab_aut = build_tab_automatas(page)

    content_container = ft.Container(
        content=tab_sub,
        padding=ft.padding.symmetric(horizontal=36, vertical=32),
        expand=True,
    )

    def switch_tab(idx: int):
        for i, btn in enumerate(tab_row.controls):
            btn.style = ft.ButtonStyle(
                color=NEON if i == idx else TEXT_DIM,
                bgcolor="transparent",
                text_style=ft.TextStyle(font_family="monospace", size=11),
                shape=ft.RoundedRectangleBorder(radius=0),
            )
        if idx == 0:
            content_container.content = tab_sub
        elif idx == 1:
            content_container.content = tab_kle
        else:
            content_container.content = tab_aut
        page.update()

    btn0 = ft.TextButton(
        "SUBCADENAS / PREFIJOS / SUFIJOS",
        on_click=lambda e: switch_tab(0),
        style=ft.ButtonStyle(
            color=NEON,
            text_style=ft.TextStyle(font_family="monospace", size=11),
            shape=ft.RoundedRectangleBorder(radius=0),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )
    btn1 = ft.TextButton(
        "CERRADURA KLEENE / POSITIVA",
        on_click=lambda e: switch_tab(1),
        style=ft.ButtonStyle(
            color=TEXT_DIM,
            text_style=ft.TextStyle(font_family="monospace", size=11),
            shape=ft.RoundedRectangleBorder(radius=0),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )

    btn2 = ft.TextButton(
        "AUTÓMATAS Y MINIMIZACIÓN",
        on_click=lambda e: switch_tab(2),
        style=ft.ButtonStyle(
            color=TEXT_DIM,
            text_style=ft.TextStyle(font_family="monospace", size=11),
            shape=ft.RoundedRectangleBorder(radius=0),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
        ),
    )

    tab_row = ft.Row([btn0, btn1, btn2], spacing=0)

    tab_bar = ft.Container(
        content=tab_row,
        border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER)),
        padding=ft.padding.only(left=24),
    )

    page.add(
        ft.Column(
            [
                header,
                tab_bar,
                content_container,
            ],
            spacing=0,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)