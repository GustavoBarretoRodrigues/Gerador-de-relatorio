import re
import threading
from datetime import date

import customtkinter as ctk
from spellchecker import SpellChecker

# ── Configuração visual ──────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

VINHO      = "#6e0202"
AZUL_HOVER = "#01167d"
BG_CARD    = "#1e1e1e"
BG_APP     = "#161616"
TEXT_MUTED = "#888880"

# ── Correção ortográfica ─────────────────────────────────────────────────────
spell = SpellChecker(language="pt")

def correct_spelling(sentence: str) -> str:
    sentence = re.sub(r"\s+", " ", sentence.strip())
    sentence = re.sub(r"\s+([,.!?])", r"\1", sentence)
    sentence = re.sub(r"([,.!?])([^\s])", r"\1 \2", sentence)

    words = sentence.split()
    corrected = []
    for word in words:
        clean = re.sub(r"[^\wáéíóúãõâêîôûç]", "", word.lower())
        if clean:
            fixed = spell.correction(clean)
            if fixed:
                corrected.append(re.sub(clean, fixed, word, flags=re.IGNORECASE))
            else:
                corrected.append(word)
        else:
            corrected.append(word)

    sentence = " ".join(corrected)
    return sentence[0].upper() + sentence[1:] if sentence else sentence

# ── Geração do relatório ─────────────────────────────────────────────────────
def build_report(tasks_text: str, turno: str, zerada: str, total_str: str) -> str:
    current_date = date.today().strftime("%d/%m/%Y")
    lines = [f"RELATORIO - TURNO {turno} ({current_date})"]

    for raw in tasks_text.strip().splitlines():
        raw = raw.strip()
        if raw:
            lines.append("* " + correct_spelling(raw))

    if zerada == "S":
        lines.append("* Lista de chamados zerada")

    try:
        parts = [int(x.strip()) for x in total_str.split(",") if x.strip()]
        total = sum(parts)
    except ValueError:
        total = 0

    lines.append(
        f"Chamados atendidos (planejados, pendentes e solucionados): {total}"
    )
    return "\n".join(lines)

