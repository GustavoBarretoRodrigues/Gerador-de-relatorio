import re
from datetime import date

from spellchecker import SpellChecker

from config import WHITELIST

spell = SpellChecker(language=["pt", "en"])
spell.word_frequency.load_words(WHITELIST)


def _preserve_case(original: str, corrected: str) -> str:
    """Aplica a capitalização do original na palavra corrigida."""
    if original.isupper():
        return corrected.upper()
    if original[0].isupper():
        return corrected.capitalize()
    return corrected


def correct_spelling(sentence: str) -> str:
    """
    Corrige erros ortográficos em uma frase, preservando:
    - Capitalização original de cada palavra
    - Pontuação colada (ex: 'servidor,' → núcleo 'servidor' + sufixo ',')
    - Termos técnicos em inglês e palavras da whitelist
    """
    # Normaliza espaços e pontuação
    sentence = re.sub(r"\s+", " ", sentence.strip())
    sentence = re.sub(r"\s+([,.!?])", r"\1", sentence)
    sentence = re.sub(r"([,.!?])([^\s])", r"\1 \2", sentence)

    # Padrão que separa prefixo-não-alfanumérico | núcleo | sufixo-não-alfanumérico
    _WORD_RE = re.compile(
        r"^([^\wáéíóúãõâêîôûç]*)"   # prefixo (aspas, parêntese, etc.)
        r"([\wáéíóúãõâêîôûç]+)"      # núcleo da palavra
        r"([^\wáéíóúãõâêîôûç]*)$"   # sufixo (pontuação, etc.)
    )

    corrected_words = []
    for word in sentence.split():
        m = _WORD_RE.match(word)
        if not m:
            corrected_words.append(word)
            continue

        prefix, core, suffix = m.groups()
        core_lower = core.lower()

        # Palavras na whitelist nunca são corrigidas
        if core_lower in WHITELIST:
            corrected_words.append(word)
            continue

        suggestion = spell.correction(core_lower)

        # Só substitui se o corretor sugeriu algo diferente
        if suggestion and suggestion != core_lower:
            fixed = _preserve_case(core, suggestion)
            corrected_words.append(prefix + fixed + suffix)
        else:
            corrected_words.append(word)

    result = " ".join(corrected_words)
    return result[0].upper() + result[1:] if result else result

def build_report(tasks_text: str, turno: str, zerada: str, total_str: str) -> str:
    """Monta o texto final do relatório a partir dos dados da UI."""
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
