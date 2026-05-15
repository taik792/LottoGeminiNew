import json
import os

# CONFIGURAZIONE RUOTE (Nell'ordine corretto: Cagliari dopo Bari)
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
        # Se il JSON principale è corrotto a causa del download incompleto, proviamo a pulirlo al volo
        with open('estrazioni.json', 'r', encoding='utf-8') as f:
            testo = f.read().strip()
            
        # Forza la chiusura del JSON se si è troncato durante il download dello storico
        if not testo.endswith('}'):
            if testo.endswith(']'): testo += '\n}'
            elif testo.endswith(','): testo = testo[:-1] + ']}'
            else: testo += ']}'
            
        dati = json.loads(testo)
        risultati_finali = []

        # Ciclo per calcolare gli ultimi 3 concorsi presenti in memoria (-1, -2, -3 in fondo alle liste)
        for colpo in range(1, 4):
            indice_estrazione = -colpo  # -1 è l'ultima di stasera, -2 la precedente, ecc.
            
            for idx1 in range(len(RUOTE)):
                for idx2 in range(idx1 + 1, len(RUOTE)):
                    r1 = RUOTE[idx1]
                    r2 = RUOTE[idx2]
                    
                    if r1 in dati and r2 in dati:
                        # Controlliamo di avere abbastanza estrazioni storiche nella ruota
                        if len(dati[r1]) >= colpo and len(dati[r2]) >= colpo:
                            numeri1 = [int(x) for x in dati[r1][indice_estrazione]]
                            numeri2 = [int(x) for x in dati[r2][indice_estrazione]]
                            
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

        # Scrive il file finale v4 richiesto dalle tue card del sito
        with open('risultati_v4.json', 'w', encoding='utf-8') as f:
            json.dump(risultati_finali, f, indent=4)
        
        print(f"✅ Motore Geometrico: Elaborati con successo {len(risultati_finali)} pronostici basati sullo storico!")

    except Exception as e:
        print(f"❌ Errore durante l'elaborazione dei dati: {e}")

if __name__ == "__main__":
    genera_results()
