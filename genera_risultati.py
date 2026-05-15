import json
import os

# CONFIGURAZIONE RUOTE (Nell'ordine corretto per il tuo script)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Conserva la memoria delle ultime 3 estrazioni

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def genera_risultati():
    try:
        # 1. Caricamento sicuro del database delle estrazioni
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        # 2. Ordinamento delle chiavi numeriche (es. "790", "791", "792")
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        # Estraiamo le ultime 3 estrazioni (le più recenti in fondo al file)
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-CO_BACK:]
        
        risultati_finali = []

        # 3. Analisi ciclica dei colpi a ritroso (dall'ultimo concorso indietro)
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
                            
                            # Logica Geometric Mirror (Distanze 45 e 30)
                            if dist == 45 or dist == 30:
                                ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                risultati_finali.append({
                                    "ruota": r1,
                                    "partner": r2,
                                    "numeri": ambo,
                                    "score": 180 if dist == 45 else 172,
                                    "colpo": colpo,
                                    "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                                })

        # 4. IL GIUNTO PERFETTO: Salviamo con il nome rigido richiesto da GitHub Action v4
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ File 'risultati_v4.json' generato con successo con {len(risultati_finali)} previsioni.")

    except Exception as e:
        print(f"❌ Errore critico durante l'elaborazione: {e}")

# Questo blocco permette l'esecuzione automatica da parte del Lotto Bot
if __name__ == "__main__":
    genera_risultati()
