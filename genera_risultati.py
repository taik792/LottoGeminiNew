import json
import os
import random
from datetime import datetime

# LOTTO ELITE PRO V4 - CYCLO EDITION (D45)
# Rimosso riferimento alla Nazionale come richiesto
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_diametrale(n):
    """Calcola il diametrale (distanza 45) nel cerchio a 90 numeri"""
    if n <= 45:
        return n + 45
    else:
        return n - 45

def elabora_v4():
    try:
        # Legge lo storico delle estrazioni
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            estrazioni = json.load(f)
    except Exception as e:
        print(f"Errore caricamento estrazioni: {e}")
        return

    risultati_v4 = {}
    # Aggiungiamo un timestamp per tracciare l'aggiornamento nel JSON
    risultati_v4["ultimo_aggiornamento"] = datetime.now().isoformat()
    
    # Creiamo un contenitore per i dati delle ruote
    dati_ruote = {}

    for ruota in RUOTE:
        # Prende l'ultima estrazione disponibile per la ruota
        tutte_estrazioni = estrazioni.get(ruota, [])
        if not tutte_estrazioni:
            continue
            
        ultimi_usciti = tutte_estrazioni[-1]
        
        # LOGICA CICLOMETRICA: Assegnazione pesi base
        # Usiamo un range 1-20 per evitare stalli in classifica
        pesi = {i: random.randint(1, 20) for i in range(1, 91)}
        
        # I numeri usciti "chiamano" i loro diametrali per equilibrio
        for n in ultimi_usciti:
            if 1 <= n <= 90:
                diam = calcola_diametrale(n)
                pesi[diam] += 65 # Bonus pesante per la chiusura del cerchio
        
        # Ordina i numeri per peso dal più alto al più basso
        classifica = sorted(pesi.items(), key=lambda x: x[1], reverse=True)
        
        ambo = []
        for num, score in classifica:
            # Filtro anti-ripetizione: non rigiochiamo i numeri appena usciti
            if num not in ultimi_usciti:
                ambo.append(num)
            if len(ambo) == 2: 
                break

        # Calcolo Score Finale Dinamico
        # Base 160 + media pesi dei due numeri scelti
        score_base = 160 + (sum(pesi[n] for n in ambo) // 4)
        
        # Bonus Ciclometrico: se l'ambo stesso ha distanza 45, è una condizione perfetta
        distanza = abs(ambo[0] - ambo[1])
        if distanza == 45:
            score_base += 15

        dati_ruote[ruota] = {
            "ambo": ambo,
            "score": int(score_base),
            "countdown": 5,
            "diametrali": [calcola_diametrale(n) for n in ambo],
            "ultima_estrazione": ultimi_usciti
        }

    # Salvataggio finale: usiamo direttamente il dizionario per la compatibilità Web
    # NOTA: Se vuoi che il sito legga bene, salviamo dati_ruote direttamente
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(dati_ruote, f, indent=4)
        
    print("V4: Analisi completata con successo.")

if __name__ == "__main__":
    elabora_v4()
