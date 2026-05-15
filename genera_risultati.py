import json

# CONFIGURAZIONE RUOTE (Assicurati che l'ordine sia quello corretto per il tuo script)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def genera_risultati():
    try:
        # 1. Carica il file estrazioni.json
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        # 2. Ordina le chiavi numeriche (es. "790", "791", "792")
        # Filtriamo solo le chiavi che sono effettivamente numeri per evitare errori
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        # Trasformiamo in lista per prendere le ultime 3 estrazioni
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-3:]
        
        risultati_finali = []

        # 3. Analisi dalla più recente (Colpo 1) alla meno recente (Colpo 3)
        for i, est in enumerate(reversed(ultime_3)):
            colpo = i + 1
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1, r2 = RUOTE[idx1], RUOTE[idx2]
                    
                    if r1 in est and r2 in est:
                        numeri1 = est[r1]
                        numeri2 = est[r2]
                        
                        for pos in range(5):
                            n1, n2 = numeri1[pos], numeri2[pos]
                            dist = calcola_distanza(n1, n2)
                            
                            # Logica Geometric Mirror: Distanza 45 o 30
                            if dist == 45 or dist == 30:
                                ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                risultati_finali.append({
                                    "ruota": r1,
                                    "partner": r2,
                                    "numeri": ambo,
                                    "score": 180 if dist == 45 else 172,
                                    "colpo": colpo,
                                    "info": f"Memoria: Colpo {colpo}"
                                })

        # 4. Scrittura del file risultati.json per il sito
        with open('risultati.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Analisi completata con successo! Generate {len(risultati_finali)} previsioni.")

    except Exception as e:
        print(f"❌ Errore critico: {e}")

if __name__ == "__main__":
    genera_risultati()
