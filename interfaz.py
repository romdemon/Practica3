import flet as ft # interfaz.py
from logica import get_substrings, get_prefixes, get_suffixes, kleene_star, kleene_plus, export_to_file, Automata
from itertools import product as iproduct
import os

BG        = "#0a0a0f"
CARD      = "#12121a"
BORDER    = "#1e1e2e"
NEON      = "#00ffb3"
PURPLE    = "#7b61ff"
PINK      = "#ff4f7b"
TEXT_DIM  = "#666677"
WHITE     = "#e8e8f0"
AZUL     = "#61dafb"
YUPI     = "🥳"
FIREWORKS = "🎆🎇✨"

def chip(text: str, color: str, bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, font_family="monospace", size=13, color=color),
        bgcolor=bg,
        #border=ft.border.all(1, color + "44"),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
    )


def section_card(title: str, color: str, chips: list[ft.Control], count: int) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(title, font_family="monospace", size=11,
                                    color=color, weight="bold"),
                            ft.Container(
                                content=ft.Text(str(count), font_family="monospace",
                                                size=10),#, color=color),
                                bgcolor=color + "18",
                                border_radius=100,
                                padding=ft.padding.symmetric(horizontal=9, vertical=3),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER)),
                ),
                ft.Container(
                    content=ft.Row(chips, wrap=True, spacing=8),
                    padding=16,
                ),
            ],
            spacing=0,
        ),
        bgcolor=CARD,
        border=ft.border.all(1, BORDER),
        border_radius=12,
    )


# ─── Pestaña 1: Subcadenas / Prefijos / Sufijos ───────────────────────────────

