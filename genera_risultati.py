import json

# --- CONFIGURAZIONE ---
CO_BACK = 3  # Quante estrazioni passate analizzare (memoria)

def calcola_ambo(a, b):
    somma = (a + b)
    while somma > 90: somma -= 90
    diff = abs(a - b)
    if diff == 0: diff = 90
    return [somma, diff]

def genera_risultati():
    # 1. Carica le estrazioni
    with open('estrazioni.json', 'r') as f:
        storico = json.load(f)
    
    # 2. Prendi le ultime X estrazioni
    ultime_estrazioni = storico[-CO_BACK:]
    tutte_le_previsioni = []
    
    # 3. Ciclo di analisi (dal più recente al meno recente)
    for i, estrazione in enumerate(reversed(ultime_estrazioni)):
        colpo = i + 1
        data_estr = estrazione.get('data', 'N.D.')
        
        ruote = [r for r in estrazione.keys() if r != 'data']
        
        for idx1 in range(len(ruote)):
            for idx2 in range(idx1 + 1, len(ruote)):
                r1, r2 = ruote[idx1], ruote[idx2]
                
                for pos in range(5):
                    n1 = estrazione[r1][pos]
                    n2 = estrazione[r2][pos]
                    
                    # Calcolo Distanza Ciclometrica
                    dist = abs(n1 - n2)
                    if dist > 45: dist = 90 - dist
                    
                    if dist == 45 or dist == 30:
                        ambo = calcola_ambo(n1, n2)
                        score = 180 if dist == 45 else 172
                        
                        tutte_le_previsioni.append({
                            "ruota": r1,
                            "partner": r2,
                            "numeri": ambo,
                            "score": score,
                            "colpo": colpo,
                            "info": f"Nata il {data_estr} - Colpo {colpo}"
                        })

    # 4. Salva il file per il sito
    with open('risultati.json', 'w') as f:
        json.dump(tutte_le_previsioni, f, indent=4)
    
    print(f"✅ Analisi completata! Generate {len(tutte_le_previsioni)} previsioni con memoria.")

if __name__ == "__main__":
    genera_risultati()
