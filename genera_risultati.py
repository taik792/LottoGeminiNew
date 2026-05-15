import json
import os

# CONFIGURAZIONE
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3 

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def elabora_v5():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
            # Gestione formati diversi del database
            estrazioni = list(db.values()) if isinstance(db, dict) else db
    except:
        print("Errore: estrazioni.json non trovato")
        return

    risultati = []
    # Analizza le ultime 3 estrazioni per la memoria
    per_analisi = estrazioni[-CO_BACK:]
    
    for i, est in enumerate(reversed(per_analisi)):
        colpo = i + 1
        # Se l'estrazione è una lista (senza nomi ruote), usiamo gli indici
        for idx1 in range(len(RUOTE)):
            for idx2 in range(idx1 + 1, len(RUOTE)):
                r1, r2 = RUOTE[idx1], RUOTE[idx2]
                
                try:
                    # Tenta di leggere come dizionario, altrimenti usa l'indice della lista
                    numeri1 = est.get(r1) if isinstance(est, dict) else est[idx1]
                    numeri2 = est.get(r2) if isinstance(est, dict) else est[idx2]
                    
                    if numeri1 and numeri2:
                        for pos in range(5):
                            n1, n2 = numeri1[pos], numeri2[pos]
                            dist = calcola_distanza(n1, n2)
                            
                            if dist == 45 or dist == 30:
                                ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                risultati.append({
                                    "ruota": r1,
                                    "partner": r2,
                                    "numeri": ambo,
                                    "score": 180 if dist == 45 else 172,
                                    "colpo": colpo,
                                    "info": f"Memoria: Colpo {colpo}"
                                })
                except:
                    continue

    # Salvataggio col nome corretto cercato dal sito
    with open('risultati.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, indent=4)
    
    print(f"✅ Creato risultati.json con {len(risultati)} previsioni.")

if __name__ == "__main__":
    elabora_v5()
