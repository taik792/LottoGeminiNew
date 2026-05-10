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

def elabora_v5_geometric():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            estrazioni = json.load(f)
    except:
        print("Errore: estrazioni.json non trovato.")
        return

    risultati_v5 = {}
    
    # 1. Analizziamo le estrazioni recenti (ultime due)
    # Cerchiamo armonie geometriche tra coppie di ruote
    for i in range(len(RUOTE)):
        for j in range(i + 1, len(RUOTE)):
            r1, r2 = RUOTE[i], RUOTE[j]
            est1 = estrazioni.get(r1, [[]])[-1]
            est2 = estrazioni.get(r2, [[]])[-1]
            
            # Cerchiamo isotopi (stessa posizione) con distanza 45 o 30
            for pos in range(5):
                n1 = est1[pos]
                n2 = est2[pos]
                dist = calcola_distanza(n1, n2)
                
                if dist == 45 or dist == 30:
                    # Abbiamo trovato una condizione geometrica!
                    # Calcoliamo la "Chiusura del Quadrato"
                    ambo_base = [fuori_90(n1 + n2), fuori_90(abs(n1 - n2))]
                    
                    # Evitiamo numeri doppi o 0
                    if ambo_base[0] == ambo_base[1]: ambo_base[1] = fuori_90(ambo_base[1] + 1)
                    
                    score = 180 if dist == 45 else 172
                    
                    # Salviamo per entrambe le ruote interessate
                    for r in [r1, r2]:
                        if r not in risultati_v5 or score > risultati_v5[r]["score"]:
                            risultati_v5[r] = {
                                "ultima": est1 if r == r1 else est2,
                                "ambo": ambo_base,
                                "score": score,
                                "countdown": 6,
                                "tecnica": f"Geometric Mirror (Pos {pos+1})",
                                "partner": r2 if r == r1 else r1
                            }

    # Riempire le ruote mancanti con logica standard se non trovano specchi
    for r in RUOTE:
        if r not in risultati_v5:
            est = estrazioni.get(r, [[]])[-1]
            risultati_v5[r] = {
                "ultima": est,
                "ambo": [fuori_90(est[0]+est[1]), fuori_90(abs(est[0]-est[1]))],
                "score": 150,
                "countdown": 6,
                "tecnica": "Analisi Standard",
                "partner": "Nessuno"
            }

    with open('risultati_v5.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_v5, f, indent=4)
    print("V5: Motore Geometrico completato.")

if __name__ == "__main__":
    elabora_v5_geometric()
