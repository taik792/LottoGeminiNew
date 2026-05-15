import json
import os

def genera_risultati():
    file_input = 'estrazioni.json'
    file_output = 'risultati_v4.json'
    
    # 1. Controllo se il file esiste
    if not os.path.exists(file_input):
        print(f"❌ ERRORE: Il file {file_input} non esiste nella cartella!")
        return

    try:
        with open(file_input, 'r', encoding='utf-8') as f:
            database = json.load(f)
        
        print(f"✅ File caricato. Trovate {len(database)} chiavi nel database.")

        # 2. Trasformiamo tutto in una lista ordinata
        # Usiamo un metodo più robusto per estrarre i dati
        estrazioni_lista = []
        chiavi_ordinate = sorted([k for k in database.keys() if k.isdigit()], key=int)
        
        for k in chiavi_ordinate:
            estrazioni_lista.append(database[k])
            
        print(f"✅ Estrazioni convertite in lista: {len(estrazioni_lista)}")

        # 3. Prendiamo le ultime 5 (più memoria per sicurezza)
        ultime = estrazioni_lista[-5:]
        risultati = []
        
        ruote = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

        # 4. Analisi semplificata (cerchiamo DISTANZA 45 ovunque)
        for i, est in enumerate(reversed(ultime)):
            colpo = i + 1
            for r1 in ruote:
                for r2 in ruote:
                    if r1 == r2 or r1 not in est or r2 not in est:
                        continue
                        
                    v1, v2 = est[r1], est[r2]
                    
                    for p in range(5):
                        n1, n2 = v1[p], v2[p]
                        dist = abs(n1 - n2)
                        if dist > 45: dist = 90 - dist
                        
                        if dist == 45 or dist == 30:
                            # Calcolo previsione
                            somma = n1 + n2
                            if somma > 90: somma -= 90
                            diff = abs(n1 - n2)
                            if diff == 0: diff = 90
                            
                            risultati.append({
                                "ruota": r1,
                                "partner": r2,
                                "numeri": [somma, diff],
                                "score": 180 if dist == 45 else 172,
                                "colpo": colpo,
                                "tag": "NUOVA" if colpo == 1 else f"Colpo {colpo}"
                            })

        # 5. Scrittura forzata
        with open(file_output, 'w', encoding='utf-8') as f:
            json.dump(risultati, f, indent=4)
            
        print(f"🚀 OPERAZIONE COMPLETATA: Scritto {file_output} con {len(risultati)} previsioni.")

    except Exception as e:
        print(f"❌ ERRORE CRITICO: {str(e)}")

if __name__ == "__main__":
    genera_risultati()
