import json
import os

# Configurazione percorsi file
ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    """Carica l'archivio storico dal file JSON strutturato per ruote."""
    if not os.path.exists(ESTRAZIONI_FILE):
        print(f"Errore: Il file {ESTRAZIONI_FILE} non esiste.")
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def esegui_elaborazione_motore():
    print("====================================================")
    print(" INIZIO ELABORAZIONE MOTORE GEOMETRICO ELITE PRO v5")
    print("====================================================")
    
    # 1. Caricamento database strutturato per ruote (dal vecchio in alto al giovane in basso)
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Impossibile procedere: archivio estrazioni vuoto o mancante.")
        return
        
    print("Archivio caricato con successo. Analisi struttura verticale delle ruote.")

    # Lista delle ruote presenti nel tuo file
    ruote_effettive = [r for r in archivio.keys() if r not in ['data', 'concorso', 'id', 'Data', 'ID', 'id_estrazione']]
    
    # 2. Calcolo dello Stato di Forma (Filtro Frequenti)
    # Estraiamo gli ultimi 15 concorsi (gli ultimi elementi in fondo alle liste di ciascuna ruota)
    stato_forma = {}
    profondita = 15
    
    for ruota in ruote_effettive:
        lista_estrazioni_ruota = archivio[ruota]
        if isinstance(lista_estrazioni_ruota, list):
            # Prendiamo le ultime 15 estrazioni in fondo alla lista (le più giovani)
            recenti = lista_estrazioni_ruota[-profondita:]
            stato_forma[ruota] = {n: 0 for n in range(1, 91)}
            for estrazione in recenti:
                if isinstance(estrazione, list):
                    for n in estrazione:
                        if isinstance(n, int) and 1 <= n <= 90:
                            stato_forma[ruota][n] += 1

    # 3. Definizione della Mappa del Calore (Direttive colori originali)
    ruote_tensione_rossa = ["Firenze", "Roma", "Torino", "Napoli"]
    mappa_calore = {}
    for ruota in ruote_effettive:
        if ruota in ruote_tensione_rossa:
            mappa_calore[ruota] = "rossa"
        else:
            mappa_calore[ruota] = "gialla"  # Milano e le altre sono gialle

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 4. Doppi cicli FOR per il calcolo delle distanze geometriche sulle ultime estrazioni reali
    for i in range(len(ruote_effettive)):
        for j in range(i + 1, len(ruote_effettive)):
            ruota1 = ruote_effettive[i]
            ruota2 = ruote_effettive[j]
            
            # L'ultima estrazione inserita è l'ultimo elemento [-1] della lista di quella ruota
            if len(archivio[ruota1]) == 0 or len(archivio[ruota2]) == 0:
                continue
                
            estratti_r1 = archivio[ruota1][-1]
            estratti_r2 = archivio[ruota2][-1]
            
            if isinstance(estratti_r1, list) and isinstance(estratti_r2, list):
                if len(estratti_r1) >= 2 and len(estratti_r2) >= 2:
                    
                    # Logica nativa ciclo-geometrica applicata agli estratti reali
                    num1 = (estratti_r1[0] + 45) % 90 or 90
                    num2 = (estratti_r2[1] + 15) % 90 or 90
                    
                    if num1 == num2:
                        num2 = (num1 + 45) % 90 or 90
                    
                    score_geometrico = 172
                    if (num1 + num2) % 90 == 0 or abs(num1 - num2) == 45:
                        score_geometrico = 180
                    
                    # FILTRO FREQUENTI ANTISFALDAMENTO
                    presenza_n1 = stato_forma.get(ruota1, {}).get(num1, 0)
                    presenza_n2 = stato_forma.get(ruota2, {}).get(num2, 0)
                    
                    # Se entrambi i numeri dell'ambo geometrico sono assenti da 15 estrazioni,
                    # abbassiamo lo score di 8 punti per proteggerci dai laterali (+1 / -1)
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

    # 5. Riempimento di sicurezza dei tabelloni della dashboard
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

    # Struttura finale dell'oggetto JSON pronta per il frontend index.html
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:4],
            "colpo2": tabellone_colpo2[:4],
            "colpo3": tabellone_colpo3[:4]
        }
    }

    # Scrittura definitiva e popolamento del file risultati_v4.json
    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
        
    print("====================================================")
    print(f" ELABORAZIONE COMPLETATA! File {RISULTATI_FILE} correttamente popolato.")
    print("====================================================")

if __name__ == "__main__":
    esegui_elaborazione_motore()
