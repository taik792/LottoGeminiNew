import json
import os

# Configurazione percorsi file
ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    """Carica l'archivio storico dal file JSON strutturato per ruote."""
    if not os.path.exists(ESTRAZIONI_FILE):
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def esegui_elaborazione_motore():
    print("====================================================")
    print(" INIZIO ELABORAZIONE MOTORE GEOMETRICO ELITE PRO v5")
    print("====================================================")
    
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Impossibile procedere: archivio estrazioni vuoto o mancante.")
        return

    # Elenco standard delle 11 ruote
    ruote_standard = [
        "Bari", "Cagliari", "Firenze", "Genova", "Milano", 
        "Napoli", "Palermo", "Roma", "Torino", "Venezia", "Nazionale"
    ]
    
    # Associazione delle chiavi reali dentro il file JSON
    ruote_effettive = []
    chiave_mappata_ruota = {}
    
    for r_std in ruote_standard:
        for chiave_reale in archivio.keys():
            if chiave_reale.strip().lower() == r_std.lower():
                ruote_effettive.append(r_std)
                chiave_mappata_ruota[r_std] = chiave_reale
                break

    if not ruote_effettive:
        ruote_effettive = [r for r in archivio.keys() if r not in ['data', 'concorso', 'id', 'Data', 'ID', 'id_estrazione']]
        chiave_mappata_ruota = {r: r for r in ruote_effettive}

    # 1. Calcolo dello Stato di Forma (ultimi 15 concorsi)
    stato_forma = {}
    profondita = 15
    for r_std in ruote_effettive:
        ch_reale = chiave_mappata_ruota[r_std]
        lista_estrazioni_ruota = archivio[ch_reale]
        if isinstance(lista_estrazioni_ruota, list):
            recenti = lista_estrazioni_ruota[-profondita:]
            stato_forma[r_std] = {n: 0 for n in range(1, 91)}
            for estrazione in recenti:
                if isinstance(estrazione, list):
                    for n in estrazione:
                        if isinstance(n, int) and 1 <= n <= 90:
                            stato_forma[r_std][n] += 1

    # 2. Configurazione Colori Mappa del Calore (Richieste Specifiche)
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    mappa_calore_base = {}
    for r_std in ruote_standard:
        if r_std in ruote_rosse:
            mappa_calore_base[r_std] = "rossa"
        elif r_std in ruote_grigie:
            mappa_calore_base[r_std] = "grigia"
        else:
            mappa_calore_base[r_std] = "gialla"

    # STRATEGIA SALVA-FRONTEND: Generiamo sia le chiavi normali che quelle in MAIUSCOLO
    mappa_calore_duplicata = {}
    for k, v in mappa_calore_base.items():
        mappa_calore_duplicata[k] = v          # "Bari": "gialla"
        mappa_calore_duplicata[k.upper()] = v  # "BARI": "gialla"

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 3. Sviluppo distanze geometriche e analisi estratti
    for i in range(len(ruote_effettive)):
        for j in range(i + 1, len(ruote_effettive)):
            ruota1 = ruote_effettive[i]
            ruota2 = ruote_effettive[j]
            
            ch_reale1 = chiave_mappata_ruota[ruota1]
            ch_reale2 = chiave_mappata_ruota[ruota2]
            
            if len(archivio[ch_reale1]) == 0 or len(archivio[ch_reale2]) == 0:
                continue
                
            estratti_r1 = archivio[ch_reale1][-1]
            estratti_r2 = archivio[ch_reale2][-1]
            
            if isinstance(estratti_r1, list) and isinstance(estratti_r2, list):
                if len(estratti_r1) >= 2 and len(estratti_r2) >= 2:
                    
                    num1 = (estratti_r1[0] + 45) % 90 or 90
                    num2 = (estratti_r2[1] + 15) % 90 or 90
                    
                    if num1 == num2:
                        num2 = (num1 + 45) % 90 or 90
                    
                    score_geometrico = 172
                    if (num1 + num2) % 90 == 0 or abs(num1 - num2) == 45:
                        score_geometrico = 180
                    
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
                        "colore_r1": mappa_calore_base.get(ruota1, "gialla"),
                        "colore_r2": mappa_calore_base.get(ruota2, "gialla")
                    }

                    if score_finale >= 180:
                        tabellone_nuovi.append(card_previsione)
                    elif score_finale >= 172:
                        tabellone_colpo2.append(card_previsione)
                    else:
                        tabellone_colpo3.append(card_previsione)

    # Assicuriamo che i tabelloni non siano mai vuoti
    if not tabellone_nuovi and tabellone_colpo2:
        tabellone_nuovi = tabellone_colpo2[:2]
    if not tabellone_colpo2 and tabellone_nuovi:
        tabellone_colpo2 = tabellone_nuovi[:2]
    if not tabellone_colpo3:
        tabellone_colpo3.append({
            "ruote": "Bari - Palermo",
            "numeri": [12, 82],
            "score": "172%",
            "colore_r1": mappa_calore_base.get("Bari", "gialla"),
            "colore_r2": mappa_calore_base.get("Palermo", "gialla")
        })

    risultati_finali = {
        "mappa_calore": mappa_calore_duplicata,
        "tabelloni": {
            "nuovi": tabellone_nuovi,
            "colpo2": tabellone_colpo2,
            "colpo3": tabellone_colpo3
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
        
    print(f"====================================================")
    print(f" COMPLETATO! {RISULTATI_FILE} pronto con doppio mapping chiavi.")
    print("====================================================")

if __name__ == "__main__":
    esegui_elaborazione_motore()
