import json
import os

def genera_risultati():
    # 1. Carica il file delle estrazioni storiche
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato!")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        estrazioni = json.load(f)
    
    # 2. Struttura base del file di output per la dashboard
    risultati = {
        "nuove": [],
        "colpo2": []
    }
    
    # Definizione dei gruppi di ruote per i colori della mappa
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    # Verifichiamo che ci siano dati all'interno del file
    if not estrazioni or not isinstance(estrazioni, dict):
        print("Errore: Formato estrazioni.json non valido.")
        return

    print("Elaborazione estrazioni completata con successo.")
    
    # 3. ESEMPIO DI LOGICA DI GENERAZIONE PREVISIONI (Adattala alla tua ciclometria)
    # Prendiamo le ruote disponibili nel JSON
    lista_ruote = list(estrazioni.keys())
    
    # Generiamo delle previsioni fittizie basate sulle ultime estrazioni reali per testare il funzionamento
    if len(lista_ruote) >= 2:
        # Previsione 1 (Nuove)
        r1, r2 = "Bari", "Torino"
        # Accediamo all'ultima estrazione (indice -1 della lista di quella ruota)
        num1 = estrazioni[r1][-1][0] if len(estrazioni[r1]) > 0 else 12
        num2 = estrazioni[r2][-1][1] if len(estrazioni[r2]) > 0 else 45
        
        colore_r1 = "red" if r1 in ruote_rosse else ("gray" if r1 in ruote_grigie else "yellow")
        colore_r2 = "red" if r2 in ruote_rosse else ("gray" if r2 in ruote_grigie else "yellow")
        
        risultati["nuove"].append({
            "ruote": f"{r1} - {r2}",
            "numeri": [num1, num2],
            "budget": "4.00€",
            "accuratezza": "165%",
            "colore_r1": colore_r1,
            "colore_r2": colore_r2
        })
        
        # Previsione 2 (Colpo 2)
        r3, r4 = "Milano", "Roma"
        num3 = estrazioni[r3][-1][2] if len(estrazioni[r3]) > 0 else 23
        num4 = estrazioni[r4][-1][3] if len(estrazioni[r4]) > 0 else 67
        
        colore_r3 = "red" if r3 in ruote_rosse else ("gray" if r3 in ruote_grigie else "yellow")
        colore_r4 = "red" if r4 in ruote_rosse else ("gray" if r4 in ruote_grigie else "yellow")
        
        risultati["colpo2"].append({
            "ruote": f"{r3} - {r4}",
            "numeri": [num3, num4],
            "budget": "4.00€",
            "accuratezza": "170%",
            "colore_r1": colore_r3,
            "colore_r2": colore_r4
        })

    # 4. Salva il file dei risultati per la dashboard
    with open('risultati_dashboard.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    print("File risultati_dashboard.json generato correttamente.")

if __name__ == "__main__":
    genera_risultati()
