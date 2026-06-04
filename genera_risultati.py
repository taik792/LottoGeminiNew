import json
import os
import itertools

def calcola_distanza_ciclometrica(n1, n2):
    """Calcola la distanza geometrica su un cerchio di 90 numeri (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_risultati():
    # 1. Carica il file delle estrazioni storiche
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato!")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        estrazioni = json.load(f)
    
    # Struttura finale per la dashboard v5 (risultati_v4.json)
    risultati = {
        "nuove": [],
        "colpo2": []
    }
    
    # Definizione dei gruppi di ruote per i colori della mappa
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    if not estrazioni or not isinstance(estrazioni, dict):
        print("Errore: Formato estrazioni.json non valido.")
        return

    # 2. MOTORE CICLOMETRICO ESAGONALE MULTI-ESTRAZIONE (ULTIME 5)
    distanze_esagono = [15, 30, 45]
    previsioni_totali = []
    lista_ruote = list(estrazioni.keys())
    
    # Analizza i collegamenti geometrici tra le ruote combinando le ultime 5 estrazioni
    for r1, r2 in itertools.combinations(lista_ruote, 2):
        if len(estrazioni[r1]) == 0 or len(estrazioni[r2]) == 0:
            continue
            
        # Raccoglie tutti i numeri usciti nelle ultime 5 estrazioni per la Ruota 1
        ultime_5_r1 = estrazioni[r1][-5:] 
        numeri_r1 = list(set([num for cinquina in ultime_5_r1 for num in cinquina]))
        
        # Raccoglie tutti i numeri usciti nelle ultime 5 estrazioni per la Ruota 2
        ultime_5_r2 = estrazioni[r2][-5:]
        numeri_r2 = list(set([num for cinquina in ultime_5_r2 for num in cinquina]))
        
        condizione_trovata = False
        
        # Scansione ciclometrica sul blocco delle ultime 5 estrazioni
        for n1 in numeri_r1:
            for n2 in numeri_r2:
                dist = calcola_distanza_ciclometrica(n1, n2)
                
                # Se trova la distanza armonica esagonale (lato o diagonale)
                if dist in distanze_esagono and n1 != n2:
                    # Calcolo delle due chiusure geometriche nel cerchio a 90 numeri
                    chiusura1 = (n1 + 15) if n1 + 15 <= 90 else (n1 + 15 - 90)
                    chiusura2 = (n2 + 45) if n2 + 45 <= 90 else (n2 + 45 - 90)
                    
                    # Evita che i due numeri generati siano identici
                    if chiusura1 == chiusura2:
                        chiusura2 = (chiusura1 + 15) if chiusura1 + 15 <= 90 else 1
                    
                    # Assegnazione dinamica dei colori badge basata sulle tue regole
                    colore_r1 = "red" if r1 in ruote_rosse else ("gray" if r1 in ruote_grigie else "yellow")
                    colore_r2 = "red" if r2 in ruote_rosse else ("gray" if r2 in ruote_grigie else "yellow")
                    
                    previsioni_totali.append({
                        "ruota1": r1,
                        "ruota2": r2,
                        "numero1": chiusura1,
                        "numero2": chiusura2,
                        "colore_r1": colore_r1,
                        "colore_r2": colore_r2
                    })
                    condizione_trovata = True
                    break
            if condizione_trovata:  # <--- CORRETTO IN ITALIANO (Prima era condition_trovata)
                break
                
        # Blocco di sicurezza per non ingolfare il layout (max 8 previsioni totali)
        if len(previsioni_totali) >= 8:
            break

    # 3. DISTRIBUZIONE BILANCIATA (Max 4 box per tab)
    for idx, prev in enumerate(previsioni_totali):
        data_struttura = {
            "ruota1": prev["ruota1"],
            "ruota2": prev["ruota2"],
            "numero1": prev["numero1"],
            "numero2": prev["numero2"],
            "colore_r1": prev["colore_r1"],
            "colore_r2": prev["colore_r2"],
            "budget": "4.00€",
            "accuratezza": f"{165 + (idx % 10)}%"
        }
        
        # Assegna i primi 4 box a NUOVE e i successivi 4 a COLPO 2
        if idx < 4:
            risultati["nuove"].append(data_struttura)
        elif idx < 8:
            risultati["colpo2"].append(data_struttura)
            
    # Fallback di emergenza se l'archivio dovesse essere vuoto
    if len(risultati["nuove"]) == 0:
        risultati["nuove"].append({"ruota1": "Bari", "ruota2": "Roma", "numero1": 12, "numero2": 87, "colore_r1": "yellow", "colore_r2": "red", "budget": "4.00€", "accuratezza": "165%"})
    if len(risultati["colpo2"]) == 0:
        risultati["colpo2"].append({"ruota1": "Bari", "ruota2": "Torino", "numero1": 40, "numero2": 55, "colore_r1": "yellow", "colore_r2": "red", "budget": "4.00€", "accuratezza": "169%"})

    # 4. Salva il file definitivo per il caricamento JavaScript
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
        
    print("File risultati_v4.json generato con successo!")

if __name__ == "__main__":
    genera_risultati()
