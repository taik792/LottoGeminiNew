import json
import os

# CONFIGURAZIONE RUOTE (Cagliari segue Bari)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Memoria delle ultime 3 estrazioni

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def pulisci_numeri(valore):
    """Trasforma stringhe con punti '10.20...' o liste in veri numeri interi"""
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
        # 1. Carica il file estrazioni.json
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            dati_grezzi = json.load(f)
        
        # 2. Ordina matematicamente i concorsi per ID numerico (791, 792, 793...)
        chiavi_valide = [k for k in dati_grezzi.keys() if k.isdigit()]
        chiavi_ordinate = sorted(chiavi_valide, key=lambda x: int(x))
        
        # Prende le ultime 3 estrazioni (la più recente è l'ultima della lista)
        estrazioni_lista = [dati_grezzi[k] for k in chiavi_ordinate]
        ultime_3 = estrazioni_lista[-CO_BACK:]
        
        risultati_finali = []

        # 3. Analisi ciclica a ritroso (i=0 è l'estrazione di stasera)
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
                                
                                # Condizione Geometric Mirror
                                if dist == 45 or dist == 30:
                                    ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                    
                                    # Inviamo al JSON anche i 5 numeri reali estratti per il sito!
                                    risultati_finali.append({
                                        "ruota": r1,
                                        "partner": r2,
                                        "numeri": ambo,
                                        "estrazione_r1": numeri1,  # Cinque numeri reali ruota 1
                                        "estrazione_r2": numeri2,  # Cinque numeri reali ruota 2
                                        "score": 180 if dist == 45 else 172,
                                        "colpo": colpo,
                                        "tag": f"Colpo {colpo}"
                                    })

        # 4. Scrittura finale nel file dei risultati
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Ottimizzazione completata! Generati {len(risultati_finali)} pronostici con i 5 numeri estratti inclusi.")

    except Exception as e:
        print(f"❌ Errore nel motore: {e}")

if __name__ == "__main__":
    genera_results = genera_risultati()
