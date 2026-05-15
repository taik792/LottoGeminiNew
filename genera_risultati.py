import json
import os

# CONFIGURAZIONE RUOTE (Ordine corretto: Cagliari segue Bari)
RUOTE_MAP = {
    "BA": "Bari", "CA": "Cagliari", "FI": "Firenze", "GE": "Genova", 
    "MI": "Milano", "NA": "Napoli", "PA": "Palermo", "RM": "Roma", 
    "TO": "Torino", "VE": "Venezia"
}
RUOTE_ORDINE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
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
        if not os.path.exists('storico01-oggi.txt'):
            print("❌ Errore: Il file storico01-oggi.txt non è stato trovato!")
            return

        # 1. Lettura del file di testo storico
        with open('storico01-oggi.txt', 'r', encoding='utf-8') as f:
            righe = f.readlines()

        # 2. Raggruppamento delle estrazioni per DATA
        estrazioni_per_data = {}
        for riga in righe:
            parti = riga.strip().split('\t')
            if len(parti) >= 7:
                data = parti[0]      # Es: "2026/05/09"
                ruota_sigla = parti[1] # Es: "BA"
                
                if ruota_sigla in RUOTE_MAP:
                    ruota_nome = RUOTE_MAP[ruota_sigla]
                    try:
                        numeri = [int(x) for x in parti[2:7]]
                        if data not in estrazioni_per_data:
                            estrazioni_per_data[data] = {}
                        estrazioni_per_data[data][ruota_nome] = numeri
                    except ValueError:
                        continue

        # 3. Ordinamento cronologico delle date (dal più vecchio al più recente)
        date_ordinate = sorted(list(estrazioni_per_data.keys()))
        
        # Prendiamo le ultime estrazioni richieste per il calcolo della memoria
        ultime_date = date_ordinate[-CO_BACK:]
        
        risultati_finali = []

        # 4. Analisi ciclometrica a ritroso (colpo 1 = ultima estrazione inserita)
        for i, data in enumerate(reversed(ultime_date)):
            colpo = i + 1
            est = estrazioni_per_data[data]
            
            for idx1 in range(len(RUOTE_ORDINE)):
                for idx2 in range(idx1 + 1, len(RUOTE_ORDINE)):
                    r1 = RUOTE_ORDINE[idx1]
                    r2 = RUOTE_ORDINE[idx2]
                    
                    if r1 in est and r2 in est:
                        numeri1 = est[r1]
                        numeri2 = est[r2]
                        
                        if len(numeri1) == 5 and len(numeri2) == 5:
                            for pos in range(5):
                                n1 = numeri1[pos]
                                n2 = numeri2[pos]
                                dist = calcola_distanza(n1, n2)
                                
                                # Condizione Geometric Mirror: Distanza 45 o 30 isotopa
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

        # 5. Scrittura finale nel file JSON per il frontend del sito
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Analisi completata con successo! Trovate {len(risultati_finali)} combinazioni nelle ultime {len(ultime_date)} estrazioni.")

    except Exception as e:
        print(f"❌ Errore critico nel motore: {e}")

if __name__ == "__main__":
    genera_risultati()
