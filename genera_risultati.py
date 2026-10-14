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
    nome_file_report_json = 'risultati_v4.json' # Ripristinato il formato JSON per l'index

    if not os.path.exists(nome_file_json):
        print(f"[ERRORE] File {nome_file_json} non trovato nella cartella corrente!")
        return

    with open(nome_file_json, 'r', encoding='utf-8') as f:
        dati = json.load(f)
    
    try:
        ruota_bari = dati['Bari']
        cinquina_precedente = ruota_bari[-2]
        cinquina_attuale = ruota_bari[-1]
    except (KeyError, IndexError):
        print("[ERRORE] Struttura JSON non compatibile o dati insufficienti su Bari.")
        return

    # Recuperiamo il PRIMO ESTRATTO di ciascuna cinquina (Indice 0)
    primo_precedente = int(cinquina_precedente[0])
    primo_attuale = int(cinquina_attuale[0])

    # Calcolo del FISSO DINAMICO
    fisso_dinamico = calcola_distanza_ciclometrica(primo_attuale, primo_precedente)
    if fisso_dinamico == 0 or fisso_dinamico == 90:
        fisso_dinamico = 40

    # Calcolo Previsione
    ambata = fuori_90(primo_attuale + fisso_dinamico)

    # Calcolo Abbinamenti
    ambo1 = fuori_90(ambata + 45)
    ambo2 = fuori_90(90 - ambata)
    ambo3 = fuori_90(91 - ambata)

    abbinamenti = [ambo1, ambo2, ambo3]
    for i in range(len(abbinamenti)):
        if abbinamenti[i] == ambata:
            abbinamenti[i] = fuori_90(abbinamenti[i] + 1)

    # Creazione del dizionario dati strutturato per l'interfaccia INDEX
    dati_output = {
        "ambiente": "LABORATORIO (PC) - STRATEGIA DINAMICA",
        "ruota_attiva": "BARI",
        "ultimo_calcolo": {
            "primo_precedente": primo_precedente,
            "primo_attuale": primo_attuale,
            "fisso_dinamico_applicato": fisso_dinamico
        },
        "previsione": {
            "tipo_giocata": "SOLO STUDIO (Spesa 0€)",
            "ambata_principale": ambata,
            "ambi_secchi": [
                f"{ambata}-{abbinamenti[0]}",
                f"{ambata}-{abbinamenti[1]}",
                f"{ambata}-{abbinamenti[2]}"
            ]
        },
        "nota_architettura": "Server di Produzione GitHub congelato su FISSO +31"
    }

    # Stampa di controllo a video sul Terminale
    print("=" * 60)
    print("        LOTTO INTELLIGENCE V8 - GENERAZIONE JSON COMPLETATA      ")
    print("=" * 60)
    print(json.dumps(dati_output, indent=4, ensure_ascii=False))
    print("=" * 60)

    # Scrittura del file risultati_v4.json pulito e strutturato per la web-app
    with open(nome_file_report_json, 'w', encoding='utf-8') as f_json:
        json.dump(dati_output, f_json, indent=4, ensure_ascii=False)
    print(f"\n[OK] File '{nome_file_report_json}' aggiornato con successo per l'interfaccia index!")

if __name__ == "__main__":
    genera_previsione_laboratorio()
