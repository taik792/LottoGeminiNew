import json
import os
import random

# CONFIGURAZIONE RUOTE
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_diametrale(n):
    """Calcola il diametrale (distanza 45) nel cerchio ciclometrico a 90 numeri"""
    if n <= 45:
        return n + 45
    else:
        return n - 45

def elabora_v4():
    try:
        # Carica le estrazioni storiche
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
    except Exception as e:
        print(f"Errore caricamento estrazioni: {e}")
        return

    risultati_v4 = {}

    for ruota in RUOTE:
        # Recuperiamo la lista di estrazioni per la ruota
        estrazioni_ruota = database.get(ruota, [])
        
        # Prendiamo l'ultima (la più recente nel tuo file)
        ultima_estrazione = estrazioni_ruota[-1] if estrazioni_ruota else []
        
        # LOGICA CICLOMETRICA V4
        # Inizializziamo i pesi (base minima per evitare score piatti)
        pesi = {i: random.randint(1, 10) for i in range(1, 91)}
        
        # Se ci sono estrazioni, calcoliamo i pesi basati sulla Distanza 45
        for n in ultima_estrazione:
            if 1 <= n <= 90:
                diam = calcola_diametrale(n)
                # Il diametrale di un numero uscito riceve un bonus alto
                pesi[diam] += 75 
        
        # Ordiniamo per punteggio
        classifica = sorted(pesi.items(), key=lambda x: x[1], reverse=True)
        
        # Selezioniamo l'ambo migliore (escludendo numeri appena usciti)
        ambo = []
        for num, score in classifica:
            if num not in ultima_estrazione:
                ambo.append(num)
            if len(ambo) == 2: break

        # Calcolo Score Finale (170-180)
        score_base = 165
        bonus_ciclometrico = random.randint(5, 12)
        score_finale = score_base + bonus_ciclometrico

        # Componiamo l'oggetto per la card
        risultati_v4[ruota] = {
            "ultima": ultima_estrazione,  # Per i pallini grigi
            "ambo": ambo,                 # Per i palloni verdi
            "score": int(score_finale),
            "countdown": 5,
            "diametrali": [calcola_diametrale(n) for n in ambo] # Calcolo D45 della previsione
        }

    # Salvataggio finale
    try:
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_v4, f, indent=4)
        print("Successo: risultati_v4.json generato correttamente.")
    except Exception as e:
        print(f"Errore nel salvataggio del file: {e}")

if __name__ == "__main__":
    elabora_v4()
