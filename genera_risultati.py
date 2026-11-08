import json
import os

def calcola_distanza_ciclometrica(e1, e5):
    dist = abs(e1 - e5)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_previsione():
    # Ultimi dati reali di partenza (Estrazione del 06/11/2026)
    e1 = 17
    e5 = 52
    
    # MOTORE A: Distanza Ciclometrica Dinamica
    ambata = calcola_distanza_ciclometrica(e1, e5)
    if ambata == 0:
        ambata = 90
        
    # Abbinamenti Ambi (Logica del Motore A)
    ambo1 = (ambata + 45) if (ambata + 45) <= 90 else (ambata + 45 - 90)
    ambo2 = 90 - ambata
    
    if ambata % 10 < 5:
        ambo3 = ambata + 5
    else:
        ambo3 = ambata - 5

    # NUOVO CICLO DI 6 COLPI (Partenza 07/11/2026)
    database_lotto = {
        "configurazione": {
            "motore_attivo": "Motore A - Distanza Ciclometrica Dinamica",
            "ruota": "BARI",
            "protocollo": "SOLO STUDIO",
            "data_generazione": "07/11/2026"
        },
        "previsione_corrente": {
            "ambata": ambata,
            "ambi_secchi": [
                f"{ambata}-{ambo1}",
                f"{ambata}-{ambo2}",
                f"{ambata}-{ambo3}"
            ]
        },
        "tabella_colpi": [
            {"colpo": 1, "data": "07/11/2026", "cinquina": "64-9-1-8-12", "esito_ambata": "NEGATIVO", "esito_ambi": "NEGATIVO", "stato": "Chiuso"},
            {"colpo": 2, "data": "10/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "In corso"},
            {"colpo": 3, "data": "12/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 4, "data": "13/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 5, "data": "14/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 6, "data": "17/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"}
        ]
    }
    
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(database_lotto, f, indent=4, ensure_ascii=False)
    print("Nuovo ciclo avviato! Previsione attiva: Ambata 35.")

if __name__ == "__main__":
    genera_previsione()