def build_tab_subcadenas(page: ft.Page) -> ft.Control:
    result_col = ft.Column(scroll="auto", spacing=14, expand=True)
    stat_sub   = ft.Text("—", size=28, weight="bold", color=NEON, font_family="monospace")
    stat_pre   = ft.Text("—", size=28, weight="bold", color=PURPLE, font_family="monospace")
    stat_suf   = ft.Text("—", size=28, weight="bold", color=PINK, font_family="monospace")
    snack      = ft.SnackBar(content=ft.Text(""), bgcolor=NEON)
    page.overlay.append(snack)

    last_results: dict = {}

    input_field = ft.TextField(
        label="Cadena σ",
        hint_text="ej: abc",
        border_color=BORDER,
        focused_border_color=NEON,
        cursor_color=NEON,
        label_style=ft.TextStyle(color=TEXT_DIM, size=11, font_family="monospace"),
        text_style=ft.TextStyle(color=WHITE, size=15, font_family="monospace"),
        bgcolor=BG,
        border_radius=8,
        filled=True,
        fill_color=BG,
    )

    def compute(e):
        s = input_field.value.strip()
        if not s:
            return
        subs = get_substrings(s)
        pres = get_prefixes(s)
        sufs = get_suffixes(s)
        last_results["subs"] = subs
        last_results["pres"] = pres
        last_results["sufs"] = sufs
        last_results["s"]    = s

        stat_sub.value = str(len(subs))
        stat_pre.value = str(len(pres))
        stat_suf.value = str(len(sufs))

        result_col.controls.clear()
        result_col.controls.append(
            section_card("SUBCADENAS", NEON,
                         [chip(t, NEON, NEON + "0a") for t in subs], len(subs))
        )   
        result_col.controls.append(
            section_card("PREFIJOS", PURPLE,
                         [chip(t, PURPLE, NEON + "0a") for t in pres], len(pres))
        )
        result_col.controls.append(
            section_card("SUFIJOS", PINK,
                         [chip(t, PINK, NEON + "0a") for t in sufs], len(sufs))
        )
        page.update()

    def export(e):
        if not last_results:
            return
        s    = last_results["s"]
        subs = last_results["subs"]
        pres = last_results["pres"]
        sufs = last_results["sufs"]
        txt = (
            f'Cadena: "{s}"\n\n'
            f"SUBCADENAS ({len(subs)}):\n{', '.join(subs)}\n\n"
            f"PREFIJOS ({len(pres)}):\n{', '.join(pres)}\n\n"
            f"SUFIJOS ({len(sufs)}):\n{', '.join(sufs)}\n"
        )
        filename = f"subcadenas_{s}.txt"
        saved_path = export_to_file(filename, txt)
        snack.content = ft.Text(f"✓  Guardado en:  {saved_path}"+ YUPI + FIREWORKS,  weight="bold")
        snack.open = True
        page.update()

    input_field.on_submit = compute

    left = ft.Container(
        content=ft.Column(
            [
                ft.Text("// ENTRADA", font_family="monospace", size=11,
                        color=PURPLE, weight="bold"),
                ft.Container(
                    content=ft.Text(
                        "Ingresa una cadena para calcular sus "
                        "subcadenas, prefijos y sufijos.",
                        size=12, color=TEXT_DIM, font_family="monospace",
                    ),
                    bgcolor=NEON + "08",
                    border=ft.border.all(1, NEON + "22"),
                    border_radius=8,
                    padding=12,
                ),
                input_field,
                ft.Row(
                    [
                        ft.Column(
                            [stat_sub, ft.Text("SUBCADENAS", size=10, color=TEXT_DIM,
                                               font_family="monospace")],
                            horizontal_alignment="center",
                        ),
                        ft.Column(
                            [stat_pre, ft.Text("PREFIJOS", size=10, color=TEXT_DIM,
                                               font_family="monospace")],
                            horizontal_alignment="center",
                        ),
                        ft.Column(
                            [stat_suf, ft.Text("SUFIJOS", size=10, color=TEXT_DIM,
                                               font_family="monospace")],
                            horizontal_alignment="center",
                        ),
                    ],
                    alignment="spaceAround",
                ),
                ft.ElevatedButton(
                    "CALCULAR",
                    on_click=compute,
                    #bgcolor=NEON,
                    #color="#000",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, NEON),
                        text_style=ft.TextStyle(font_family="monospace",
                                                weight="bold",
                                                size=12),
                    ),
                    width=999,
                    height=46,
                ),
                ft.OutlinedButton(
                    "EXPORTAR .TXT",
                    on_click=export,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, AZUL),
                        color=AZUL,
                        text_style=ft.TextStyle(font_family="monospace", weight="bold",
                                                size=11),
                    ),
                    width=999,
                    height=42,
                ),
            ],
            spacing=16,
        ),
        bgcolor=CARD,
        border=ft.border.all(1, BORDER),
        border_radius=12,
        padding=24,
        width=360,
    )

    empty = ft.Container(
        content=ft.Text("— ingresa una cadena para comenzar —",
                        font_family="monospace", size=12, color=BORDER),
        expand=True,
        height=200,
    )
    result_col.controls.append(empty)

    return ft.Row(
        [left, ft.Container(content=result_col, expand=True)],
        spacing=24,
        vertical_alignment="start",
        expand=True,
    )


# ─── Pestaña 2: Cerradura de Kleene / Positiva ───────────────────────────────

