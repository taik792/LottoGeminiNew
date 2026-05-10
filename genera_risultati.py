import json
import os

# CONFIGURAZIONE RUOTE
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def elabora_v4_geometric():
    try:
        # Carichiamo le estrazioni dal tuo file
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            estrazioni = json.load(f)
    except Exception as e:
        print(f"Errore caricamento: {e}")
        return

    risultati_v4 = {}
    
    # 1. Scansione Geometrica tra coppie di ruote (Simmetria Isotopa)
    for i in range(len(RUOTE)):
        for j in range(i + 1, len(RUOTE)):
            r1, r2 = RUOTE[i], RUOTE[j]
            # Prendiamo l'ultima estrazione di ogni ruota
            est1 = estrazioni.get(r1, [[]])[-1]
            est2 = estrazioni.get(r2, [[]])[-1]
            
            if not est1 or not est2: continue

            # Cerchiamo numeri nella stessa posizione con Distanza 45 o 30
            for pos in range(5):
                n1, n2 = est1[pos], est2[pos]
                dist = calcola_distanza(n1, n2)
                
                # Se troviamo una condizione ottimale (D45 o D30)
                if dist == 45 or dist == 30:
                    # Calcolo chiusura quadrato ciclometrico
                    ambo = [fuori_90(n1 + n2), fuori_90(abs(n1 - n2))]
                    if ambo[0] == ambo[1]: ambo[1] = fuori_90(ambo[1] + 1)
                    
                    # Score basato sulla forza della figura
                    score = 180 if dist == 45 else 172
                    
                    # Aggiorniamo i risultati per le due ruote coinvolte
                    for r in [r1, r2]:
                        if r not in risultati_v4 or score > risultati_v4[r]["score"]:
                            risultati_v4[r] = {
                                "ultima": est1 if r == r1 else est2,
                                "ambo": ambo,
                                "score": score,
                                "countdown": 5,
                                "tecnica": f"Geometric Mirror (Isotopia Pos {pos+1})",
                                "partner": r2 if r == r1 else r1,
                                "diametrali": [fuori_90(n + 45) for n in ambo]
                            }

    # 2. Riempimento ruote senza condizioni (Analisi Standard)
    for r in RUOTE:
        if r not in risultati_v4:
            est = estrazioni.get(r, [[]])[-1]
            # Calcolo standard basato sui primi due estratti
            ambo_std = [fuori_90(est[0]+est[1]), fuori_90(abs(est[0]-est[1]))]
            risultati_v4[r] = {
                "ultima": est,
                "ambo": ambo_std,
                "score": 150,
                "countdown": 5,
                "tecnica": "Analisi Lineare Standard",
                "partner": "Nessuno",
                "diametrali": [fuori_90(n + 45) for n in ambo_std]
            }

    # Salvataggio nel file che il sito già legge
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_v4, f, indent=4)
    print("V4 aggiornata con successo al motore Geometric Mirror.")

if __name__ == "__main__":
    elabora_v4_geometric()
