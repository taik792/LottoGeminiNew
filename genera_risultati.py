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
    """Restituisce l'indice dell'esagono (da 1 a 15) a cui appartiene il numero."""
    resto = numero % 15
    return 15 if resto == 0 else resto

def esegui_elaborazione_motore():
    print("=== AVVIO MOTORE GEOMETRICO: ESAGONI SENZA DUPLICATI ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    # 1. Pulizia totale e normalizzazione dei nomi delle ruote (Niente più "BARI" e "Bari" separati)
    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        # Saltiamo le chiavi di servizio dell'estrazione
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        # Rendiamo standard il nome: prima lettera maiuscola, il resto minuscolo
        nome_standard = chiave.strip().capitalize()
        if nome_standard == "Nazionale":
            nome_standard = "Nazionale"

        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                # Prendiamo solo i 5 numeri reali convertiti in interi
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    # 2. Assegnazione RIGIDA e UNIVOCA dei colori (Evita rotture sul front-end)
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    
    mappa_calore = {}
    elenco_ruote = sorted(list(ruote_pulite.keys()))
    
    for r in elenco_ruote:
        if r in ruote_rosse:
            mappa_calore[r] = "rossa"
        elif r in ruote_grigie:
            mappa_calore[r] = "grigia"
        else:
            mappa_calore[r] = "gialla"

    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 3. Analisi ciclometrica pura sulle posizioni isotope
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            estratti_r1 = ruote_pulite[r1]
            estratti_r2 = ruote_pulite[r2]

            for p in range(5):
                n1 = estratti_r1[p]
                n2 = estratti_r2[p]

                # Rileviamo se fanno parte della stessa spina esagonale
                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    # Calcolo base della chiusura armonica (Diametrale del primo elemento)
                    ambata = (n1 + 45) % 90 or 90
                    
                    # Calcolo dinamico dell'abbinamento (Passo geometrico protetto da duplicati)
                    passi_esagono = [15, 30, 60, 75]
                    abbinamento = None
                    
                    for passo in passi_esagono:
                        candidato = (n2 + passo) % 90 or 90
                        # Il numero candidato NON deve essere uguale a n1, n2 o all'ambata stessa!
                        if candidato not in [n1, n2, ambata]:
                            abbinamento = candidato
                            break
                    
                    # Se non si trova un passo libero (rarissimo), usiamo il diametrale di n2
                    if not abbinamento:
                        abbinamento = (n2 + 45) % 90 or 90

                    previsione = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [ambata, abbinamento],
                        "score": f"{180 if dist == 15 else 172 if dist == 30 else 164}%",
                        "colore_r1": mappa_calore[r1],
                        "colore_r2": mappa_calore[r2]
                    }

                    # Smistamento nei tabelloni corretti a seconda della distanza ciclometrica rilevata
                    if dist == 15:
                        tabellone_nuovi.append(previsione)
                    elif dist == 30:
                        tabellone_colpo2.append(previsione)
                    elif dist == 45:
                        tabellone_colpo3.append(previsione)

    # 4. Copertura di sicurezza se l'estrazione non contiene armonie esagonali isotope pure
    if not tabellone_nuovi:
        tabellone_nuovi = tabellone_colpo2[:3] if tabellone_colpo2 else []
    if not tabellone_colpo2:
        tabellone_colpo2 = tabellone_nuovi[1:4] if len(tabellone_nuovi) > 1 else tabellone_nuovi
    if not tabellone_colpo3:
        tabellone_colpo3 = tabellone_nuovi[2:5] if len(tabellone_nuovi) > 2 else tabellone_nuovi

    # Costruzione dell'output finale pulito
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6],
            "colpo2": tabellone_colpo2[:6],
            "colpo3": tabellone_colpo3[:6]
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("Salvataggio completato. Struttura dati rigenerata e corretta!")

if __name__ == "__main__":
    esegui_elaborazione_motore()
