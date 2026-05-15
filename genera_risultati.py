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

def elabora_v5_geometric():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
            # Forza il database a essere una lista di estrazioni
            estrazioni = list(database.values()) if isinstance(database, dict) else database
    except Exception as e:
        print(f"Errore caricamento: {e}")
        return

    risultati_v5 = []
    # Analizza le ultime estrazioni disponibili
    target_estrazioni = estrazioni[-CO_BACK:]
    
    for i, estrazione in enumerate(reversed(target_estrazioni)):
        colpo = i + 1
        
        # CORREZIONE ERRORE 'LIST': 
        # Se l'estrazione è una lista, non ha il campo 'data', quindi usiamo un segnaposto
        data_estr = estrazione.get('data', 'N.D.') if isinstance(estrazione, dict) else f"Estrazione -{i}"
        
        for idx1 in range(len(RUOTE)):
            for idx2 in range(idx1 + 1, len(RUOTE)):
                r1, r2 = RUOTE[idx1], RUOTE[idx2]
                
                # Accedi ai dati in modo sicuro sia che sia Dizionario che Lista
                if isinstance(estrazione, dict) and r1 in estrazione and r2 in estrazione:
                    est1, est2 = estrazione[r1], estrazione[r2]
                elif isinstance(estrazione, list):
                    # Se è una lista, saltiamo l'analisi perché mancano le etichette delle ruote
                    continue
                else:
                    continue
                
                for pos in range(5):
                    n1, n2 = est1[pos], est2[pos]
                    dist = calcola_distanza(n1, n2)
                    
                    if dist == 45 or dist == 30:
                        score = 180 if dist == 45 else 172
                        ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                        
                        risultati_v5.append({
                            "ruota": r1,
                            "partner": r2,
                            "numeri": ambo,
                            "score": score,
                            "colpo": colpo,
                            "info": f"{data_estr} - Colpo {colpo}"
                        })

    # Ordina: prima i nuovi (Colpo 1), poi per Score
    risultati_v5.sort(key=lambda x: (x['colpo'], -x['score']))
    
    with open('risultati.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_v5, f, indent=4)
    
    print(f"✅ V5 completata! Previsioni generate: {len(risultati_v5)}")

if __name__ == "__main__":
    elabora_v5_geometric()
