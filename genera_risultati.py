import json
import os
import random

# LOTTO ELITE PRO V4 - CYCLO EDITION (D45)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_diametrale(n):
    """Calcola il diametrale (distanza 45) nel cerchio a 90 numeri"""
    if n <= 45:
        return n + 45
    else:
        return n - 45

def elabora_v4():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            estrazioni = json.load(f)
    except:
        print("Errore: estrazioni.json non trovato.")
        return

    risultati_v4 = {}

    for ruota in RUOTE:
        ultimi_usciti = estrazioni.get(ruota, [[]])[-1]
        
        # Logica Ciclometrica: pesiamo i numeri e i loro diametrali
        pesi = {i: random.randint(1, 15) for i in range(1, 91)}
        
        for n in ultimi_usciti:
            if 1 <= n <= 90:
                # Il numero uscito "chiama" il suo diametrale
                diam = calcola_diametrale(n)
                pesi[diam] += 60 
        
        classifica = sorted(pesi.items(), key=lambda x: x[1], reverse=True)
        
        ambo = []
        for num, score in classifica:
            if num not in ultimi_usciti and num > 2:
                ambo.append(num)
            if len(ambo) == 2: break

        # Calcolo Score Ciclometrico
        distanza = abs(ambo[0] - ambo[1])
        bonus_distanza = 20 if distanza == 45 or distanza == 30 else 0
        score_finale = 165 + (sum(pesi[n] for n in ambo) // 5) + bonus_distanza

        risultati_v4[ruota] = {
            "ambo": ambo,
            "score": int(score_finale),
            "countdown": 5,
            "diametrali": [calcola_diametrale(n) for n in ambo],
            "tipo": "Ciclometrica D45"
        }

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_v4, f, indent=4)
    print("V4: Analisi Ciclometrica completata e salvata in risultati_v4.json")

if __name__ == "__main__":
    elabora_v4()
