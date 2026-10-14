import json
import os

def calcola_distanza_ciclometrica(a, b):
    """Calcola la distanza ciclometrica (massimo 45) tra due numeri."""
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(numero):
    """Applica la regola del fuori 90."""
    while numero > 90:
        numero -= 90
    while numero <= 0:
        numero += 90
    return numero

def genera_previsione_laboratorio():
    nome_file_json = 'estrazioni.json'
    nome_file_report = 'risultati_v4.txt'

    if not os.path.exists(nome_file_json):
        print(f"[ERRORE] File {nome_file_json} non trovato nella cartella corrente!")
        return

    with open(nome_file_json, 'r', encoding='utf-8') as f:
        dati = json.load(f)
    
    # Nel tuo JSON Bari contiene direttamente la lista di tutte le cinquine estratte
    try:
        ruota_bari = dati['Bari']
        cinquina_precedente = ruota_bari[-2] # Sabato 10 Ottobre
        cinquina_attuale = ruota_bari[-1]    # Martedì 13 Ottobre
    except (KeyError, IndexError):
        print("[ERRORE] Struttura JSON non compatibile o dati insufficienti su Bari.")
        return

    # Recuperiamo il PRIMO ESTRATTO di ciascuna cinquina (Indice 0)
    primo_precedente = int(cinquina_precedente[0]) # Primo di Sabato (16)
    primo_attuale = int(cinquina_attuale[0])       # Primo di Martedì (56)

    # Calcolo del FISSO DINAMICO (Passo Adattivo Ciclometrico)
    fisso_dinamico = calcola_distanza_ciclometrica(primo_attuale, primo_precedente)
    
    # Correttivo di sicurezza se la distanza è nulla
    if fisso_dinamico == 0 or fisso_dinamico == 90:
        fisso_dinamico = 40

    # Calcolo Previsione: 1° Attuale di Bari + Fisso Dinamico
    ambata = fuori_90(primo_attuale + fisso_dinamico)

    # Calcolo Abbinamenti Matematici di Laboratorio per Ambo Secco
    ambo1 = fuori_90(ambata + 45)
    ambo2 = fuori_90(90 - ambata)
    ambo3 = fuori_90(91 - ambata)

    # Controllo e Correttivo anti-duplicazione
    abbinamenti = [ambo1, ambo2, ambo3]
    for i in range(len(abbinamenti)):
        if abbinamenti[i] == ambata:
            abbinamenti[i] = fuori_90(abbinamenti[i] + 1)

    # Costruzione del Blocco di Testo per Console e File
    output = []
    output.append("=" * 60)
    output.append("        LOTTO INTELLIGENCE V8 - AMBIENTE LABORATORIO (PC)        ")
    output.append("                 ALGORITMO REGINA DINAMICO                      ")
    output.append("=" * 60)
    output.append(f"Cinquina Precedente Bari : {cinquina_precedente}")
    output.append(f"Cinquina Attuale Bari    : {cinquina_attuale}")
    output.append(f"Formula: 1° Ba Prec ({primo_precedente}) vs 1° Ba Att ({primo_attuale})")
    output.append(f"--> FISSO DINAMICO RILEVATO: +{fisso_dinamico}")
    output.append("-" * 60)
    output.append(" PREVISIONE IN CORSO (PROSSIMO COLPO - SOLO STUDIO):")
    output.append(" Ruota Attiva      : BARI (Ruota Unica)")
    output.append(f" Ambata Principale : {ambata}")
    output.append(f" I 3 Ambi Secchi   : {ambata}-{abbinamenti[0]}, {ambata}-{abbinamenti[1]}, {ambata}-{abbinamenti[2]}")
    output.append("=" * 60)
    output.append("NOTA: Configurazione esclusiva del Laboratorio Locale.")
    output.append("Il server di Produzione GitHub rimane CONGELATO sul FISSO +31.")
    output.append("=" * 60)

    # Stampa a video sul Terminale
    testo_completo = "\n".join(output)
    print(testo_completo)

    # Scrittura e Aggiornamento automatico del file risultati_v4.txt
    with open(nome_file_report, 'w', encoding='utf-8') as f_report:
        f_report.write(testo_completo)
    print(f"\n[OK] File '{nome_file_report}' aggiornato con successo!")

if __name__ == "__main__":
    genera_previsione_laboratorio()
