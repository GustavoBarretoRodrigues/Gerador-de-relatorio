import re
from datetime import date
from spellchecker import SpellChecker

spell = SpellChecker(language='pt')

def correct_spelling(sentence: str) -> str:
    """
    Corrige ortografia básica + normaliza texto:
    - Remove espaços extras
    - Ajusta pontuação
    - Corrige palavras erradas (offline)
    - Capitaliza frase
    """

    # Remove espaços duplicados
    sentence = re.sub(r'\s+', ' ', sentence.strip())

    # Corrige pontuação
    sentence = re.sub(r'\s+([,.!?])', r'\1', sentence)
    sentence = re.sub(r'([,.!?])([^\s])', r'\1 \2', sentence)

    # Corrige palavras individualmente
    words = sentence.split()
    corrected_words = []

    for word in words:
        # Mantém pontuação separada
        clean_word = re.sub(r'[^\wáéíóúãõâêîôûç]', '', word.lower())

        if clean_word:
            corrected = spell.correction(clean_word)
            if corrected:
                # Mantém pontuação original
                corrected_word = re.sub(clean_word, corrected, word, flags=re.IGNORECASE)
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)

    sentence = " ".join(corrected_words)

    # Capitaliza primeira letra
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]

    return sentence

def generate_report():
    choose_shift = ''
    current_date = date.today().strftime("%d/%m/%Y")

    while choose_shift not in ['M', 'T']:
        choose_shift = input("Turno da manhã ou tarde (M/T): ").upper().strip()

    if choose_shift == "M": turn = 'MANHÃ'
    if choose_shift == "T": turn = 'TARDE'


    report = [f"RELATÓRIO – TURNO {turn} ({current_date})"]

    phrases = []
    print("Digite as frases para o relatório. Quando quiser parar, digite STOP.")
    while True:
        sentence = input("Frase: ")
        if sentence.strip().upper() == "STOP":
            break
        phrases.append("* " + correct_spelling(sentence))

    report.extend(phrases)

    reset_list = ""

    while reset_list not in ['S', 'N']:
        reset_list = input("A lista de chamados foi zerada? (S/N): ").upper().strip()

    if reset_list == 'S':report.append("* Lista de chamados zerada")

    total = input("Informe o total de chamados atendidos (planejados, pendentes e solucionados): ")
    total_calls = list(map(int, total.split(",")))
    report.append(f"Chamados atendidos (planejados, pendentes e solucionados) : {sum(total_calls)}")

    print('-'*50)
    print("\n".join(report))
    print('-' * 50)

if __name__ == "__main__":
    generate_report()
    # input serve para terminal não fechar, como estou gerando executavel
    input('\nPressione "ENTER" para fechar!')

