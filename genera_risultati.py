import json
import os
import datetime

def esegui_aggiornamento_laboratorio():
    file_estrazioni = "estrazioni.json"
    file_risultati = "risultati_v4.json"
    
    # 1. Controllo presenza file estrazioni
    if not os.path.exists(file_estrazioni):
        print(f"❌ ERRORE: Non trovo il file '{file_estrazioni}' nella cartella!")
        return
        
    # 2. Lettura dell'archivio estrazioni
    try:
        with open(file_estrazioni, "r", encoding="utf-8") as f:
            archivio = json.load(f)
    except Exception as e:
        print(f"❌ ERRORE nella lettura di {file_estrazioni}: {e}")
        return

    # 3. Estrazione dell'ultimo 1° estratto di BARI
    try:
        if isinstance(archivio, list):
            ultima_estrazione = archivio[-1]
        elif isinstance(archivio, dict):
            ultime_chiavi = sorted(list(archivio.keys()))
            ultima_estrazione = archivio[ultime_chiavi[-1]]
        else:
            raise ValueError("Formato struttura dati estrazioni non riconosciuto.")
            
        ruota_bari = ultima_estrazione.get("BARI") or ultima_estrazione.get("Bari") or ultima_estrazione.get("ruote", {}).get("BARI")
        
        if isinstance(ruota_bari, list):
            primo_estratto_bari = int(ruota_bari[0])
        else:
            str_numeri = str(ruota_bari).replace(",", " ").split()
            primo_estratto_bari = int(str_numeri[0])
            
    except Exception as e:
        print(f"❌ ERRORE nell'estrarre l'ultimo numero di Bari da {file_estrazioni}: {e}")
        print("Uso l'input manuale d'emergenza dell'ultima estrazione (13) per non bloccare il sistema.")
        primo_estratto_bari = 13

    # 4. Applicazione Algoritmo Regina Concentrato (Fisso +31)
    ambata = primo_estratto_bari + 31
    if ambata > 90:
        ambata -= 90
        
    passi = [9, 20, 74]
    ambi = []
    for p in passi:
        abbinamento = ambata + p
        if abbinamento > 90:
            abbinamento -= 90
        if abbinamento == ambata:
            abbinamento = (abbinamento + 1) if abbinamento < 90 else 1
        ambi.append(f"{ambata}-{abbinamento}")
        
    # 5. Generazione della nuova struttura per risultati_v4.json
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
    
    # 6. Scrittura fisica del file risultati_v4.json
    try:
        with open(file_risultati, "w", encoding="utf-8") as f:
            json.dump(nuovi_dati, f, indent=4, ensure_ascii=False)
        print(f"✅ SUCCESSO: {file_estrazioni} letto. {file_risultati} generato correttamente!")
        print(f"   Input Bari: {primo_estratto_bari} -> Nuova Ambata: {ambata}")
    except Exception as e:
        print(f"❌ ERRORE nella scrittura di {file_risultati}: {e}")

if __name__ == "__main__":
    esegui_aggiornamento_laboratorio()