def build_tab_kleene(page: ft.Page) -> ft.Control:
    result_col = ft.Column(scroll="auto", spacing=14, expand=True)
    stat_total = ft.Text("—", size=28, weight="bold", color=NEON, font_family="monospace")
    snack      = ft.SnackBar(content=ft.Text(""), bgcolor=NEON)
    page.overlay.append(snack)

    last_results: dict = {}
    DISPLAY_LIMIT = 2000

    alpha_field = ft.TextField(
        label="Alfabeto Σ",
        hint_text="ej: ab  ó  01",
        border_color=BORDER,
        focused_border_color=NEON,
        cursor_color=NEON,
        label_style=ft.TextStyle(color=TEXT_DIM, size=11, font_family="monospace"),
        text_style=ft.TextStyle(color=WHITE, size=15, font_family="monospace"),
        bgcolor=BG,
        border_radius=8,
        filled=True,
        fill_color=BG,
    )

    maxlen_field = ft.TextField(
        label="Longitud máxima",
        hint_text="1 – 8",
        value="3",
        border_color=BORDER,
        focused_border_color=NEON,
        cursor_color=NEON,
        label_style=ft.TextStyle(color=TEXT_DIM, size=11, font_family="monospace"),
        text_style=ft.TextStyle(color=WHITE, size=15, font_family="monospace"),
        bgcolor=BG,
        border_radius=8,
        filled=True,
        fill_color=BG,
        keyboard_type="number",
    )

    def _run(kind: str):
        raw = alpha_field.value.replace(" ", "")
        chars = list(dict.fromkeys(raw))   # deduplicate, preserve order
        if not chars:
            return
        try:
            ml = int(maxlen_field.value)
            ml = max(1, min(8, ml))
        except ValueError:
            ml = 3
        maxlen_field.value = str(ml)

        data = kleene_star(chars, ml) if kind == "star" else kleene_plus(chars, ml)
        last_results["kind"]  = kind
        last_results["chars"] = chars
        last_results["ml"]    = ml
        last_results["data"]  = data

        stat_total.value = str(len(data))

        color  = NEON if kind == "star" else PURPLE
        label  = "CERRADURA DE KLEENE  Σ*" if kind == "star" else "CERRADURA POSITIVA  Σ+"
        shown  = data[:DISPLAY_LIMIT]
        chips  = []
        for t in shown:
            if t == "ε":
                chips.append(chip("ε", PINK, NEON + "44"))
            else:
                chips.append(chip(t, color, NEON + "44"))

        controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(label, font_family="monospace", size=11,
                                color=color, weight="bold"),
                        ft.Container(
                            content=ft.Text(f"{len(data):,}", font_family="monospace",
                                            size=10),# color=color),
                            bgcolor=color + "18",
                            border_radius=100,
                            padding=ft.padding.symmetric(horizontal=9, vertical=3),
                        ),
                    ],
                    alignment="spaceBetween",
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER)),
            ),
            ft.Container(
                content=ft.Row(chips, wrap=True, spacing=8),
                padding=16,
            ),
        ]

        if len(data) > DISPLAY_LIMIT:
            controls.append(
                ft.Container(
                    content=ft.Text(
                        f"⚠  Mostrando {DISPLAY_LIMIT:,} de {len(data):,} — exporta para ver todas",
                        font_family="monospace", size=11, color=PINK,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    border=ft.border.only(top=ft.border.BorderSide(1, BORDER)),
                )
            )

        result_col.controls.clear()
        result_col.controls.append(
            ft.Container(
                content=ft.Column(controls, spacing=0),
                bgcolor=CARD,
                border=ft.border.all(1, BORDER),
                border_radius=12,
            )
        )
        page.update()

    def export(e):
        if not last_results:
            return
        kind  = last_results["kind"]
        chars = last_results["chars"]
        ml    = last_results["ml"]
        data  = last_results["data"]
        tipo  = "Cerradura de Kleene (Σ*)" if kind == "star" else "Cerradura Positiva (Σ+)"
        txt = (
            f"Alfabeto: {{{', '.join(chars)}}}\n"
            f"Longitud máxima: {ml}\n"
            f"Tipo: {tipo}\n"
            f"Total de cadenas: {len(data):,}\n\n"
            + ", ".join(data) + "\n"
        )
        filename = f"cerradura_{'kleene' if kind == 'star' else 'positiva'}.txt"
        saved_path = export_to_file(filename, txt)
        snack.content = ft.Text(f"✓  Guardado en:  {saved_path} " + YUPI + FIREWORKS, weight="bold")
        snack.open = True
        page.update()

    left = ft.Container(
        content=ft.Column(
            [
                ft.Text("// ENTRADA", font_family="monospace", size=11,
                        color=PURPLE, weight="bold"),
                ft.Container(
                    content=ft.Text(
                        "Σ*  incluye la cadena vacía  ε\nΣ+  excluye la cadena vacía",
                        size=12, color=TEXT_DIM, font_family="monospace",
                    ),
                    bgcolor=NEON + "08",
                    border=ft.border.all(1, NEON + "22"),
                    border_radius=8,
                    padding=12,
                ),
                alpha_field,
                maxlen_field,
                ft.Row(
                    [
                        ft.Column(
                            [stat_total,
                             ft.Text("CADENAS", size=10, color=TEXT_DIM, font_family="monospace")],
                            horizontal_alignment="center",
                            expand=True,
                        ),
                    ],
                    alignment="spaceAround",
                ),
                ft.ElevatedButton(
                    "KLEENE  Σ*",
                    on_click=lambda e: _run("star"),
                   # bgcolor=NEON,
                   # color="#000",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, NEON),
                        text_style=ft.TextStyle(font_family="monospace",
                                                weight="bold",
                                                size=12),
                    ),
                    width=999,
                    height=46,
                ),
                ft.OutlinedButton(
                    "POSITIVA  Σ+",
                    on_click=lambda e: _run("plus"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, PURPLE),
                        color=PURPLE,
                        text_style=ft.TextStyle(font_family="monospace",
                                                size=12),
                    ),
                    width=999,
                    height=44,
                ),
                ft.OutlinedButton(
                    "EXPORTAR .TXT",
                    on_click=export,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, AZUL),
                        color=AZUL,
                        text_style=ft.TextStyle(font_family="monospace", weight="bold",
                                                size=11),
                    ),
                    width=999,
                    height=42,
                ),
            ],
            spacing=16,
        ),
        bgcolor=CARD,
        border=ft.border.all(1, BORDER),
        border_radius=12,
        padding=24,
        width=360,
    )

    empty = ft.Container(
        content=ft.Text("— define un alfabeto y genera la cerradura —",
                        font_family="monospace", size=12, color=BORDER),
        expand=True,
        height=200,
    )
    result_col.controls.append(empty)

    return ft.Row(
        [left, ft.Container(content=result_col, expand=True)],
        spacing=24,
        vertical_alignment="start",
        expand=True,
    )

