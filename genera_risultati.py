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

def genera_risultati():
    try:
        # 1. Carica il file estrazioni.json
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        
        risultati_finali = []
        
        print("\n=== AVVIO MOTORE GEOMETRIC MIRROR V4 ===")
        
        # Gestiamo i 3 colpi a ritroso: 
        # colpo_idx = 1 significa l'ultimo blocco in fondo (il più recente)
        # colpo_idx = 2 significa il penultimo blocco, ecc.
        for colpo in [1, 2, 3]:
            print(f"🔄 Analisi concorsi per calcolo 'Colpo {colpo}'...")
            
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    # Verifichiamo che entrambe le ruote esistano nel database
                    if r1 in database and r2 in database:
                        lista_r1 = database[r1]
                        lista_r2 = database[r2]
                        
                        # Verifichiamo di avere abbastanza estrazioni storiche nella lista
                        if len(lista_r1) >= colpo and len(lista_r2) >= colpo:
                            # Prendiamo l'estrazione corretta a ritroso usando l'indice negativo (-1, -2, -3)
                            numeri1 = lista_r1[-colpo]
                            numeri2 = lista_r2[-colpo]
                            
                            # Controllo di sicurezza sui 5 numeri
                            if len(numeri1) == 5 and len(numeri2) == 5:
                                for pos in range(5):
                                    n1 = int(numeri1[pos])
                                    n2 = int(numeri2[pos])
                                    dist = calcola_distanza(n1, n2)
                                    
                                    # Condizione Geometric Mirror (Distanza 30 o 45)
                                    if dist == 45 or dist == 30:
                                        ambo = [fuori_90(n1 + n2), abs(n1 - n2) if n1 != n2 else 90]
                                        
                                        risultati_finali.append({
                                            "ruota": r1,
                                            "partner": r2,
                                            "numeri": ambo,
                                            "estrazione_r1": numeri1,  # Invia i 5 numeri reali alla card del sito
                                            "estrazione_r2": numeri2,  # Invia i 5 numeri reali alla card del sito
                                            "score": 180 if dist == 45 else 172,
                                            "colpo": colpo,
                                            "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                                        })

        # 3. Scrittura finale nel file dei risultati per il sito web
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"========================================\n✅ FINE! Generati con successo {len(risultati_finali)} pronostici in risultati_v4.json")

    except Exception as e:
        print(f"❌ Errore critico nel motore: {e}")

if __name__ == "__main__":
    genera_results = genera_risultati()
