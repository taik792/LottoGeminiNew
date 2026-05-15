import json
import os

# CONFIGURAZIONE RUOTE (Con Cagliari subito dopo Bari)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Analizza le ultime 3 estrazioni per la memoria

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def genera_risultati():
    try:
        # 1. Caricamento sicuro del file estrazioni
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        # 2. Ordinamento delle chiavi numeriche (es. "791", "792", "793")
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        # Prendiamo le ultime 3 estrazioni disponibili
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-CO_BACK:]
        
        risultati_finali = []

        # 3. Analisi sui 3 colpi a ritroso usando l'ordine fisso delle RUOTE
        for i, est in enumerate(reversed(ultime_3)):
            colpo = i + 1
            
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    # Verifichiamo che entrambe le ruote esistano in questa estrazione
                    if r1 in est and r2 in est:
                        numeri1 = est[r1]
                        numeri2 = est[r2]
                        
                        # Controllo di sicurezza sulle liste dei numeri
                        if isinstance(numeri1, list) and isinstance(numeri2, list) and len(numeri1) == 5 and len(numeri2) == 5:
                            for pos in range(5):
                                n1 = numeri1[pos]
                                n2 = numeri2[pos]
                                dist = calcola_distanza(n1, n2)
                                
                                # Condizione Geometric Mirror: Distanza 45 o 30
                                if dist == 45 or dist == 30:
                                    # Calcolo dell'ambo geometrico secondo il tuo standard
                                    somma_fuori90 = fuori_90(n1 + n2)
                                    diff_geometrica = abs(n1 - n2) if n1 != n2 else 90
                                    ambo = [somma_fuori90, diff_geometrica]
                                    
                                    risultati_finali.append({
                                        "ruota": r1,
                                        "partner": r2,
                                        "numeri": ambo,
                                        "score": 180 if dist == 45 else 172,
                                        "colpo": colpo,
                                        "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                                    })

        # 4. Scrittura finale nel file richiesto dal frontend
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Motore V4.1 eseguito con successo! Trovate {len(risultati_finali)} combinazioni nelle ultime {len(ultime_3)} estrazioni.")

    except Exception as e:
        print(f"❌ Errore critico nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
