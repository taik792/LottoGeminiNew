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
    # Percorsi dei file (adatta se i tuoi file si chiamano diversamente)
    archivio_path = "estrazioni.json"
    output_path = "risultati_dashboard.json"
    
    if not os.path.exists(archivio_path):
        print(f"Errore: Il file {archivio_path} non esiste.")
        return

    with open(archivio_path, "r", encoding="utf-8") as f:
        estrazioni = json.load(f)
    
    # Prendiamo l'ultima estrazione inserita nello storico
    # (ordinato dal più vecchio al più recente)
    ultima_estrazione = estrazioni[-1]
    print(f"Elaborazione estrazione del: {ultima_estrazione.get('data', 'Data non disponibile')}")

    nuove_predizioni = []
    
    # --- ESEMPIO DI LOGICA DI CALCOLO GEOMETRICO / ISOTOPO ---
    # Sostituisci o integra questo ciclo con la tua reale logica di quadratura
    ruote = [r for r in ultima_estrazione.keys() if r not in ["data", "id", "concorso"]]
    
    for i in range(len(ruote)):
        for j in range(i + 1, len(ruote)):
            r1 = ruote[i]
            r2 = ruote[j]
            
            # Esegui qui i tuoi calcoli ciclometrici (esagoni, distanze, somme)
            # In questo esempio ipotizziamo di aver trovato una struttura valida:
            struttura_valida = True 
            
            if struttura_valida:
                pred = {}
                
                # CORREZIONE BUG: Assegnazione corretta dei colori dinamici
                pred["ruota1"] = r1
                pred["ruota2"] = r2
                pred["colore_r1"] = determina_colore_ruota(r1)
                pred["colore_r2"] = determina_colore_ruota(r2)
                
                # Numeri generati dal tuo algoritmo (es. ambo inserito nel cerchio)
                pred["numero1"] = 36
                pred["numero2"] = 51
                pred["accuratezza"] = "180%"
                
                nuove_predizioni.append(pred)
                
                # Limiti il tabellone alle prime 5 strutture più forti
                if len(nuove_predizioni) >= 5:
                    break
        if len(nuove_predizioni) >= 5:
            break

    # Struttura finale da passare alla dashboard index.html
    dashboard_data = {
        "nuove": nuove_predizioni,
        "colpo2": [], # Popola con lo storico dei colpi precedenti se necessario
        "colpo3": []
    }
    
    # Scrittura del file finale che legge la dashboard
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4, ensure_ascii=False)
    
    print(f"Calcolo completato con successo. File {output_path} aggiornato.")

if __name__ == "__main__":
    genera_results = genera_results() if 'genera_results' in locals() else genera_risultati()