# ── Interface ────────────────────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatorio")
        self.geometry("560x760")
        self.resizable(False, False)
        self.configure(fg_color=BG_APP)

        self._turno  = ctk.StringVar(value="")
        self._zerada = ctk.StringVar(value="N")

        self._build_ui()

    # ── Layout ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Cabeçalho
        hdr = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0)
        hdr.pack(fill="x")
        ctk.CTkLabel(
            hdr, text="Gerador de Relatorio",
            font=ctk.CTkFont(size=18, weight="bold"), text_color=VINHO
        ).pack(pady=(16, 2))
        ctk.CTkLabel(
            hdr,
            text=date.today().strftime("%A, %d/%m/%Y").capitalize(),
            font=ctk.CTkFont(size=12), text_color=TEXT_MUTED
        ).pack(pady=(0, 10))

        # Abas
        self._tabview = ctk.CTkTabview(
            self, fg_color=BG_APP,
            segmented_button_fg_color=BG_CARD,
            segmented_button_selected_color=VINHO,
            segmented_button_selected_hover_color=AZUL_HOVER,
            segmented_button_unselected_color=BG_CARD,
            segmented_button_unselected_hover_color=AZUL_HOVER,
            text_color="white",
            border_color=VINHO, border_width=1
        )
        self._tabview.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        self._tabview.add("Relatorio")
        self._tabview.add("Sobre")

        self._build_tab_relatorio(self._tabview.tab("Relatorio"))
        self._build_tab_sobre(self._tabview.tab("Sobre"))

    def _build_tab_relatorio(self, parent):
        pad = {"padx": 8, "pady": (0, 12)}

        scroll = ctk.CTkScrollableFrame(parent, fg_color=BG_APP, scrollbar_button_color=VINHO)
        scroll.pack(fill="both", expand=True)

        # Tarefas
        self._card_label(scroll, "Tarefas realizadas durante o dia")
        self._tasks = ctk.CTkTextbox(
            scroll, height=130, font=ctk.CTkFont(size=13),
            fg_color=BG_CARD, border_color=VINHO, border_width=1, corner_radius=8
        )
        self._tasks.pack(fill="x", **pad)

        # Turno
        self._card_label(scroll, "Qual turno?")
        turno_row = ctk.CTkFrame(scroll, fg_color="transparent")
        turno_row.pack(fill="x", **pad)
        for label, val in [("Manha", "MANHA"), ("Tarde", "TARDE")]:
            ctk.CTkRadioButton(
                turno_row, text=label, variable=self._turno, value=val,
                font=ctk.CTkFont(size=13), radiobutton_width=18, radiobutton_height=18,
                fg_color=VINHO, hover_color=AZUL_HOVER
            ).pack(side="left", padx=(0, 24))

        # Lista zerada
        self._card_label(scroll, "Lista de chamados zerada?")
        zerada_row = ctk.CTkFrame(scroll, fg_color="transparent")
        zerada_row.pack(fill="x", **pad)
        ctk.CTkCheckBox(
            zerada_row, text="Sim",
            variable=self._zerada, onvalue="S", offvalue="N",
            font=ctk.CTkFont(size=13),
            checkbox_width=18, checkbox_height=18,
            fg_color=VINHO, hover_color=AZUL_HOVER, checkmark_color="white"
        ).pack(side="left")

        # Total de chamados
        self._card_label(scroll, "Total de chamados atendidos")
        ctk.CTkLabel(
            scroll,
            text="Planejados, pendentes e solucionados (separados por virgula)",
            font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, anchor="w"
        ).pack(fill="x", padx=8, pady=(0, 4))

        total_row = ctk.CTkFrame(scroll, fg_color="transparent")
        total_row.pack(fill="x", **pad)
        self._total = ctk.CTkEntry(
            total_row, placeholder_text="Ex: 5, 3, 12",
            font=ctk.CTkFont(size=13), fg_color=BG_CARD,
            border_color="#444", corner_radius=8
        )
        self._total.pack(side="left", fill="x", expand=True)
        self._total.bind("<KeyRelease>", self._update_sum)
        self._sum_label = ctk.CTkLabel(
            total_row, text="", font=ctk.CTkFont(size=13, weight="bold"),
            text_color=VINHO, width=80
        )
        self._sum_label.pack(side="left", padx=(10, 0))

        # Botao gerar
        self._btn = ctk.CTkButton(
            scroll, text="Gerar Relatorio",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=44, corner_radius=8,
            fg_color=VINHO, hover_color=AZUL_HOVER,
            command=self._on_generate
        )
        self._btn.pack(fill="x", padx=8, pady=(8, 12))

        # Resultado
        self._card_label(scroll, "Relatorio gerado")
        self._result = ctk.CTkTextbox(
            scroll, height=200, font=ctk.CTkFont(family="Courier", size=12),
            fg_color=BG_CARD, border_color="#333", border_width=1,
            corner_radius=8, state="disabled"
        )
        self._result.pack(fill="x", **pad)

        self._copy_btn = ctk.CTkButton(
            scroll, text="Copiar relatorio",
            font=ctk.CTkFont(size=13), height=36, corner_radius=8,
            fg_color="transparent", border_color="#444", border_width=1,
            text_color=TEXT_MUTED, hover_color=AZUL_HOVER,
            command=self._copy_result
        )
        self._copy_btn.pack(fill="x", padx=8, pady=(0, 16))

    def _build_tab_sobre(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=8, pady=16)

        ctk.CTkLabel(
            frame, text="Sobre a aplicacao",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=VINHO
        ).pack(pady=(24, 12))

        ctk.CTkLabel(
            frame,
            text=(
                "Esta aplicacao tem a finalidade de facilitar a criacao\n"
                "de um relatorio, ao final do dia, para manter o turno\n"
                "contrario informado sobre as informacoes que ocorreram\n"
                "durante o outro turno."
            ),
            font=ctk.CTkFont(size=13),
            text_color="white",
            justify="center"
        ).pack(padx=24, pady=(0, 24))

    def _card_label(self, parent, text: str):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white", anchor="w"
        ).pack(fill="x", padx=8, pady=(14, 6))

    # ── Logica ───────────────────────────────────────────────────────────────
    def _update_sum(self, _event=None):
        raw = self._total.get()
        try:
            parts = [int(x.strip()) for x in raw.split(",") if x.strip()]
            self._sum_label.configure(text=f"= {sum(parts)}" if parts else "")
        except ValueError:
            self._sum_label.configure(text="")

    def _on_generate(self):
        tasks  = self._tasks.get("1.0", "end").strip()
        turno  = self._turno.get()
        zerada = self._zerada.get()
        total  = self._total.get().strip()

        if not tasks:
            self._flash_error("Descreva as tarefas do turno."); return
        if not turno:
            self._flash_error("Selecione o turno."); return

        self._btn.configure(state="disabled", text="Gerando...")
        threading.Thread(
            target=self._generate_thread,
            args=(tasks, turno, zerada, total),
            daemon=True
        ).start()

    def _generate_thread(self, tasks, turno, zerada, total):
        report = build_report(tasks, turno, zerada, total)
        self.after(0, self._show_result, report)

    def _show_result(self, report: str):
        self._result.configure(state="normal")
        self._result.delete("1.0", "end")
        self._result.insert("1.0", report)
        self._result.configure(state="disabled")
        self._btn.configure(state="normal", text="Gerar Relatorio")

    def _copy_result(self):
        text = self._result.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._copy_btn.configure(text="Copiado!")
            self.after(2000, lambda: self._copy_btn.configure(text="Copiar relatorio"))

    def _flash_error(self, msg: str):
        self._btn.configure(text=f"Aviso: {msg}", fg_color="#A32D2D")
        self.after(2500, lambda: self._btn.configure(
            text="Gerar Relatorio", fg_color=VINHO
        ))

# ── Entrada ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()