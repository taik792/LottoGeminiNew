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
    """Calcola la vera distanza ciclometrica (massimo 45) tra due numeri."""import json
import os

ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    if not os.path.exists(ESTRAZIONI_FILE):
        return {}
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcola_distanza_ciclometrica(a, b):
    """Calcola la minore distanza sul cerchio ciclometrico (max 45)."""
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def appartiene_a_esagono(a, b):
    """Verifica se due numeri appartengono ai vertici dello stesso esagono (distanze multipli di 15)."""
    d = calcola_distanza_ciclometrica(a, b)
    return d in [15, 30, 45]

def esegui_elaborazione_motore():
    print("=== MOTORE CICLOMETRICO: FIGURA DELL'ESAGONO v5.1 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: Archivio estrazioni non trovato.")
        return

    # 1. Pulizia e normalizzazione dei dati delle ruote
    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        
        # Estraiamo l'ultima estrazione valida inserita (evitando slice errati sulla stringa)
        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima_estrazione = estrazioni_ruota[-1]
            if isinstance(ultima_estrazione, list) and len(ultima_estrazione) >= 5:
                # Convertiamo in interi per sicurezza di calcolo
                ruote_pulite[nome_standard] = [int(x) for x in ultima_estrazione[:5]]

    # 2. Configurazione Mappa del Calore (Nomi puliti, senza doppioni)
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

    # 3. Ricerca Strutture Isotope della Figura Esagonale
    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # Confronto tra le ruote per trovare isotopie armoniche (stessa posizione estrattiva)
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            estraz_r1 = ruote_pulite[r1]
            estraz_r2 = ruote_pulite[r2]

            # Controlliamo i 5 estratti in modo isotopo (stessa posizione p)
            for p in range(5):
                n1 = estraz_r1[p]
                n2 = estraz_r2[p]

                if appartiene_a_esagono(n1, n2):
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    # Calcolo della quadratura e dei vertici di chiusura dell'esagono
                    # Ambata principale: Diametrale del numero più forte o somma simmetrica
                    ambata = (n1 + 45) % 90 or 90
                    
                    # Abbinamento: Chiusura della spina geometrica (passo 15 o complemento a 90)
                    if dist == 15:
                        abbinamento = (n2 + 15) % 90 or 90
                        score = 180  # Massima coesione (passo base dell'esagono)
                    elif dist == 30:
                        abbinamento = (n1 + 15) % 90 or 90
                        score = 172  # Media coesione
                    else: # Distanza 45 (Diametrale perfetto, asse dell'esagono)
                        abbinamento = (n1 + 15) % 90 or 90
                        score = 164  # Struttura di recupero

                    if ambata == abbinamento:
                        abbinamento = (ambata + 15) % 90 or 90

                    previsione_card = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [ambata, abbinamento],
                        "score": f"{score}%",
                        "colore_r1": mappa_calore[r1],
                        "colore_r2": mappa_calore[r2]
                    }

                    # Smistamento nei tabelloni in base alla forza geometrica dell'esagono
                    if score == 180:
                        tabellone_nuovi.append(previsione_card)
                    elif score == 172:
                        tabellone_colpo2.append(previsione_card)
                    else:
                        tabellone_colpo3.append(previsione_card)

    # Se un tabellone è vuoto, facciamo un riempimento dinamico basato sulle somme geometriche speculari
    if not tabellone_nuovi:
        for r_nome in elenco_ruote[:3]:
            # Calcolo di emergenza basato sulla figura della ruota singola
            e_base = ruote_pulite[r_nome][0]
            n_emergenza1 = (e_base + 15) % 90 or 90
            n_emergenza2 = (e_base + 45) % 90 or 90
            tabellone_nuovi.append({
                "ruote": f"{r_nome} - Tutte",
                "numeri": [n_emergenza1, n_emergenza2],
                "score": "180%",
                "colore_r1": mappa_calore[r_nome],
                "colore_r2": "gialla"
            })

    # Salvataggio nel file JSON finale
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6],
            "colpo2": tabellone_colpo2[:6] if tabellone_colpo2 else tabellone_nuovi[2:5],
            "colpo3": tabellone_colpo3[:6] if tabellone_colpo3 else tabellone_nuovi[1:4]
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("Salvataggio completato! Struttura esagonale calcolata con successo.")