# ─── Practica 3: Automatas ───────────────────────────────────────────────

def build_tab_automatas(page: ft.Page) -> ft.Control:
    result_col = ft.Column(scroll="auto", spacing=14, expand=True)
    snack = ft.SnackBar(content=ft.Text(""), bgcolor=NEON)
    page.overlay.append(snack)

    # Campos de entrada
    estados_field = ft.TextField(label="Estados (Q)", hint_text="q0,q1,q2", bgcolor=BG, border_color=BORDER)
    alfabeto_field = ft.TextField(label="Alfabeto (Σ)", hint_text="0,1", bgcolor=BG, border_color=BORDER)
    inicial_field = ft.TextField(label="Estado Inicial", hint_text="q0", bgcolor=BG, border_color=BORDER)
    finales_field = ft.TextField(label="Estados Finales (F)", hint_text="q2", bgcolor=BG, border_color=BORDER)
    transiciones_field = ft.TextField(label="Transiciones (estado,símbolo,destino)", hint_text="q0,0,q1 \nq1,λ,q2", multiline=True, bgcolor=BG, border_color=BORDER, min_lines=4)
    cadena_field = ft.TextField(label="Cadena a Simular", hint_text="0101", bgcolor=BG, border_color=BORDER)

    def parse_automata():
        try:
            states = [s.strip() for s in estados_field.value.split(",")]
            alphabet = [s.strip() for s in alfabeto_field.value.split(",")]
            start = inicial_field.value.strip()
            accept = [s.strip() for s in finales_field.value.split(",")]
            
            transitions = {}
            for line in transiciones_field.value.strip().split("\n"):
                if not line.strip(): continue
                src, sym, dst = [x.strip() for x in line.split(",")]
                if src not in transitions: transitions[src] = {}
                if sym not in transitions[src]: transitions[src][sym] = set()
                transitions[src][sym].add(dst)
            
            return Automata(states, alphabet, transitions, start, accept)
        except Exception as e:
            snack.content = ft.Text(f"Error de parsing: Verifique el formato. {e}")
            snack.open = True
            page.update()
            return None

    def run_simulation(e):
        aut = parse_automata()
        if not aut: return
        word = cadena_field.value.strip()
        
        is_acc, history = aut.simulate_word(word)
        
        result_col.controls.clear()
        
        # λ-clausura inicial
        init_closure = aut.lambda_closure({aut.start_state})
        result_col.controls.append(ft.Text(f"λ-Clausura Inicial ({aut.start_state}): {init_closure}", color=NEON, font_family="monospace"))
        
        # Historial paso a paso
        steps_ui = []
        for i, char in enumerate(word):
            steps_ui.append(ft.Text(f"Paso {i+1} | Símbolo: '{char}' -> Estados Activos: {history[i+1]}", font_family="monospace"))
            
        result_col.controls.append(ft.Container(content=ft.Column(steps_ui), padding=10, border=ft.border.all(1, BORDER), border_radius=8))
        
        # Veredicto
        color = NEON if is_acc else PINK
        texto = "CADENA ACEPTADA" if is_acc else "CADENA RECHAZADA"
        result_col.controls.append(ft.Text(texto, color=color, weight="bold", size=18, font_family="monospace"))
        page.update()

    def run_minimization(e):
        aut = parse_automata()
        if not aut: return
        
        # Minimizar
        try:
            min_dfa, particiones = minimize_dfa(aut)
            
            result_col.controls.clear()
            result_col.controls.append(ft.Text("PROCESO DE MINIMIZACIÓN", color=PURPLE, weight="bold", font_family="monospace"))
            
            # Grupos fusionados
            result_col.controls.append(ft.Text(f"Estados originales: {len(aut.states)} | Estados minimizados: {len(min_dfa.states)}", font_family="monospace"))
            result_col.controls.append(ft.Text(f"Grupos Equivalentes: {particiones}", color=AZUL, font_family="monospace"))
            
            # Nueva tabla
            trans_ui = []
            for state, paths in min_dfa.transitions.items():
                for sym, targets in paths.items():
                    trans_ui.append(ft.Text(f"{state} --({sym})--> {list(targets)[0]}", font_family="monospace"))
                    
            result_col.controls.append(ft.Container(content=ft.Column(trans_ui), padding=10, border=ft.border.all(1, BORDER), border_radius=8))
            page.update()
        except Exception as ex:
             snack.content = ft.Text(f"Error al minimizar (Asegúrese de ingresar un AFD válido): {ex}")
             snack.open = True
             page.update()

    left = ft.Container(
        content=ft.Column(
            [
                ft.Text("// DEFINICIÓN (AFND / AFN-λ / AFD)", font_family="monospace", size=11, color=NEON, weight="bold"),
                estados_field,
                alfabeto_field,
                inicial_field,
                finales_field,
                transiciones_field,
                cadena_field,
                ft.ElevatedButton("SIMULAR PASO A PASO", on_click=run_simulation, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, NEON)), width=999),
                ft.OutlinedButton("MINIMIZAR AFD", on_click=run_minimization, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), side=ft.BorderSide(1, PURPLE), color=PURPLE), width=999),
            ],
            spacing=10,
        ),
        bgcolor=CARD, border=ft.border.all(1, BORDER), border_radius=12, padding=24, width=360,
    )

    empty = ft.Container(content=ft.Text("— Define un autómata para simular o minimizar —", font_family="monospace", size=12, color=BORDER), expand=True)
    result_col.controls.append(empty)

    return ft.Row([left, ft.Container(content=result_col, expand=True)], spacing=24, vertical_alignment="start", expand=True)