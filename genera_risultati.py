import json
import os

ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    if not os.path.exists(ESTRAZIONI_FILE):
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcola_distanza_ciclometrica(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def determina_esagono(numero):
    resto = numero % 15
    return 15 if resto == 0 else resto

def analizza_statistiche_ruote(archivio):
    """
    Analizza la cronologia per calcolare ritardi e frequenze recenti (ultimi 18 colpi).
    """
    stats = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        if not isinstance(estrazioni_ruota, list) or len(estrazioni_ruota) == 0:
            continue
            
        ritardi = {n: 0 for n in range(1, 91)}
        frequenza_recente = {n: 0 for n in range(1, 91)}
        
        ultime_18 = estrazioni_ruota[-18:] if len(estrazioni_ruota) >= 18 else estrazioni_ruota
        
        for estrazione in ultime_18:
            if isinstance(estrazione, list):
                for num in estrazione[:5]:
                    if 1 <= int(num) <= 90:
                        frequenza_recente[int(num)] += 1
                        
        for n in range(1, 91):
            ritardo = 0
            trovato = False
            for estrazione in reversed(estrazioni_ruota):
                if isinstance(estrazione, list) and n in [int(x) for x in estrazione[:5]]:
                    trovato = True
                    break
                ritardo += 1
            stats_val = ritardo if trovato else len(estrazioni_ruota)
            ritardi[n] = stats_val
            
        stats[nome_standard] = {
            "ritardi": ritardi,
            "frequenze_18": frequenza_recente
        }
    return stats

def calcola_peso_statistico(n, ruota, stats):
    """
    Assegna un punteggio di precisione al numero basato su ritardo ideale e ciclicità.
    """
    if ruota not in stats:
        return 50  
        
    ritardo = stats[ruota]["ritardi"].get(n, 0)
    freq = stats[ruota]["frequenze_18"].get(n, 0)
    
    punteggio = 50
    
    if freq == 1:
        punteggio += 15
    elif freq == 2:
        punteggio += 20
    elif freq == 0:  
        punteggio += 5
    else:            
        punteggio -= 10
        
    if 10 <= ritardo <= 36:
        punteggio += 25
    elif 1 <= ritardo <= 9: 
        punteggio -= 15
    elif ritardo > 54:      
        punteggio -= 10
        
    return punteggio

def esegui_elaborazione_motore():
    print("=== AVVIO MOTORE GEOMETRICO-STATISTICO v8.0 DINAMICO ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    statistiche_ruote = analizza_statistiche_ruote(archivio)

    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    elenco_ruote = sorted(list(ruote_pulite.keys()))
    previsioni_generate = {}

    # Dizionario d'appoggio temporaneo per contare la presenza reale delle ruote nelle previsioni
    conteggio_presenze_ruote = {r: 0 for r in ruote_pulite}

    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            for p in range(5):
                n1 = ruote_pulite[r1][p]
                n2 = ruote_pulite[r2][p]

                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    somma_isotopa = (n1 + n2) % 90 or 90
                    
                    ambata = (somma_isotopa + 45) % 90 or 90
                    
                    peso_n1 = calcola_peso_statistico(n1, r1, statistiche_ruote)
                    peso_n2 = calcola_peso_statistico(n2, r2, statistiche_ruote)
                    
                    passo_dinamico = 30 if peso_n1 >= peso_n2 else 60
                    abbinamento = (ambata + passo_dinamico) % 90 or 90

                    if ambata == abbinamento or ambata in [n1, n2] or abbinamento in [n1, n2]:
                        ambata = (n1 + 45) % 90 or 90
                        abbinamento = (n2 + 45) % 90 or 90
                    
                    if ambata == abbinamento:
                        abbinamento = (ambata + 15) % 90 or 90

                    numeri_gioco = sorted([ambata, abbinamento])
                    chiave_ambo = f"{numeri_gioco[0]}-{numeri_gioco[1]}"

                    peso_r1 = calcola_peso_statistico(numeri_gioco[0], r1, statistiche_ruote) + calcola_peso_statistico(numeri_gioco[1], r1, statistiche_ruote)
                    peso_r2 = calcola_peso_statistico(numeri_gioco[0], r2, statistiche_ruote) + calcola_peso_statistico(numeri_gioco[1], r2, statistiche_ruote)
                    media_peso = (peso_r1 + peso_r2) / 4

                    base_score = 140 if dist == 15 else 130 if dist == 30 else 120
                    score_finale_numerico = int(base_score + (media_peso * 0.4))
                    
                    if score_finale_numerico > 195: score_finale_numerico = 195
                    str_score = f"{score_finale_numerico}%"

                    tipo_tabellone = "nuovi" if dist == 15 else "colpo2" if dist == 30 else "colpo3"

                    if chiave_ambo in previsioni_generate:
                        if r1 not in previsioni_generate[chiave_ambo]["ruote"]:
                            previsioni_generate[chiave_ambo]["ruote"] += f", {r1}"
                            vecchio_score = int(previsioni_generate[chiave_ambo]["score"].replace("%", ""))
                            previsioni_generate[chiave_ambo]["score"] = f"{min(vecchio_score + 5, 198)}%"
                    else:
                        previsioni_generate[chiave_ambo] = {
                            "ruote": f"{r1} - {r2}",
                            "numeri": numeri_gioco,
                            "score": str_score,
                            "colore_r1": "gialla", # Sarà sovrascritto dopo dinamicamente
                            "colore_r2": "gialla", # Sarà sovrascritto dopo dinamicamente
                            "tipo": tipo_tabellone,
                            "valore_ordinamento": score_finale_numerico,
                            "lista_ruote_coinvolte": [r1, r2]
                        }

    # --- CALCOLO DELLA MAPPA DEL CALORE DINAMICA ---
    # Contiamo quante volte ogni ruota compare nelle previsioni effettive
    for pred in previsioni_generate.values():
        # Estraiamo i nomi puliti delle ruote (gestendo anche le stringhe aggregate con virgole)
        ruote_stringa = pred["ruote"].replace(" - ", ", ")
        singole_ruote = [r.strip() for r in ruote_stringa.split(",")]
        for r in singole_ruote:
            if r in conteggio_presenze_ruote:
                conteggio_presenze_ruote[r] += 1

    # Stabiliamo le soglie dinamiche basandoci sulle presenze massime rilevate
    valori_presenze = conteggio_presenze_ruote.values()
    max_presenze = max(valori_presenze) if valori_presenze else 0

    mappa_calore = {}
    for r, count in conteggio_presenze_ruote.items():
        if count == 0:
            mappa_calore[r] = "grigia" # Nessuna previsione trovata su questa ruota
        elif count >= max(2, int(max_presenze * 0.6)):
            mappa_calore[r] = "rossa"  # Alta concentrazione geometrica (Perno)
        else:
            mappa_calore[r] = "gialla" # Presenza normale o isolata

    # Aggiorniamo i colori interni delle schede basandoci sulla mappa dinamica appena calcolata
    for pred in previsioni_generate.values():
        ruote_stringa = pred["ruote"].replace(" - ", ", ")
        singole_ruote = [r.strip() for r in ruote_stringa.split(",")]
        pred["colore_r1"] =
