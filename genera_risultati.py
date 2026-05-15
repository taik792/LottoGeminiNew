import json
import os

RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def pulisci_numeri(valore):
    if isinstance(valore, list):
        try: return [int(n) for n in valore]
        except: return []
    if isinstance(valore, str):
        try:
            valore_pulito = valore.replace(" ", ".").replace("-", ".")
            parti = [p for p in valore_pulito.split(".") if p.strip().isdigit()]
            return [int(n) for n in parti]
        except: return []
    return []

def genera_risultati():
    try:
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        chiavi_tutte = list(dati_grezzi.keys())
        ultime_chiavi = chiavi_tutte[-CO_BACK:]
        
        # --- LOG DI CONTROLLO ---
        print("\n=== VERIFICA COSA LEGGE PYTHON ===")
        print(f"Chiavi totali nel file: {len(chiavi_tutte)}")
        print(f"Le ultime {CO_BACK} chiavi lette in fondo al file sono: {ultime_chiavi}")
        
        for k in ultime_chiavi:
            print(f"\nContenuto chiave '{k}':")
            for r in ["Bari", "Cagliari"]:
                if r in dati_grezzi[k]:
                    print(f"  - {r}: {dati_grezzi[k][r]} -> Numeri puliti: {puli_numeri(dati_grezzi[k][r])}")
                else:
                    print(f"  - {r} NON TROVATA in questa estrazione!")
        print("==================================\n")
        # ------------------------

        ultime_3 = [dati_grezzi[k] for k in ultime_chiavi]
        risultati_finali = []

        for i, est in enumerate(reversed(ultime_3)):
            colpo = i + 1
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    if r1 in est and r2 in est:
                        numeri1 = pulisci_numeri(est[r1])
                        numeri2 = pulisci_numeri(est[r2])
                        
                        if len(numeri1) == 5 and len(numeri2) == 5:
                            for pos in range(5):
                                n1 = numeri1[pos]
                                n2 = numeri2[pos]
                                dist = calcola_distanza(n1, n2)
                                
                                if dist == 45 or dist == 30:
                                    ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                    risultati_finali.append({
                                        "ruota": r1,
                                        "partner": r2,
                                        "numeri": ambo,
                                        "estrazione_r1": numeri1,
                                        "estrazione_r2": numeri2,
                                        "score": 180 if dist == 45 else 172,
                                        "colpo": colpo,
                                        "tag": f"Colpo {colpo}"
                                    })

        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Fatto. Combinazioni trovate: {len(risultati_finali)}")

    except Exception as e:
        print(f"❌ Errore nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
