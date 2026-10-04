import json
import os
import datetime

def esegui_aggiornamento_laboratorio():
    file_estrazioni = "estrazioni.json"
    file_risultati = "resultados_v4.json" # se la tua index cerca risultati_v4.json rinominalo di conseguenza
    
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

    # 3. Estrazione dell'ultimo 1° estratto di BARI secondo la tua struttura
    try:
        # Nella tua struttura le chiavi hanno la prima lettera maiuscola ("Bari")
        chiave_bari = "Bari" if "Bari" in archivio else "BARI"
        
        if chiave_bari in archivio and len(archivio[chiave_bari]) > 0:
            # Prende l'ultimo array della lista di Bari
            ultima_cinquina_bari = archivio[chiave_bari][-1]
            # Prende il primo elemento dell'array (il 1° estratto)
            primo_estratto_bari = int(ultima_cinquina_bari[0])
        else:
            raise KeyError("Ruota Bari non trovata nell'archivio JSON.")
            
    except Exception as e:
        print(f"❌ ERRORE nell'estrarre l'ultimo numero di Bari: {e}")
        print("Uso l'input manuale d'emergenza (13) per non bloccare la dashboard.")
        primo_estratto_bari = 13

    # 4. Applicazione Algoritmo Regina Concentrato (Fisso +31)
    ambata = primo_estratto_bari + 31
    if ambata > 90:
        ambata -= 90
        
    # I 3 passi calcolati dall'ottimizzatore brute-force su Bari
    passi = [9, 20, 74]
    ambi = []
    for p in passi:
        abbinamento = ambata + p
        if abbinamento > 90:
            abbinamento -= 90
        if abbinamento == ambata:
            abbinamento = (abbinamento + 1) if abbinamento < 90 else 1
        ambi.append(f"{ambata}-{abbinamento}")
        
    # 5. Generazione della nuova struttura per la Dashboard index.html
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
    # NOTA: se nel codice javascript della tua index.html hai scritto "risultati_v4.json", 
    # assicurati che il nome qui sotto corrisponda perfettamente (controlla se c'è la 'v' o se è risultati_v4)
    file_output = "risultati_v4.json" 
    
    try:
        with open(file_output, "w", encoding="utf-8") as f:
            json.dump(nuovi_dati, f, indent=4, ensure_ascii=False)
        print(f"✅ SUCCESSO: '{file_estrazioni}' letto correttamente.")
        print(f"   Ultimo 1° Estratto Bari rilevato: {primo_estratto_bari}")
        print(f"   File '{file_output}' rigenerato con la nuova logica Regina Concentrato!")
    except Exception as e:
        print(f"❌ ERRORE nella scrittura del file di output: {e}")

if __name__ == "__main__":
    esegui_aggiornamento_laboratorio()