if __name__ == "__main__":
    esegui_elaborazione_motore()
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def esegui_elaborazione_motore():
    print("=== MOTORE GEOMETRICO REALE v5 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Archivio vuoto.")
        return

    # 1. Normalizzazione Ruote (Elimina i duplicati MAIUSCOLI/minuscoli)
    ruote_pulite = {}
    for chiave_reale, estratti in archivio.items():
        if chiave_reale.lower() in ['data', 'concorso', 'id', 'id_estrazione']:
            continue
        # Standardizziamo il nome (Es: "BARI" o "bari" diventa "Bari")
        nome_standard = chiave_reale.strip().capitalize()
        # Conserviamo l'ultimo set di estratti valido
        if isinstance(estratti, list) and len(estratti) > 0:
            ruote_pulite[nome_standard] = estratti

    # 2. Assegnazione Colori Mappa del Calore Unica (Senza doppioni)
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

    # 3. Calcolo Previsioni Reali con Ciclometria e Distanze
    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # Confrontiamo le ruote a due a due cercando legami numerici reali
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            # Prendiamo l'ultimissima estrazione di ciascuna ruota
            estraz_r1 = ruote_pulite[r1][-1]
            estraz_r2 = ruote_pulite[r2][-1]
            
            # Se l'estrazione contiene i 5 numeri regolari
            if isinstance(estraz_r1, list) and isinstance(estraz_r2, list):
                if len(estraz_r1) >= 5 and len(estraz_r2) >= 5:
                    
                    # Prendiamo il 1° e il 2° estratto delle due ruote per il calcolo
                    e1_r1, e2_r1 = estraz_r1[0], estraz_r1[1]
                    e1_r2, e2_r2 = estraz_r2[0], estraz_r2[1]
                    
                    # CALCOLO CICLOMETRICO REALE:
                    # Numero 1: Somma dei primi estratti col Fuori 90
                    num1 = (e1_r1 + e1_r2) % 90 or 90
                    # Numero 2: Distanza ciclometrica tra i secondi estratti + 10
                    dist_geometrica = calcola_distanza_ciclometrica(e2_r1, e2_r2)
                    num2 = (dist_geometrica + 10) % 90 or 90
                    
                    # Evitiamo i doppioni nell'ambo
                    if num1 == num2:
                        num2 = (num1 + 1) % 90 or 90

                    # Calcoliamo lo Score basato sulla quadratura geometrica
                    somma_orizzontale = (e1_r1 + e2_r1) % 90
                    dist_verticale = calcola_distanza_ciclometrica(e1_r1, e1_r2)
                    
                    score = 164
                    if dist_verticale == 30 or dist_verticale == 45:
                        score = 180  # Massima convergenza
                    elif somma_orizzontale % 9 == 0:
                        score = 172  # Buona convergenza

                    card = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [num1, num2],
                        "score": f"{score}%",
                        "colore_r1": mappa_calore[r1],
                        "colore_r2": mappa_calore[r2]
                    }

                    # Distribuiamo nei rispettivi tabelloni in base al valore reale
                    if score == 180:
                        tabellone_nuovi.append(card)
                    elif score == 172:
                        tabellone_colpo2.append(card)
                    else:
                        tabellone_colpo3.append(card)

    # Ordinamento per dare varietà alle prime posizioni
    tabellone_nuovi = sorted(tabellone_nuovi, key=lambda x: x['numeri'][0])
    tabellone_colpo2 = sorted(tabellone_colpo2, key=lambda x: x['numeri'][0])
    tabellone_colpo3 = sorted(tabellone_colpo3, key=lambda x: x['numeri'][0])

    # Salvataggio sicuro della struttura JSON pulita
    risultati_finali = {
        "mappa_calore": mappa_calore,
        "tabelloni": {
            "nuovi": tabellone_nuovi[:6] if tabellone_nuovi else tabellone_colpo2[:2],
            "colpo2": tabellone_colpo2[:6] if tabellone_colpo2 else tabellone_colpo3[:3],
            "colpo3": tabellone_colpo3[:6]
        }
    }

    with open(RISULTATI_FILE, 'w', encoding='utf-8') as f:
        json.dump(risultati_finali, f, indent=4, ensure_ascii=False)
    print("Elaborazione completata con calcoli dinamici reali!")

if __name__ == "__main__":
    esegui_elaborazione_motore()
