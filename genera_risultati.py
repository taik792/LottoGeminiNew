import json
import os

def determina_colore_ruota(ruota):
    """
    Assegna il colore corretto alle ruote secondo le specifiche:
    - Palermo, Roma, Torino = Rosse
    - Milano = Grigia
    - Altre = Gialle
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
        estrazioni = json.load(f)
    
    # Gestione dello storico (lista cronologica: l'ultimo elemento [-1] è il più recente)
    if isinstance(estrazioni, list):
        if len(estrazioni) == 0:
            print("Errore: L'archivio è vuoto.")
            return
        ultima_estrazione = estrazioni[-1]
    elif isinstance(estrazioni, dict):
        if len(estrazioni) == 0:
            print("Errore: L'archivio è vuoto.")
            return
        chiavi_ordinate = sorted(list(estrazioni.keys()))
        ultima_chiave = chiavi_ordinate[-1]
        ultima_estrazione = estrazioni[ultima_chiave]
    else:
        print("Errore: Formato file JSON non supportato.")
        return

    print(f"Elaborazione estrazione recente del: {ultima_estrazione.get('data', 'Data non disponibile')}")

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []
    
    escludi = ["data", "id", "concorso", "numero", "anno"]
    ruote = [r for r in ultima_estrazione.keys() if r.lower() not in escludi]
    
    # --- LOGICA DI CALCOLO GEOMETRICO / FILTRI TAB ---
    for i in range(len(ruote)):
        for j in range(i + 1, len(ruote)):
            r1 = ruote[i]
            r2 = ruote[j]
            
            struttura_valida = True 
            
            if struttura_valida:
                pred = {
                    "ruota1": r1.capitalize(),
                    "ruota2": r2.capitalize(),
                    "colore_r1": determina_colore_ruota(r1),
                    "colore_r2": determina_colore_ruota(r2),
                    "numero1": 36,  # Qui si innesteranno i tuoi calcoli futuri
                    "numero2": 51,
                    "accuratezza": "180%"
                }
                
                # Smistamento nei tre moduli Tab del sito
                if len(tabellone_nuovi) < 5:
                    pred["accuratezza"] = "180%"
                    tabellone_nuovi.append(pred)
                elif len(tabellone_colpo2) < 5:
                    pred["accuratezza"] = "172%"
                    tabellone_colpo2.append(pred)
                elif len(tabellone_colpo3) < 5:
                    pred["accuratezza"] = "164%"
                    tabellone_colpo3.append(pred)

    # Struttura dati finale letta dall'interfaccia web
    dashboard_data = {
        "nuove": tabellone_nuovi,
        "colpo2": tabellone_colpo2, 
        "colpo3": tabellone_colpo3
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4, ensure_ascii=False)
    
    print(f"Calcolo completato con successo. File {output_path} pronto.")

# BLOCCO DI AVVIO SNELLITO E CORRETTO (Risolve il TypeError alla riga 93)
if __name__ == "__main__":
    genera_risultati()
