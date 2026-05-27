import json
import os

# Configurazione percorsi file
ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    """Carica l'archivio storico dal file JSON adattandosi a liste o dizionari."""
    if not os.path.exists(ESTRAZIONI_FILE):
        print(f"Errore: Il file {ESTRAZIONI_FILE} non esiste.")
        return []
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        dati = json.load(f)
        # Se l'archivio è un dizionario, estraiamo i valori per renderlo una lista ordinata
        if isinstance(dati, dict):
            # Ordina le chiavi numericamente o cronologicamente se possibile
            try:
                chiavi_ordinate = sorted(dati.keys(), key=lambda x: int(x) if x.isdigit() else x)
                return [dati[k] for k in chiavi_ordinate]
            except Exception:
                return list(dati.values())
        return dati

def analizza_stato_forma(archivio, profondita=15):
    """
    Analizza le ultime estrazioni inserite (in fondo all'archivio)
    per determinare quanti estratti attivi ha ogni numero su ciascuna ruota.
    """
    stato_forma = {}
    if not archivio:
        return stato_forma
        
    # Essendo una lista ora lo slice funziona perfettamente
    estrazioni_recenti = archivio[-min(profondita, len(archivio)):]
    
    for estrazione in estrazioni_recenti:
        if not isinstance(estrazione, dict):
            continue
        for ruota, numeri in estrazione.items():
            if ruota in ['data', 'concorso', 'id', 'Data', 'ID', 'id_estrazione']:
                continue
            if ruota not in stato_forma:
                stato_forma[ruota] = {n: 0 for n in range(1, 91)}
            
            if isinstance(numeri, list):
                for n in numeri:
                    if isinstance(n, int) and 1 <= n <= 90:
                        stato_forma[ruota][n] += 1
    return stato_forma

def esegui_elaborazione_motore():
    print("====================================================")
    print(" INIZIO ELABORAZIONE MOTORE GEOMETRICO ELITE PRO v5")
    print("====================================================")
    
    # 1. Caricamento database cronologico
    dati_estrazioni = carica_dati_estrazioni()
    if not dati_estrazioni:
        print("Impossibile procedere: archivio estrazioni vuoto o mancante.")
        return
        
    print(f"Archivio caricato con successo. Rilevati {len(dati_estrazioni)} concorsi storici.")

    # 2. Estrazione dello stato di forma recente
    stato_forma = analizza_stato_forma(dati_estrazioni, profondita=15)

    # 3. Identificazione dell'ultimo concorso reale inserito
    ultima_estrazione = dati_estrazioni[-1]
    if not isinstance(ultima_estrazione, dict):
        print("Errore: la struttura dell'ultima estrazione non è valida.")
        return
        
    ruote_effettive = [r for r in ultima_estrazione.keys() if r not in ['data', 'concorso', 'id', 'Data', 'ID', 'id_estrazione']]
    
    # 4. Definizione della Mappa del Calore
    ruote_tensione_rossa = ["Firenze", "Roma", "Torino", "Napoli"]
    mappa_calore = {}
    
    for ruota in ruote_effettive:
        if ruota in ruote_tensione_rossa:
            mappa_calore[ruota] = "rossa"
        else:
            mappa_calore[ruota] = "gialla"

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 5. Doppi cicli FOR per il calcolo delle distanze geometriche
    for i in range(len(ruote_effettive)):
        for j in range(i + 1, len(ruote_effettive)):
            ruota1 = ruote_effettive[i]
            ruota2 = ruote_effettive[j]
            
            estratti_r1 = ultima_estrazione[ruota1]
            estratti_r2 = ultima_estrazione[ruota2]
            
            if isinstance(estratti_r1, list) and isinstance(estratti_r2, list):
                if len(estratti_r1) >= 2 and len(estratti_r2) >= 2:
                    
                    # Logica nativa delle distanze geometriche
                    num1 = (estratti_r1[0] + 45) % 90 or 90
                    num2 = (estratti_r2[1] + 15) % 90 or 90
                    
                    if num1 == num2:
                        num2 = (num1 + 45) % 90 or 90
                    
                    score_geometrico = 172
                    if (num1 + num2) % 90 == 0 or abs(num1 - num2) == 45:
                        score_geometrico = 180
                    
                    # FILTRO FREQUENTI
                    presenza_n1 = stato_forma.get(ruota1, {}).get(num1, 0)
                    presenza_n2 = stato_forma.get(ruota2, {}).get(num2, 0)
                    
                    if presenza_n1 == 0 and presenza_n2 == 0:
                        score_finale = score_geometrico - 8
                    else:
                        score_finale = score_geometrico

                    card_previsione = {
                        "ruote": f"{ruota1} - {ruota2}",
                        "numeri": [num1, num2],
                        "score": f"{score_finale}%",
                        "colore_r1": mappa_calore.get(ruota1, "gialla"),
                        "colore_r2": mappa_calore.get(ruota2, "gialla")
                    }

                    if score_finale >= 180:
                        tabellone_nuovi.append(card_previsione)
                    elif score_finale >= 172:
                        tabellone_colpo2.append(card_previsione)
                    else:
                        tabellone_colpo3.append(card_previsione)

    # 6. Riempimento di sicurezza dei tabelloni
    if not tabellone_nuovi and tabellone_colpo2:
        tabellone_nuovi = tabellone_colpo2[:2]
    if not tabellone_colpo3:
        tabellone_colpo3.append({
            "ruote": "Bari - Palermo",
            "numeri": [12, 82],
            "score": "172%",
            "colore_r1": mappa_calore.get("Bari", "gialla"),
            "colore_r2": mappa_calore.get("Palermo", "gialla")
        })

    # Struttura finale dell'oggetto JSON
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:4],
            "colpo2": tabellone_colpo2[:4],
            "colpo3": tabellone_colpo3[:4]
        }
    }

    # Scrittura definitiva del file risultati_v4.json
    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
        
    print("====================================================")
    print(f" ELABORAZIONE COMPLETATA! File {RISULTATI_FILE} generato.")
    print("====================================================")

if __name__ == "__main__":
    esegui_elaborazione_motore()
