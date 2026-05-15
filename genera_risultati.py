import json
import os

# CONFIGURAZIONE RUOTE (Cagliari segue Bari)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

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
        # 1. Carica il file estrazioni.json (che contiene direttamente le ruote)
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            est = json.load(f)
        
        risultati_finali = []

        print("\n=== CALCOLO GEOMETRIC MIRROR ===")
        
        # 2. Confronto diretto tra tutte le ruote presenti nel file
        for idx1 in range(len(RUOTE)):
            for idx2 in range(idx1 + 1, len(RUOTE)):
                r1 = RUOTE[idx1]
                r2 = RUOTE[idx2]
                
                # Verifichiamo se entrambe le ruote esistono nel JSON
                if r1 in est and r2 in est:
                    numeri1 = pulisci_numeri(est[r1])
                    numeri2 = pulisci_numeri(est[r2])
                    
                    if len(numeri1) == 5 and len(numeri2) == 5:
                        for pos in range(5):
                            n1 = numeri1[pos]
                            n2 = numeri2[pos]
                            dist = calcola_distanza(n1, n2)
                            
                            # Condizione Geometric Mirror (Distanza 30 o 45)
                            if dist == 45 or dist == 30:
                                ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                
                                risultati_finali.append({
                                    "ruota": r1,
                                    "partner": r2,
                                    "numeri": ambo,
                                    "estrazione_r1": numeri1,  # I 5 numeri reali per il sito
                                    "estrazione_r2": numeri2,  # I 5 numeri reali per il sito
                                    "score": 180 if dist == 45 else 172,
                                    "colpo": 1,
                                    "tag": "NUOVA"
                                })
                                print(f"🎯 Trovata condizione: {r1}-{r2} in Pos.{pos+1} (Dist. {dist})")

        # 3. Scrittura finale nel file dei risultati
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"================================\n✅ Successo! Generati {len(risultati_finali)} pronostici in risultati_v4.json")

    except Exception as e:
        print(f"❌ Errore nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
