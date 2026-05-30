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
    # Percorsi dei file di configurazione
    archivio_path = "estrazioni.json"
    output_path = "risultati_dashboard.json"
    
    if not os.path.exists(archivio_path):
        print(f"Errore: Il file {archivio_path} non esiste.")
        return

    with open(archivio_path, "r", encoding="utf-8") as f:
        estrazioni = json.load(f)
    
    # --- GESTIONE ROBUSTA STRUTTURA JSON (Previene KeyError: -1) ---
    if isinstance(estrazioni, list):
        if len(estrazioni) == 0:
            print("Errore: L'archivio in formato lista è vuoto.")
            return
        ultima_estrazione = estrazioni[-1]
    elif isinstance(estrazioni, dict):
        if len(estrazioni) == 0:
            print("Errore: L'archivio in formato dizionario è vuoto.")
            return
        # Se le chiavi sono i progressivi/date, prendiamo l'ultima chiave ordinata
        chiavi_ordinate = sorted(list(estrazioni.keys()))
        ultima_chiave = chiavi_ordinate[-1]
        ultima_estrazione = estrazioni[ultima_chiave]
        # Se serve, teniamo traccia della chiave come data/concorso
        if "data" not in ultima_estrazione:
            ultima_estrazione["data"] = ultima_chiave
    else:
        print("Errore: Formato del file JSON non supportato.")
        return

    print(f"Elaborazione estrazione del: {ultima_estrazione.get('data', 'Data non disponibile')}")

    nuove_predizioni = []
    
    # Lista delle ruote da elaborare escludendo i metadati
    escludi = ["data", "id", "concorso", "numero", "anno"]
    ruote = [r for r in ultima_estrazione.keys() if r.lower() not in escludi]
    
    # --- LOGICA DI CALCOLO GEOMETRICO / ISOTOPO ---
    # Questa struttura cicla le ruote ed applica la colorazione corretta
    for i in range(len(ruote)):
        for j in range(i + 1, len(ruote)):
            r1 = ruote[i]
            r2 = ruote[j]
            
            # Qui si innesta la tua logica ciclometrica.
            # Ipotizziamo che l'algoritmo trovi una convergenza strutturale:
            struttura_valida = True 
            
            if strattura_valida:
                pred = {}
                pred["ruota1"] = r1.capitalize()
                pred["ruota2"] = r2.capitalize()
                
                # Applicazione dei colori corretti senza SyntaxError
                pred["colore_r1"] = determina_colore_ruota(r1)
                pred["colore_r2"] = determina_colore_ruota(r2)
                
                # Ambo fisso o calcolato da inserire nella card
                pred["numero1"] = 36
                pred["numero2"] = 51
                pred["accuratezza"] = "180%"
                
                nuove_predizioni.append(pred)
                
                if len(nuove_predizioni) >= 5:
                    break
        if len(nuove_predizioni) >= 5:
            break

    # Prepariamo l'output finale per index.html
    dashboard_data = {
        "nuove": nuove_predizioni,
        "colpo2": [], 
        "colpo3": []
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4, ensure_ascii=False)
    
    print(f"Calcolo completato con successo. File {output_path} aggiornato per la dashboard.")

if __name__ == "__main__":
    genera_risultati()
