import json
import os

# CONFIGURAZIONE RUOTE (Con l'ordine esatto: Cagliari segue Bari)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 15  # Memoria delle ultime 3 estrazioni

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def pulisci_numeri(valore):
    """Converte i numeri in lista di interi, sia che siano scritti come lista [1,2] o come testo '1.2.3'"""
    if isinstance(valore, list):
        try:
            return [int(n) for n in valore]
        except:
            return []
    if isinstance(valore, str):
        try:
            # Sostituisce eventuali spazi o caratteri strani e divide sui punti
            valore_pulito = valore.replace(" ", ".").replace("-", ".")
            parti = [p for p in valore_pulito.split(".") if p.strip().isdigit()]
            return [int(n) for n in parti]
        except:
            return []
    return []

def genera_risultati():
    try:
        # 1. Caricamento del database delle estrazioni
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        # 2. Ordinamento delle chiavi numeriche
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        # Prendiamo le ultime 3 estrazioni disponibili per la memoria
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-CO_BACK:]
        
        risultati_finali = []

        # 3. Analisi sui 3 colpi a ritroso
        for i, est in enumerate(reversed(ultime_3)):
            colpo = i + 1
            
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    if r1 in est and r2 in est:
                        # Puliamo e convertiamo i numeri in liste reali di interi (gestisce il formato "10.20.30")
                        numeri1 = pulisci_numeri(est[r1])
                        numeri2 = pulisci_numeri(est[r2])
                        
                        # Controllo di sicurezza: devono esserci esattamente 5 numeri validi per ruota
                        if len(numeri1) == 5 and len(numeri2) == 5:
                            for pos in range(5):
                                n1 = numeri1[pos]
                                n2 = numeri2[pos]
                                dist = calcola_distanza(n1, n2)
                                
                                # Condizione Geometric Mirror: Distanza 45 o 30
                                if dist == 45 or dist == 30:
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

        # 4. Scrittura finale nel file richiesto da GitHub Pages
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Motore eseguito! Trovate {len(risultati_finali)} combinazioni valide.")

    except Exception as e:
        print(f"❌ Errore critico nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
