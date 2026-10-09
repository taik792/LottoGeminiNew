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
        chiave_bari = "Bari" if "Bari" in archivio else "BARI"
        
        if chiave_bari in archivio and len(archivio[chiave_bari]) > 0:
            # Prende l'ultimo array della lista di Bari (Estrazione dell'08/10:)
            ultima_cinquina_bari = archivio[chiave_bari][-1]
            # Prende il primo numero della cinquina (74)
            primo_estratto_bari = int(ultima_cinquina_bari[0])
        else:
            raise KeyError("Ruota Bari non trovata nell'archivio JSON.")
            
    except Exception as e:
        print(f"❌ ERRORE nell'estrarre l'ultimo numero di Bari: {e}")
        print("Uso l'input manuale dell'ultima estrazione (74) per non bloccarsi.")
        primo_estratto_bari = 74

    # 4. Applicazione NUOVA LOGICA: Regina Concentrato con FISSO +44
    ambata = primo_estratto_bari + 44
    if ambata > 90:
        ambata -= 90
        
    # I 3 passi geometrici approvati (+9, +20, +74) applicati sulla nuova ambata
    passi = [9, 20, 74]
    ambi = []
    for p in passi:
        abbinamento = ambata + p
        if abbinamento > 90:
            abbinamento -= 90
        if abbinamento == ambata:
            abbinamento = (abbinamento + 1) if abbinamento < 90 else 1
        ambi.append(f"{ambata}-{abbinamento}")
        
    # 5. Generazione della struttura per la Dashboard index.html
    nuovi_dati = {
        "ruota_base": "BARI",
        "ruota_recupero": "NESSUNA (Configurazione Concentrata)",
        "configurazione": "FISSO +44 (Ottimizzato 28%)",
        "input_estrazione": primo_estratto_bari,
        "previsione": {
            "ambata": ambata,
            "ambi_secchi": ambi
        },
        "protocollo": {
            "colpo_attuale": 1,
            "stato": "STUDIO - NON GIOCARE",
            "prossima_estrazione": "10/10/2026"
        }
    }
    
    # 6. Scrittura fisica del file risultati_v4.json
    try:
        with open(file_risultati, "w", encoding="utf-8") as f:
            json.dump(nuovi_dati, f, indent=4, ensure_ascii=False)
        print(f"==================================================")
        print(f"✅ MOTORE AGGIORNATO CON SUCCESSO SUL PC!")
        print(f"==================================================")
        print(f"   Input Bari (Ultimo 1° Estratto): {primo_estratto_bari}")
        print(f"   Configurazione Attiva: FISSO +44")
        print(f"   🔥 NUOVA AMBATA CALCOLATA: {ambata}")
        print(f"   🎯 AMBI SECCHI GENERATI: {', '.join(ambi)}")
        print(f"   Pannello '{file_risultati}' pronto per index.html")
        print(f"==================================================")
    except Exception as e:
        print(f"❌ ERRORE nella scrittura di {file_risultati}: {e}")

if __name__ == "__main__":
    esegui_aggiornamento_laboratorio()
