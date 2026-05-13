import threading
from datetime import date

import customtkinter as ctk

from config import TEMAS, FONT
from core import build_report

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatorio")
        self.geometry("560x760")
        self.resizable(False, False)

        self._tema_atual = "dark"
        self._t = TEMAS["dark"]

        self._turno  = ctk.StringVar(value="")
        self._zerada = ctk.StringVar(value="N")

        ctk.set_appearance_mode(self._t["appearance"])
        self.configure(fg_color=self._t["bg_app"])

        self._build_ui()

    # ── Layout principal ─────────────────────────────────────────────────────

    def _build_ui(self):
        t = self._t
        self._build_header(t)
        self._build_tabview(t)

    def _build_header(self, t: dict):
        self._hdr = ctk.CTkFrame(self, fg_color=t["bg_card"], corner_radius=0)
        self._hdr.pack(fill="x")

        top_row = ctk.CTkFrame(self._hdr, fg_color="transparent")
        top_row.pack(fill="x", padx=(16, 8), pady=(16, 2))

        self._lbl_title = ctk.CTkLabel(
            top_row, text="Gerador de Relatorio",
            font=ctk.CTkFont(size=FONT["title"], weight="bold"),
            text_color=t["vinho"],
        )
        self._lbl_title.pack(side="left")

        self._btn_tema = ctk.CTkButton(
            top_row,
            text=t["icon"],
            width=36, height=28, corner_radius=8,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            border_color=t["vinho"], border_width=1,
            text_color=t["vinho"],
            hover_color=t["azul_hover"],
            command=self._toggle_tema,
        )
        self._btn_tema.pack(side="right", padx=(0, 4))

        self._lbl_date = ctk.CTkLabel(
            self._hdr,
            text=date.today().strftime("%A, %d/%m/%Y").capitalize(),
            font=ctk.CTkFont(size=14),
            text_color=t["text_muted"],
        )
        self._lbl_date.pack(pady=(0, 10))

    def _build_tabview(self, t: dict):
        self._tabview = ctk.CTkTabview(
            self, fg_color=t["bg_app"],
            segmented_button_fg_color=t["bg_card"],
            segmented_button_selected_color=t["vinho"],
            segmented_button_selected_hover_color=t["azul_hover"],
            segmented_button_unselected_color=t["bg_card"],
            segmented_button_unselected_hover_color=t["azul_hover"],
            text_color=t["text_main"],
            border_color=t["vinho"], border_width=1,
        )
        self._tabview.pack(fill="both", expand=True, padx=12, pady=(8, 12))
        self._tabview.add("Relatorio")
        self._tabview.add("Sobre")

        self._build_tab_relatorio(self._tabview.tab("Relatorio"))
        self._build_tab_sobre(self._tabview.tab("Sobre"))

    # ── Aba Relatório ────────────────────────────────────────────────────────

    def _build_tab_relatorio(self, parent):
        t   = self._t
        pad = {"padx": 8, "pady": (0, 12)}

        self._scroll = ctk.CTkScrollableFrame(
            parent, fg_color=t["bg_app"],
            scrollbar_button_color=t["vinho"],
        )
        self._scroll.pack(fill="both", expand=True)
        s = self._scroll

        # Tarefas
        self._lbl_tasks = self._card_label(s, "Tarefas realizadas durante o dia")
        self._tasks = ctk.CTkTextbox(
            s, height=130, font=ctk.CTkFont(size=FONT["caixa"]),
            fg_color=t["bg_card"], border_color=t["vinho"],
            border_width=1, corner_radius=8, text_color=t["text_main"],
        )
        self._tasks.pack(fill="x", **pad)

        # Turno
        self._lbl_turno = self._card_label(s, "Qual turno?")
        turno_row = ctk.CTkFrame(s, fg_color="transparent")
        turno_row.pack(fill="x", **pad)

        _rb_cfg = dict(
            variable=self._turno,
            font=ctk.CTkFont(size=FONT["radio"]),
            radiobutton_width=18, radiobutton_height=18,
            fg_color=t["vinho"], hover_color=t["azul_hover"],
            text_color=t["text_main"],
        )
        self._radio_manha = ctk.CTkRadioButton(turno_row, text="Manha", value="MANHA", **_rb_cfg)
        self._radio_manha.pack(side="left", padx=(0, 24))
        self._radio_tarde = ctk.CTkRadioButton(turno_row, text="Tarde", value="TARDE", **_rb_cfg)
        self._radio_tarde.pack(side="left", padx=(0, 24))

        # Lista zerada
        self._lbl_zerada = self._card_label(s, "Lista de chamados zerada?")
        zerada_row = ctk.CTkFrame(s, fg_color="transparent")
        zerada_row.pack(fill="x", **pad)
        self._chk_zerada = ctk.CTkCheckBox(
            zerada_row, text="Sim",
            variable=self._zerada, onvalue="S", offvalue="N",
            font=ctk.CTkFont(size=FONT["radio"]),
            checkbox_width=18, checkbox_height=18,
            fg_color=t["vinho"], hover_color=t["azul_hover"],
            checkmark_color="white", text_color=t["text_main"],
        )
        self._chk_zerada.pack(side="left")

        # Total de chamados
        self._lbl_total_title = self._card_label(s, "Total de chamados atendidos")
        self._lbl_total_hint = ctk.CTkLabel(
            s, text="Planejados, pendentes e solucionados (separados por virgula)",
            font=ctk.CTkFont(size=FONT["text"]),
            text_color=t["text_muted"], anchor="w",
        )
        self._lbl_total_hint.pack(fill="x", padx=8, pady=(0, 4))

        total_row = ctk.CTkFrame(s, fg_color="transparent")
        total_row.pack(fill="x", **pad)
        self._total = ctk.CTkEntry(
            total_row, placeholder_text="Ex: 5, 3, 12",
            font=ctk.CTkFont(size=FONT["caixa"]),
            fg_color=t["bg_card"], border_color=t["border_total"],
            corner_radius=8, text_color=t["text_main"],
        )
        self._total.pack(side="left", fill="x", expand=True)
        self._total.bind("<KeyRelease>", self._update_sum)

        self._sum_label = ctk.CTkLabel(
            total_row, text="",
            font=ctk.CTkFont(size=FONT["button"], weight="bold"),
            text_color=t["vinho"], width=80,
        )
        self._sum_label.pack(side="left", padx=(10, 0))

        # Botão gerar
        self._btn = ctk.CTkButton(
            s, text="Gerar Relatorio",
            font=ctk.CTkFont(size=FONT["button"], weight="bold"),
            height=44, corner_radius=8,
            fg_color=t["vinho"], hover_color=t["azul_hover"],
            command=self._on_generate,
        )
        self._btn.pack(fill="x", padx=8, pady=(8, 12))

        # Resultado
        self._lbl_result_title = self._card_label(s, "Relatorio gerado")
        self._result = ctk.CTkTextbox(
            s, height=200, font=ctk.CTkFont(family="Courier", size=FONT["button"]),
            fg_color=t["bg_card"], border_color=t["border_result"],
            border_width=1, corner_radius=8, state="disabled",
            text_color=t["text_main"],
        )
        self._result.pack(fill="x", **pad)

        self._copy_btn = ctk.CTkButton(
            s, text="Copiar relatorio",
            font=ctk.CTkFont(size=FONT["button"]), height=36, corner_radius=8,
            fg_color="transparent", border_color=t["border_total"], border_width=1,
            text_color=t["text_muted"], hover_color=t["azul_hover"],
            command=self._copy_result,
        )
        self._copy_btn.pack(fill="x", padx=8, pady=(0, 16))

    # ── Aba Sobre ────────────────────────────────────────────────────────────

    def _build_tab_sobre(self, parent):
        t = self._t
        self._sobre_frame = ctk.CTkFrame(parent, fg_color=t["bg_card"], corner_radius=12)
        self._sobre_frame.pack(fill="both", expand=True, padx=8, pady=16)

        self._lbl_sobre_title = ctk.CTkLabel(
            self._sobre_frame, text="Sobre a aplicacao",
            font=ctk.CTkFont(size=FONT["title"], weight="bold"),
            text_color=t["vinho"],
        )
        self._lbl_sobre_title.pack(pady=(24, 12))

        self._lbl_sobre_body = ctk.CTkLabel(
            self._sobre_frame,
            text=(
                "Esta aplicacao tem a finalidade de facilitar a criacao\n"
                "de um relatorio, ao final do dia, para manter o turno\n"
                "contrario informado sobre as informacoes que ocorreram\n"
                "durante o outro turno."
            ),
            font=ctk.CTkFont(size=FONT["text"]),
            text_color=t["text_main"], justify="center",
        )
        self._lbl_sobre_body.pack(padx=24, pady=(0, 24))

    # ── Helpers de UI ────────────────────────────────────────────────────────

    def _card_label(self, parent, txt: str) -> ctk.CTkLabel:
        lbl = ctk.CTkLabel(
            parent, text=txt,
            font=ctk.CTkFont(size=FONT["label"], weight="bold"),
            text_color=self._t["text_main"], anchor="w",
        )
        lbl.pack(fill="x", padx=8, pady=(14, 6))
        return lbl

    # ── Toggle de tema ───────────────────────────────────────────────────────

    def _toggle_tema(self):
        self._tema_atual = "light" if self._tema_atual == "dark" else "dark"
        self._t = TEMAS[self._tema_atual]
        ctk.set_appearance_mode(self._t["appearance"])
        self._apply_tema()

    def _apply_tema(self):
        t = self._t
        self.configure(fg_color=t["bg_app"])

        self._hdr.configure(fg_color=t["bg_card"])
        self._lbl_title.configure(text_color=t["vinho"])
        self._lbl_date.configure(text_color=t["text_muted"])

        self._btn_tema.configure(
            text=t["icon"], border_color=t["vinho"],
            text_color=t["vinho"], hover_color=t["azul_hover"],
        )
        self._tabview.configure(
            fg_color=t["bg_app"],
            segmented_button_fg_color=t["bg_card"],
            segmented_button_selected_color=t["vinho"],
            segmented_button_selected_hover_color=t["azul_hover"],
            segmented_button_unselected_color=t["bg_card"],
            segmented_button_unselected_hover_color=t["azul_hover"],
            text_color=t["text_main"],
            border_color=t["vinho"],
        )
        self._scroll.configure(fg_color=t["bg_app"], scrollbar_button_color=t["vinho"])

        for lbl in (
            self._lbl_tasks, self._lbl_turno, self._lbl_zerada,
            self._lbl_total_title, self._lbl_result_title,
        ):
            lbl.configure(text_color=t["text_main"])

        self._lbl_total_hint.configure(text_color=t["text_muted"])

        self._tasks.configure(fg_color=t["bg_card"], border_color=t["vinho"], text_color=t["text_main"])
        self._total.configure(fg_color=t["bg_card"], border_color=t["border_total"], text_color=t["text_main"])
        self._sum_label.configure(text_color=t["vinho"])

        for rb in (self._radio_manha, self._radio_tarde):
            rb.configure(fg_color=t["vinho"], hover_color=t["azul_hover"], text_color=t["text_main"])

        self._chk_zerada.configure(fg_color=t["vinho"], hover_color=t["azul_hover"], text_color=t["text_main"])
        self._btn.configure(fg_color=t["vinho"], hover_color=t["azul_hover"])
        self._result.configure(fg_color=t["bg_card"], border_color=t["border_result"], text_color=t["text_main"])
        self._copy_btn.configure(border_color=t["border_total"], text_color=t["text_muted"], hover_color=t["azul_hover"])

        self._sobre_frame.configure(fg_color=t["bg_card"])
        self._lbl_sobre_title.configure(text_color=t["vinho"])
        self._lbl_sobre_body.configure(text_color=t["text_main"])

    # ── Lógica de negócio ────────────────────────────────────────────────────

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
            daemon=True,
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
        txt = self._result.get("1.0", "end").strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self._copy_btn.configure(text="Copiado!")
            self.after(2000, lambda: self._copy_btn.configure(text="Copiar relatorio"))

    def _flash_error(self, msg: str):
        self._btn.configure(text=f"Aviso: {msg}", fg_color="#A32D2D")
        self.after(2500, lambda: self._btn.configure(
            text="Gerar Relatorio", fg_color=self._t["vinho"],
        ))
