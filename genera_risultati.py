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
    # 1. Caricamento del file estrazioni.json locale
    if not os.path.exists('estrazioni.json'):
        print("[ERRORE] File estrazioni.json non trovato nella cartella corrente!")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        dati = json.load(f)
    
    # Assumiamo che il file contenga una lista di estrazioni ordinate dalla più vecchia alla più recente
    # Estraiamo le ultime due estrazioni per la ruota di BARI
    try:
        estrazione_precedente = dati[-2]['BARI']
        ultima_estrazione = dati[-1]['BARI']
        data_ultima = dati[-1].get('DATA', 'Ultima')
    except (IndexError, KeyError):
        print("[ERRORE] Struttura del file JSON non valida o dati insufficienti (servono almeno 2 estrazioni).")
        return

    # 2. Recupero dei Primi Estratti di Bari
    primo_precedente = int(estrazione_precedente[0]) # Sabato (es. 16)
    primo_ultimo = int(ultima_estrazione[0])         # Martedì (es. 56)

    # 3. Calcolo del FISSO DINAMICO (Passo Adattivo)
    # Calcola la distanza ciclometrica tra gli ultimi due primi estratti
    fisso_dinamico = calcola_distanza_ciclometrica(primo_ultimo, primo_precedente)
    
    # Se la distanza è troppo bassa (es. 0), applichiamo un correttivo di sicurezza (es. +40 di default)
    if fisso_dinamico == 0 or fisso_dinamico == 90:
        fisso_dinamico = 40

    # 4. Calcolo dell'Ambata Principale (1° Estratto Ultima Estrazione + Fisso Dinamico)
    ambata = fuori_90(primo_ultimo + fisso_dinamico)

    # 5. Calcolo degli Abbinamenti per Ambo Secco (Algoritmo di Laboratorio)
    # Usiamo il Diametrale (+45), il Complementare (90 - ambata) e il Simmetrico a 91
    ambo1 = fuori_90(ambata + 45)
    ambo2 = fuori_90(90 - ambata)
    ambo3 = fuori_90(91 - ambata)

    # Se un abbinamento coincide con l'ambata, applichiamo un correttivo (+1)
    abbinamenti = [ambo1, ambo2, ambo3]
    for i in range(len(abbinamenti)):
        if abbinamenti[i] == ambata:
            abbinamenti[i] = fuori_90(abbinamenti[i] + 1)

    # 6. Output dei Risultati a Console
    print("=" * 60)
    print("        LOTTO INTELLIGENCE V8 - AMBIENTE LABORATORIO (PC)        ")
    print("                 ALGORITMO REGINA DINAMICO                      ")
    print("=" * 60)
    print(f"Analisi basata sull'estrazione del: {data_ultima}")
    print(f"1° Ba precedente: {primo_precedente} | 1° Ba attuale: {primo_ultimo}")
    print(f"--> FISSO DINAMICO CALCOLATO: +{fisso_dinamico}")
    print("-" * 60)
    print(f" PREVISIONE IN CORSO (SOLO STUDIO - SPESA 0€):")
    print(f" Ruota Attiva      : BARI (Unica)")
    print(f" Ambata Principale : {ambata}")
    print(f" I 3 Ambi Secchi   : {ambata}-{abbinamenti[0]}, {ambata}-{abbinamenti[1]}, {ambata}-{abbinamenti[2]}")
    print("=" * 60)
    print("NOTA: Questa configurazione è attiva SOLO SUL PC LOCALE.")
    print("Il server di Produzione GitHub rimane CONGELATO sul FISSO +31.")
    print("=" * 60)

if __name__ == "__main__":
    genera_previsione_laboratorio()
