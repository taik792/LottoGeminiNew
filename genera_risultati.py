import json
import os

# CONFIGURAZIONE RUOTE (Nell'ordine corretto: Cagliari segue Bari)
RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
CO_BACK = 3  # Analizziamo gli ultimi 3 concorsi presenti in fondo alle liste

def calcola_distanza(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(n):
    while n > 90: n -= 90
    while n < 1: n += 90
    return n

def genera_risultati():
    try:
        if not os.path.exists('estrazioni.json'):
            print("❌ Errore: estrazioni.json non trovato.")
            return

        # 1. Caricamento del file JSON reale
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        
        risultati_finali = []

        # 2. Analisi sui 3 colpi a ritroso (1 = ultima estrazione, 2 = penultima, 3 = terzultima)
        for colpo in range(1, CO_BACK + 1):
            # L'indice a ritroso nella lista Python: -1 è l'ultimo, -2 il penultimo, -3 il terzultimo
            indice_estrazione = -colpo 
            
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    # Verifichiamo che entrambe le ruote esistano nel database
                    if r1 in database and r2 in database:
                        lista_r1 = database[r1]
                        lista_r2 = database[r2]
                        
                        # Verifichiamo che ci siano abbastanza estrazioni storiche da analizzare
                        if len(lista_r1) >= colpo and len(lista_r2) >= colpo:
                            numeri1 = lista_r1[indice_estrazione]
                            numeri2 = lista_r2[indice_estrazione]
                            
                            # Controllo di sicurezza: devono essere due cinquine valide
                            if isinstance(numeri1, list) and isinstance(numeri2, list) and len(numeri1) == 5 and len(numeri2) == 5:
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

        # 3. Scrittura del file finale atteso dal sito
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Motore eseguito con successo sulla struttura reale! Trovate {len(risultati_finali)} combinazioni.")

    except Exception as e:
        print(f"❌ Errore critico nel motore strutturato: {e}")

if __name__ == "__main__":
    genera_results = genera_risultati()
