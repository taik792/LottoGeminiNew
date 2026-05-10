import json
import random

# CONFIGURAZIONE V4 - CYCLO D45
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_diametrale(n):
    return n + 45 if n <= 45 else n - 45

def genera_v4():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
    except Exception as e:
        print(f"Errore caricamento dati: {e}")
        return

    risultati_finali = {}

    for ruota in RUOTE:
        # Recupero ultimi 5 numeri estratti
        storico_ruota = database.get(ruota, [])
        ultimi_numeri = storico_ruota[-1] if storico_ruota else []
        
        # Calcolo Score basato su spie ciclometriche
        pesi = {i: random.randint(1, 20) for i in range(1, 91)}
        for n in ultimi_numeri:
            diam = calcola_diametrale(n)
            pesi[diam] += 70 # Bonus forte per la chiusura del diametrale
            
        # Selezione Ambo (escludendo gli appena usciti)
        classifica = sorted(pesi.items(), key=lambda x: x[1], reverse=True)
        ambo = []
        for num, score in classifica:
            if num not in ultimi_numeri:
                ambo.append(num)
            if len(ambo) == 2: break
            
        # Salvataggio dati ruota
        risultati_finali[ruota] = {
            "ultima": ultimi_numeri,
            "ambo": ambo,
            "diametrali": [calcola_diametrale(n) for n in ambo],
            "score": 160 + (sum(pesi[n] for n in ambo) // 10),
            "countdown": 5
        }

    # Salvataggio nel file V4
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4)
    print("File risultati_v4.json generato con successo!")

if __name__ == "__main__":
    genera_v4()
