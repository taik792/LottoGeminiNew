import json
import os

def aggiorna_risultati_json(primo_estratto_bari):
    """
    Calcola la nuova logica Regina Concentrato (Solo BARI)
    e sovrascrive correttamente il file risultati_v4.json sul PC.
    """
    # 1. Calcolo Ambata con Fisso +31 (Fuori 90)
    ambata = primo_estratto_bari + 31
    if ambata > 90:
        ambata -= 90
        
    # 2. Sviluppo dei 3 Ambi Secchi con passi ottimizzati (+9, +20, +74)
    passi = [9, 20, 74]
    ambi = []
    for p in passi:
        abbinamento = ambata + p
        if abbinamento > 90:
            abbinamento -= 90
        ambi.append(f"{ambata}-{abbinamento}")
        
    # 3. Struttura dati per il JSON (Impostata solo sulla ruota di BARI)
    nuovi_dati = {
        "ruota_base": "BARI",
        "ruota_recupero": "NESSUNA (Configurazione Concentrata)",
        "configurazione": "FISSO +31",
        "input_estrazione": primo_estratto_bari,
        "previsione": {
            "ambata": ambata,
            "ambi_secchi": ambi
        },
        "protocollo": {
            "colpo_attuale": 1,
            "stato": "STUDIO - NON GIOCARE",
            "prossima_estrazione": "06/10/2026"
        }
    }
    
    # 4. Scrittura fisica del file risultati_v4.json
    nome_file = "risultati_v4.json"
    with open(nome_file, "w", encoding="utf-8") as f:
        json.dump(nuovi_dati, f, indent=4, ensure_ascii=False)
        
    print(f"✅ File {nome_file} generato e aggiornato con successo solo su BARI!")

# Eseguiamo il calcolo con il 13 uscito stasera a Bari
if __name__ == "__main__":
    aggiorna_risultati_json(13)
