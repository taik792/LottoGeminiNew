import json
import os

def calcola_distanza(n1, n2):
    """Calcola la distanza ciclometrica (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_risultati():
    # 1. Caricamento dell'archivio estrazioni strutturato per Ruote
    if not os.path.exists('estrazioni.json'):
        print("Errore: file estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # Elenco delle ruote canoniche da analizzare
    ruote_elenco = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
    
    # Verifica che ci siano estrazioni a sufficienza controllando una ruota pilota (es. Bari)
    if "Bari" not in archivio or not isinstance(archivio["Bari"], list) or len(archivio["Bari"]) < 3:
        print("Errore: Struttura dati non conforme o estrazioni insufficienti.")
        return

    num_estrazioni = len(archivio["Bari"])
    print(f"Rilevate {num_estrazioni} estrazioni storiche memorizzate per ruota.")

    # Struttura dati V5 finale richiesta dalla dashboard web
    risultati = {
        "nuove": [],
        "colpo2": [],
        "colpo3": [],
        "mappa_colore": {}
    }

    # Inizializziamo il contatore delle tensioni per la mappa del calore
    conteggio_ruote = {r: 0 for r in ruote_elenco}

    # Mappatura dei colpi basata sugli indici negativi (dal più recente a ritroso)
    mappa_colpi = {
        "nuove": -1,   # L'ultima estrazione inserita (la più recente)
        "colpo2": -2,  # La penultima
        "colpo3": -3   # La terzultima
    }

    # 2. Elaborazione dei tre colpi ciclometrici
    for etichetta_colpo, indice_storico in mappa_colpi.items():
        
        # Confronto tra tutte le coppie di ruote per l'estrazione corrente identificata dall'indice
        for i in range(len(ruote_elenco)):
            for j in range(i + 1, len(ruote_elenco)):
                ruota1 = ruote_elenco[i]
                ruota2 = ruote_elenco[j]

                # Saltiamo se la ruota non è presente nel file json corrente
                if ruota1 not in archivio or ruota2 not in archivio:
                    continue

                # Estrazione dei 5 numeri per ciascuna ruota basandosi sull'indice cronologico
                try:
                    num_r1 = archivio[ruota1][indice_storico]
                    num_r2 = archivio[ruota2][indice_storico]
                except IndexError:
                    continue # Salto di sicurezza in caso di indici fuori portata

                # Controllo formale sulla validità della cinquina
                if not isinstance(num_r1, list) or not isinstance(num_r2, list) or len(num_r1) < 5 or len(num_r2) < 5:
                    continue

                # Controllo posizione per posizione (Isotopia geometrica)
                for pos in range(5):
                    try:
                        n1 = int(num_r1[pos])
                        n2 = int(num_r2[pos])
                    except (ValueError, IndexError):
                        continue

                    dist = calcola_distanza(n1, n2)

                    # Intercettazione delle distanze armoniche della simmetria specchio
                    if dist in [45, 30, 15]:
                        score = 172
                        if dist == 45:
                            score = 180

                        # Calcolo matematico dei pronostici speculari
                        pronostico_1 = (n1 + 30) % 90
                        pronostico_2 = (n2 + 30) % 90
                        if pronostico_1 == 0: pronostico_1 = 90
                        if pronostico_2 == 0: pronostico_2 = 90

                        # =======================================================
                        # 🛠️ FILTRO SALVA-PORTAFOGLIO V5 (CORREZIONE ANOMALIA DOPPIONI)
                        # =======================================================
                        if pronostico_1 == pronostico_2:
                            if pronostico_1 <= 45:
                                pronostico_2 = pronostico_1 + 45
                            else:
                                pronostico_2 = pronostico_1 - 45
                        # =======================================================

                        # Alimenta la tensione della mappa del calore solo sulle nuove condizioni attive
                        if etichetta_colpo == "nuove":
                            conteggio_ruote[ruota1] += 1
                            conteggio_ruote[ruota2] += 1

                        card = {
                            "ruota1": ruota1,
                            "ruota2": ruota2,
                            "num1": pronostico_1,
                            "num2": pronostico_2,
                            "score": score,
                            "dati_r1": " . ".join(map(str, num_r1)),
                            "dati_r2": " . ".join(map(str, num_r2))
                        }
                        
                        risultati[etichetta_colpo].append(card)

        # Ordinamento decrescente per Score qualitativo ed estrazione dei primi 9 pronostici top
        risultati[etichetta_colpo] = sorted(
            risultati[etichetta_colpo], 
            key=lambda x: x['score'], 
            reverse=True
        )[:9]

    # 3. Calcolo e assegnazione dei livelli di colore per la Heatmap
    for ruota, colpi in conteggio_ruote.items():
        if colpi == 0:
            risultati["mappa_colore"][ruota] = "calore-basso"
        elif colpi <= 2:
            risultati["mappa_colore"][ruota] = "calore-medio"
        else:
            risultati["mappa_colore"][ruota] = "calore-alto"

    # 4. Scrittura del file JSON finale atteso dalla dashboard
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    
    print("Sviluppo Lotto Elite Pro V5 completato con successo. Dati scritti correttamente.")

if __name__ == "__main__":
    genera_risultati()
