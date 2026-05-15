import json
import os

# CONFIGURAZIONE
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Memoria delle ultime 3 estrazioni

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def elabora_v5_geometric():
    try:
        # Caricamento estrazioni
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
            # Gestione struttura: se è un dizionario prendiamo i valori, altrimenti è già una lista
            estrazioni = list(database.values()) if isinstance(database, dict) else database
    except:
        print("Errore: estrazioni.json non trovato o corrotto.")
        return

    risultati_v5 = []
    
    # Analizziamo le ultime 3 estrazioni per mantenere la memoria
    target_estrazioni = estrazioni[-CO_BACK:]
    
    for i, estrazione in enumerate(reversed(target_estrazioni)):
        colpo = i + 1
        data_estr = estrazione.get('data', 'N.D.')
        
        for idx1 in range(len(RUOTE)):
            for idx2 in range(idx1 + 1, len(RUOTE)):
                r1, r2 = RUOTE[idx1], RUOTE[idx2]
                
                # Verifichiamo che le ruote esistano nell'estrazione
                if r1 in estrazione and r2 in estrazione:
                    est1, est2 = estrazione[r1], estrazione[r2]
                    
                    for pos in range(5):
                        n1, n2 = est1[pos], est2[pos]
                        dist = calcola_distanza(n1, n2)
                        
                        # Se troviamo distanza 45 o 30 (simmetria isotopa)
                        if dist == 45 or dist == 30:
                            score = 180 if dist == 45 else 172
                            
                            # Calcolo previsione geometrica
                            ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                            
                            risultati_v5.append({
                                "ruota": r1,
                                "partner": r2,
                                "numeri": ambo,
                                "score": score,
                                "colpo": colpo,
                                "info": f"Nata il {data_estr} - Colpo {colpo}"
                            })

    # Salvataggio file per il sito (ordiniamo per colpo e poi per score)
    risultati_v5.sort(key=lambda x: (x['colpo'], -x['score']))
    
    with open('risultati.json', 'w', encoding='utf-8') as f:
        json.dump(risultati_v5, f, indent=4)
    
    print(f"✅ Analisi V5 completata con memoria ({len(risultati_v5)} previsioni).")

if __name__ == "__main__":
    elabora_v5_geometric()
