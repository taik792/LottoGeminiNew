import json
import os

def calcola_distanza(n1, n2):
    """Calcola la distanza ciclometrica (max 45)"""
    dist = abs(n1 - n2)
    if dist > 45:
        dist = 90 - dist
    return dist

def estrai_ultimi_numeri(archivio, ruota1, ruota2, limite=5):
    """Estrae una lista di tutti i numeri usciti nelle ultime X estrazioni sulle due ruote"""
    numeri_recenti = set()
    for ruota in [ruota1, ruota2]:
        if ruota in archivio:
            # Prende le ultime 'limite' estrazioni disponibili nell'archivio
            ultime_estrazioni = archivio[ruota][-limite:]
            for estrazione in ultime_estrazioni:
                if isinstance(estrazione, list):
                    for num in estrazione:
                        numeri_recenti.add(int(num))
    return numeri_recenti

def trova_compagno_sincrono(base_num, numeri_esclusi):
    """Trova un compagno d'ambo che non sia uscito di recente, mantenendo la logica di cadenza"""
    candidato = base_num
    # Se il candidato teorico è uscito da poco, ci spostiamo di +10 (stessa cadenza) finché non ne troviamo uno libero
    for _ in range(9):
        if candidato not in numeri_esclusi:
            return candidato
        candidato = (candidato + 10) % 90
        if candidato == 0: candidato = 90
    return base_num  # Ritorna il base se non trova alternative (salvagente)

def genera_risultati():
    if not os.path.exists('estrazioni.json'):
        print("Errore: file estrazioni.json non trovato.")
        return

    with open('estrazioni.json', 'r', encoding='utf-8') as f:
        archivio = json.load(f)

    ruote_elenco = ["Bari", "Cagliari", "Firenze", "Genova", "Milano", "Napoli", "Palermo", "Roma", "Torino", "Venezia"]
    
    if "Bari" not in archivio or not isinstance(archivio["Bari"], list) or len(archivio["Bari"]) < 5:
        print("Errore: Struttura dati non conforme o estrazioni insufficienti.")
        return

    num_estrazioni = len(archivio["Bari"])
    print(f"Rilevate {num_estrazioni} estrazioni storiche.")

    risultati = {
        "nuove": [],
        "colpo2": [],
        "colpo3": [],
        "mappa_colore": {}
    }

    conteggio_ruote = {r: 0 for r in ruote_elenco}
    mappa_colpi = {"nuove": -1, "colpo2": -2, "colpo3": -3}

    for etichetta_colpo, indice_storico in mappa_colpi.items():
        for i in range(len(ruote_elenco)):
            for j in range(i + 1, len(ruote_elenco)):
                ruota1 = ruote_elenco[i]
                ruota2 = ruote_elenco[j]

                if ruota1 not in archivio or ruota2 not in archivio:
                    continue

                try:
                    num_r1 = archivio[ruota1][indice_storico]
                    num_r2 = archivio[ruota2][indice_storico]
                except IndexError:
                    continue

                if not isinstance(num_r1, list) or not isinstance(num_r2, list) or len(num_r1) < 5 or len(num_r2) < 5:
                    continue

                # Generiamo la lista nera dei numeri usciti nelle ultime 5 estrazioni su queste due ruote
                numeri_da_escludere = estrai_ultimi_numeri(archivio, ruota1, ruota2, limite=5)

                for pos in range(5):
                    try:
                        n1 = int(num_r1[pos])
                        n2 = int(num_r2[pos])
                    except (ValueError, IndexError):
                        continue

                    dist = calcola_distanza(n1, n2)

                    if dist in [45, 30, 15]:
                        score = 172
                        if dist == 45:
                            score = 180

                        pronostico_1 = (n1 + 30) % 90
                        if pronostico_1 == 0: pronostico_1 = 90
                        
                        # Calcoliamo il secondo numero teorico
                        teorico_2 = (n2 + 30) % 90
                        if teorico_2 == 0: teorico_2 = 90

                        # Applichiamo il filtro anti-ripetizione sul secondo numero
                        pronostico_2 = trova_compagno_sincrono(teorico_2, numeri_da_escludere)

                        # Controllo di sicurezza se i due numeri coincidono
                        filtro_attivo = False
                        if pronostico_1 == pronostico_2:
                            filtro_attivo = True
                            if pronostico_1 <= 45:
                                pronostico_2 = pronostico_1 + 45
                            else:
                                pronostico_2 = pronostico_1 - 45

                        if etichetta_colpo == "nuove":
                            conteggio_ruote[ruota1] += 1
                            conteggio_ruote[ruota2] += 1

                        card = {
                            "ruota1": ruota1,
                            "ruota2": ruota2,
                            "num1": pronostico_1,
                            "num2": pronostico_2,
                            "score": score,
                            "filtro_budget": filtro_attivo,
                            "dati_r1": " . ".join(map(str, num_r1)),
                            "dati_r2": " . ".join(map(str, num_r2))
                        }
                        risultati[etichetta_colpo].append(card)

        risultati[etichetta_colpo] = sorted(risultati[etichetta_colpo], key=lambda x: x['score'], reverse=True)[:9]

    for ruota, colpi in conteggio_ruote.items():
        if colpi == 0: risultati["mappa_colore"][ruota] = "calore-basso"
        elif colpi <= 2: risultati["mappa_colore"][ruota] = "calore-medio"
        else: risultati["mappa_colore"][ruota] = "calore-alto"

    with open('risultati_v4.json', 'w', encoding='utf-8') as f:
        json.dump(risultati, f, ensure_ascii=False, indent=4)
    print("Elaborazione completata con filtro sincronismo attivo.")

if __name__ == "__main__":
    genera_risultati()
