import json
import os
from datetime import datetime

def calcola_distanza_ciclometrica(e1, e5):
    """Calcola la distanza assoluta sul cerchio ciclometrico (max 45)"""
    dist = abs(e1 - e5)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_previsione():
    # Ultimi dati reali inseriti (Estrazione del 27/10/2026)
    ultima_cinquina = [65, 57, 90, 11, 73]
    e1 = ultima_cinquina[0]
    e5 = ultima_cinquina[4]
    
    # MOTORE A: Distanza Ciclometrica Dinamica
    ambata = calcola_distanza_ciclometrica(e1, e5)
    
    # Se l'ambata dovesse essere 0 (casi rari), usiamo il fuori 90 standard
    if ambata == 0:
        ambata = 90
        
    # Abbinamenti Ambi (Logica del Motore A)
    ambo1 = (ambata + 45) if (ambata + 45) <= 90 else (ambata + 45 - 90)
    ambo2 = 90 - ambata
    
    # Diametrale in decina (+5 o -5 per rimanere nella stessa decina)
    if ambata % 10 < 5:
        ambo3 = ambata + 5
    else:
        ambo3 = ambata - 5

    # Struttura dati con i 6 colpi di monitoraggio richiesti
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
            {"colpo": 1, "data": "29/10/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Chiuso"},
            {"colpo": 2, "data": "30/10/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Chiuso"},
            {"colpo": 3, "data": "03/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "In Corso"},
            {"colpo": 4, "data": "05/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 5, "data": "06/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"},
            {"colpo": 6, "data": "07/11/2026", "cinquina": "", "esito_ambata": "⏳", "esito_ambi": "⏳", "stato": "Programmato"}
        ]
    }
    
    # Salvataggio nel file locale JSON
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(database_lotto, f, indent=4, ensure_ascii=False)
    print("File risultati_v4.json generato correttamente con il Motore A.")

if __name__ == "__main__":
    genera_previsione()
