import json
import os
from datetime import datetime

def calcola_distanza_ciclometrica(e1, e5):
    dist = abs(e1 - e5)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_previsione():
    # Ultimi dati reali di partenza (Estrazione del 27/10/2026)
    e1 = 65
    e5 = 73
    
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

    # NUOVA STRUTTURA ALLINEATA CON IL CALENDARIO REALE RECENTE
    database_lotto = {
        "configurazione": {
            "motore_attivo": "Motore A - Distanza Ciclometrica Dinamica",
            "ruota": "BARI",
            "protocollo": "SOLO STUDIO",
            "data_generazione": "28/10/2026"
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
            {"colpo": 1, "data": "29/10/2026", "cinquina": "28-19-52-20-46", "esito_ambata": "Negativo", "esito_ambi": "Negativo", "stato": "Chiuso"},
            {"colpo": 2, "data": "30/10/2026", "cinquina": "58-79-20-27-7", "esito_ambata": "Negativo", "esito_ambi": "Negativo", "stato": "Chiuso"},
            {"colpo": 3, "data": "31/10/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "In corso"},
            {"colpo": 4, "data": "03/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 5, "data": "05/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 6, "data": "06/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"}
        ]
    }
    
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(database_lotto, f, indent=4, ensure_ascii=False)
    print("File risultati_v4.json rigenerato con allineamento date (Colpo 3 Attivo).")

if __name__ == "__main__":
    genera_previsione()
