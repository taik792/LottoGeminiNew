import json
import os

RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Tiene in memoria gli ultimi 3 concorsi per i colpi 1, 2 e 3

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
            database = json.load(f)
        
        # CORREZIONE AUTOMATICA STRUTTURA: Se il file è piatto, lo convertiamo in uno storico
        if any(ruota in database for ruota in RUOTE):
            print("⚠️ Rilevata struttura piatta! Converto automaticamente il file in formato Storico...")
            database = {"Concorso_Corrente": database}
            # Salviamo il file corretto così non si rompe più in futuro
            with open('estrazioni.json', 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=4)

        # Ordiniamo le estrazioni (le più recenti vanno in fondo)
        chiavi_ordinate = list(database.keys())
        ultime_chiavi = chiavi_ordinate[-CO_BACK:]
        print(f"📁 Analizzo gli ultimi concorsi inseriti: {ultime_chiavi}")
        
        risultati_finali = []

        # Analisi a ritroso (l'ultimo inserito è il Colpo 1, il penultimo è il Colpo 2...)
        for i, chiave_concorso in enumerate(reversed(ultime_chiavi)):
            colpo = i + 1
            est = database[chiave_concorso]
            
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
                                        "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                                    })

        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"=== RECAP FINALE ===")
        print(f"✅ Elaborazione riuscita! Pronostici totali salvati: {len(risultati_finali)}")

    except Exception as e:
        print(f"❌ Errore nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
