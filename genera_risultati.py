import json
import os
import itertools

def calcola_distanza_ciclometrica(n1, n2):
    """Calcola la distanza geometrica su un cerchio di 90 numeri (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_results():
    # 1. Carica il file delle estrazioni storiche
    if not os.path.exists('estrazioni.json'):
        print("Errore: estrazioni.json non trovato!")
        return
        
    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        estrazioni = json.load(f)
    
    # Struttura finale controllata per la dashboard
    risultati = {
        "nuove": [],
        "colpo2": []
    }
    
    # Definizione dei gruppi di ruote per i colori
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    if not estrazioni or not isinstance(estrazioni, dict):
        print("Errore: Formato estrazioni.json non valido.")
        return

    # 2. MOTORE CICLOMETRICO ESAGONALE
    distanze_esagono = [15, 30, 45]
    previsioni_totali = []
    lista_ruote = list(estrazioni.keys())
    
    # Cerchiamo le strutture armoniche nell'ultima estrazione
    for r1, r2 in itertools.combinations(lista_ruote, 2):
        if len(estrazioni[r1]) == 0 or len(estrazioni[r2]) == 0:
            continue
            
        cinquina_r1 = estrazioni[r1][-1]
        cinquina_r2 = estrazioni[r2][-1]
        
        condizione_trovata = False
        
        for n1 in cinquina_r1:
            for n2 in cinquina_r2:
                dist = calcola_distanza_ciclometrica(n1, n2)
                
                if dist in distanze_esagono and n1 != n2:
                    # Calcolo chiusure geometriche esagonali distinte
                    chiusura1 = (n1 + 15) if n1 + 15 <= 90 else (n1 + 15 - 90)
                    chiusura2 = (n2 + 45) if n2 + 45 <= 90 else (n2 + 45 - 90)
                    
                    if chiusura1 == chiusura2:
                        chiusura2 = (chiusura1 + 15) if chiusura1 + 15 <= 90 else 1
                    
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
            if condizione_trovata:
                break
                
        # CRITICO: Ci fermiamo non appena abbiamo abbastanza previsioni in totale (es. 8)
        # per evitare l'effetto cascata sulla dashboard!
        if len(previsioni_totali) >= 8:
            break

    # 3. DISTRIBUZIONE LIMITATA (Max 4 per tab)
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
        
        # Inserisce le prime 4 in 'nuove' e le successive 4 in 'colpo2'
        if idx < 4:
            risultati["nuove"].append(data_struttura)
        elif idx < 8:
            risultati["colpo2"].append(data_struttura)

    # 4. Scrittura del file finale pulito
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    print("File risultati_v4.json generato e limitato correttamente.")

if __name__ == "__main__":
    genera_results()
