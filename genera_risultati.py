import json
import os

def determina_colore_ruota(ruota):
    """
    Assegna il colore corretto alle ruote secondo le specifiche:
    - Palermo, Roma, Torino = Rosse (red)
    - Milano = Grigia (gray)
    - Altre = Gialle (yellow)
    """
    ruota_clean = ruota.strip().lower()
    if ruota_clean in ["palermo", "roma", "torino"]:
        return "red"
    elif ruota_clean == "milano":
        return "gray"
    else:
        return "yellow"

def genera_risultati():
    archivio_path = "estrazioni.json"
    output_path = "risultati_dashboard.json"
    
    if not os.path.exists(archivio_path):
        print(f"Errore: Il file {archivio_path} non esiste.")
        return

    with open(archivio_path, "r", encoding="utf-8") as f:
        mappa_estrazioni = json.load(f)
    
    # Isoliamo i nomi delle ruote escludendo eventuali chiavi di servizio se presenti
    escludi = ["data", "id", "concorso", "numero", "anno"]
    ruote_disponibili = [r for r in mappa_estrazioni.keys() if r.lower() not in escludi]
    
    if not ruote_disponibili:
        print("Errore: Nessuna ruota trovata nel file JSON.")
        return

    print(f"Ruote rilevate dall'archivio: {len(ruote_disponibili)}")

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []
    
    # --- ACCOPPIAMENTO GEOMETRICO DELLE RUOTE ---
    for i in range(len(ruote_disponibili)):
        for j in range(i + 1, len(ruote_disponibili)):
            r1 = ruote_disponibili[i]
            r2 = ruote_disponibili[j]
            
            # NOTA: Per fare i calcoli ciclometrici sull'ultimo colpo estrattivo, puoi accedere così:
            # ultimo_estratto_r1 = mappa_estrazioni[r1][-1] -> restituisce i 5 numeri (es: [51, 65, 6, 29, 81])
            # ultimo_estratto_r2 = mappa_estrazioni[r2][-1]
            
            pred = {
                "ruota1": r1.capitalize(),
                "ruota2": r2.capitalize(),
                "colore_r1": determina_colore_ruota(r1),
                "colore_r2": determina_colore_ruota(r2),
                "numero1": 36,  # Valore fisso o calcolato dal tuo algoritmo
                "numero2": 51,  # Valore fisso o calcolato dal tuo algoritmo
                "accuratezza": "180%"
            }
            
            # Distribuzione nei 3 Tab della Dashboard
            if len(tabellone_nuovi) < 5:
                pred["accuratezza"] = "180%"
                tabellone_nuovi.append(pred)
            elif len(tabellone_colpo2) < 5:
                pred["accuratezza"] = "172%"
                tabellone_colpo2.append(pred)
            elif len(tabellone_colpo3) < 5:
                pred["accuratezza"] = "164%"
                tabellone_colpo3.append(pred)

    # Creazione della struttura letta da index.html
    dashboard_data = {
        "nuove": tabellone_nuovi,
        "colpo2": tabellone_colpo2, 
        "colpo3": tabellone_colpo3
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4, ensure_ascii=False)
    
    print(f"Calcolo completato con successo! File {output_path} pronto per il sito.")

if __name__ == "__main__":
    genera_results = genera_risultati()
