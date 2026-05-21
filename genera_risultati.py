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

    # Prendiamo le ultime estrazioni per i calcoli dei colpi
    chiavi_ordinate = sorted(list(archivio.keys()))
    if len(chiavi_ordinate) < 1:
        print("Errore: l'archivio non contiene abbastanza estrazioni.")
        return

    # Struttura dati per i risultati finali
    risultati = {
        "nuove": [],
        "colpo2": [],
        "colpo3": []
    }

    # Definiamo i blocchi di estrazioni per i rispettivi colpi
    # nuove -> basate sull'ultima estrazione assoluta
    # colpo2 -> basate sulla penultima
    # colpo3 -> basate sulla terzultima
    mappa_colpi = {
        "nuove": chiavi_ordinate[-1] if len(chiavi_ordinate) >= 1 else None,
        "colpo2": chiavi_ordinate[-2] if len(chiavi_ordinate) >= 2 else None,
        "colpo3": chiavi_ordinate[-3] if len(chiavi_ordinate) >= 3 else None
    }

    # 2. Elaborazione per ciascun colpo
    for etichetta_colpo, data_estrazione in mappa_colpi.items():
        if not data_estrazione:
            continue

        estrazione_corrente = archivio[data_estrazione]
        ruote = list(estrazione_corrente.keys())

        # Confronto tra tutte le coppie di ruote (Isotopia e Simmetria)
        for i in range(len(ruote)):
            for j in range(i + 1, len(ruote)):
                ruota1 = ruote[i]
                ruota2 = ruote[j]

                # Saltiamo la Nazionale nei calcoli principali per stabilità geometrica
                if ruota1 == "Nazionale" or ruota2 == "Nazionale":
                    continue

                num_r1 = estrazione_corrente[ruota1]
                num_r2 = estrazione_corrente[ruota2]

                # Controllo posizione per posizione (Isotopia)
                for pos in range(5):
                    n1 = num_r1[pos]
                    n2 = num_r2[pos]

                    dist = calcola_distanza(n1, n2)

                    # Cerchiamo le distanze armoniche principali (45, 30, 60)
                    if dist in [45, 30, 15]:
                        score = 172
                        if dist == 45:
                            score = 180

                        # Calcolo base dei pronostici teorici
                        pronostico_1 = (n1 + 30) % 90
                        pronostico_2 = (n2 + 30) % 90
                        if pronostico_1 == 0: pronostico_1 = 90
                        if pronostico_2 == 0: pronostico_2 = 90

                        # =======================================================
                        # 🛠️ LOGICA FILTRO SALVA-PORTAFOGLIO V5 (CORREZIONE ANOMALIE)
                        # =======================================================
                        if pronostico_1 == pronostico_2:
                            # Se i numeri sono uguali (es. 45 - 45), applichiamo la chiusura diametrale
                            if pronostico_1 <= 45:
                                pronostico_2 = pronostico_1 + 45
                            else:
                                pronostico_2 = pronostico_1 - 45
                        # =======================================================

                        # Costruzione della card per la Dashboard
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

        # Ordinamento delle card per dare priorità agli Score più alti (180%)
        risultati[etichetta_colpo] = sorted(
            risultati[etichetta_colpo], 
            key=lambda x: x['score'], 
            reverse=True
        )[:9] # Limitiamo a un massimo di 9 card per pannello per mantenere la dashboard pulita

    # 3. Scrittura del file dei risultati per la dashboard web
    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    
    print("Sviluppo V5 completato: file risultati_v4.json generato con successo con Filtro Diametrale attivo.")

# Esecuzione dello script
if __name__ == "__main__":
    genera_risultati()
