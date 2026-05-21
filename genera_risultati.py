import json
import os

def calcola_distanza(n1, n2):
    """Calcola la distanza ciclometrica (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def genera_risultati():
    # 1. Caricamento dell'archivio estrazioni
    if not os.path.exists('estrazioni.json'):
        print("Errore: file estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    # Gestione flessibile se l'archivio è una lista o un dizionario
    if isinstance(archivio, list):
        # Se è una lista di estrazioni, usiamo gli indici come chiavi ordinate
        chiavi_ordinate = list(range(len(archivio)))
    else:
        # Se è il classico dizionario con le date
        chiavi_ordinate = sorted(list(archivio.keys()))

    if len(chiavi_ordinate) < 1:
        print("Errore: l'archivio non contiene abbastanza estrazioni.")
        return

    # Struttura dati V5 finale richiesta dalla dashboard
    risultati = {
        "nuove": [],
        "colpo2": [],
        "colpo3": [],
        "mappa_colore": {}
    }

    # Inizializziamo il contatore delle tensioni per tutte le ruote
    ruote_elenco = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
    conteggio_ruote = {r: 0 for r in ruote_elenco}

    # Definiamo i blocchi di estrazioni per i rispettivi colpi
    mappa_colpi = {
        "nuove": chiavi_ordinate[-1] if len(chiavi_ordinate) >= 1 else None,
        "colpo2": chiavi_ordinate[-2] if len(chiavi_ordinate) >= 2 else None,
        "colpo3": chiavi_ordinate[-3] if len(chiavi_ordinate) >= 3 else None
    }

    # 2. Elaborazione per ciascun colpo
    for etichetta_colpo, chiave_estrazione in mappa_colpi.items():
        if chiave_estrazione is None:
            continue

        estrazione_corrente = archivio[chiave_estrazione]
        
        # 🛠️ CORREZIONE ERROR: Gestiamo se l'estrazione interna è una lista di dizionari o un dizionario diretto
        if isinstance(estrazione_corrente, list):
            # Se è una lista (es. [{"ruota": "Bari", "numeri": [...]}]), la convertiamo al volo in dizionario
            temp_dict = {}
            for item in estrazione_corrente:
                if isinstance(item, dict) and "ruota" in item:
                    temp_dict[item["ruota"]] = item.get("numeri", [])
                elif isinstance(item, dict):
                    # Se ha le ruote come chiavi dentro dizionari singoli scritti in lista
                    temp_dict.update(item)
            estrazione_corrente = temp_dict

        ruote = list(estrazione_corrente.keys())

        # Confronto tra tutte le coppie di ruote (Isotopia e Simmetria)
        for i in range(len(ruote)):
            for j in range(i + 1, len(ruote)):
                ruota1 = ruote[i]
                ruota2 = ruote[j]

                if ruota1 == "Nazionale" or ruota2 == "Nazionale":
                    continue

                num_r1 = estrazione_corrente[ruota1]
                num_r2 = estrazione_corrente[ruota2]

                # Salto di sicurezza se mancano i dati della ruota o non sono liste valide
                if not isinstance(num_r1, list) or not isinstance(num_r2, list) or len(num_r1) < 5 or len(num_r2) < 5:
                    continue

                # Controllo posizione per posizione (Isotopia)
                for pos in range(5):
                    n1 = num_r1[pos]
                    n2 = num_r2[pos]

                    dist = calcola_distanza(n1, n2)

                    if dist in [45, 30, 15]:
                        score = 172
                        if dist == 45:
                            score = 180

                        pronostico_1 = (n1 + 30) % 90
                        pronostico_2 = (n2 + 30) % 90
                        if pronostico_1 == 0: pronostico_1 = 90
                        if pronostico_2 == 0: pronostico_2 = 90

                        # =======================================================
                        # 🛠️ LOGICA FILTRO SALVA-PORTAFOGLIO V5 (CORREZIONE ANOMALIE)
                        # =======================================================
                        if pronostico_1 == pronostico_2:
                            if pronostico_1 <= 45:
                                pronostico_2 = pronostico_1 + 45
                            else:
                                pronostico_2 = pronostico_1 - 45
                        # =======================================================

                        if etichetta_colpo == "nuove":
                            if ruota1 in conteggio_ruote: conteggio_ruote[ruota1] += 1
                            if ruota2 in conteggio_ruote: conteggio_ruote[ruota2] += 1

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

        risultati[etichetta_colpo] = sorted(
            risultati[etichetta_colpo], 
            key=lambda x: x['score'], 
            reverse=True
        )[:9]

    # 3. Generazione dei dati per la Mappa del Calore
    for ruota, colpi in conteggio_ruote.items():
        if colpi == 0:
            risultati["mappa_colore"][ruota] = "calore-basso"
        elif colpi <= 2:
            risultati["mappa_colore"][ruota] = "calore-medio"
        else:
            risultati["mappa_colore"][ruota] = "calore-alto"

    # 4. Scrittura del file dei risultati per la dashboard web
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    
    print("Sviluppo V5 completato con patch di stabilità per strutture a lista.")

if __name__ == "__main__":
    genera_risultati()
