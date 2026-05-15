import json
import os

# CONFIGURAZIONE RUOTE (Nell'ordine corretto basato sulle correzioni precedenti)
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
        if not os.path.exists('estrazioni.json'):
            print("❌ Errore: estrazioni.json non trovato.")
            return
            
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-3:]
        
        risultati_finali = []

        for i, est in enumerate(reversed(ultime_3)):
            colpo = i + 1
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1, r2 = RUOTE[idx1], RUOTE[idx2]
                    
                    if r1 in est and r2 in est:
                        for pos in range(5):
                            n1 = est[r1][pos]
                            n2 = est[r2][pos]
                            dist = calcola_distanza(n1, n2)
                            
                            # TEST: Accettiamo tutte le distanze superiori a 10 per vedere se scrive il file!
                            if dist >= 10:
                                ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                risultati_finali.append({
                                    "ruota": r1,
                                    "partner": r2,
                                    "numeri": ambo,
                                    "score": 180 if dist == 45 else 172,
                                    "colpo": colpo,
                                    "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                                })

        # Salva nel file richiesto dall'Action
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ TEST COMPLETATO! Generato 'risultati_v4.json' con {len(risultati_finali)} condizioni.")

    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    elabora_v5_geometric()
