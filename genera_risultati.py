import json
import os

# Configurazione percorsi file
ESTRAZIONI_FILE = 'estrazioni.json'
RISULTATI_FILE = 'risultati_v4.json'

def carica_dati_estrazioni():
    """Carica l'archivio storico dal file JSON."""
    if not os.path.exists(ESTRAZIONI_FILE):
        print(f"Errore: Il file {ESTRAZIONI_FILE} non esiste.")
        return []
    with open(ESTRAZIONI_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def analizza_stato_forma(archivio, profondita=15):
    """
    Analizza le ultime estrazioni inserite (le più recenti in fondo al file JSON)
    per determinare quanti estratti attivi ha ogni numero su ciascuna ruota.
    """
    stato_forma = {}
    # Estrae gli ultimi concorsi (quelli più giovani alla fine della lista)
    estrazioni_recenti = archivio[-profondita:]
    
    for estrazione in estrazioni_recenti:
        for ruota, numeri in estrazione.items():
            # Esclude chiavi di servizio o metadati
            if ruota in ['data', 'concorso', 'id', 'Data', 'ID']:
                continue
            if ruota not in stato_forma:
                stato_forma[ruota] = {n: 0 for n in range(1, 91)}
            
            for n in numeri:
                if isinstance(n, int) and 1 <= n <= 90:
                    stato_forma[ruota][n] += 1
    return stato_forma

def esegui_elaborazione_motore():
    print("====================================================")
    print(" INIZIO ELABORAZIONE MOTORE GEOMETRICO ELITE PRO v5")
    print("====================================================")
    
    # 1. Caricamento database cronologico (dal vecchio al giovane)
    dati_estrazioni = carica_dati_estrazioni()
    if not dati_estrazioni:
        print("Impossibile procedere: archivio estrazioni vuoto o mancante.")
        return
        
    print(f"Archivio caricato con successo. Rilevati {len(dati_estrazioni)} concorsi storici.")

    # 2. Estrazione dello stato di forma recente (ultimi 15 colpi)
    stato_forma = analizza_stato_forma(dati_estrazioni, profondita=15)

    # 3. Identificazione dell'ultimo concorso reale inserito (in fondo alla lista)
    ultima_estrazione = dati_estrazioni[-1]
    ruote_effettive = [r for r in ultima_estrazione.keys() if r not in ['data', 'concorso', 'id', 'Data', 'ID']]
    
    # 4. Definizione della Mappa del Calore secondo le tue direttive colori
    # Ruote Rosse (Tensione Massima) e Ruote Gialle (Calore Standard)
    ruote_tensione_rossa = ["Firenze", "Roma", "Torino", "Napoli"]
    mappa_calore = {}
    
    for ruota in ruote_effettive:
        if ruota in ruote_tensione_rossa:
            mappa_calore[ruota] = "rossa"
        else:
            mappa_calore[ruota] = "gialla"  # Milano e le restanti sono gialle (nessuna ruota blu)

    # Contenitori per i tre tabelloni della Dashboard web
    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    # 5. Doppi cicli FOR per il calcolo delle distanze e convergenze geometriche pure
    for i in range(len(ruote_effettive)):
        for j in range(i + 1, len(ruote_effettive)):
            ruota1 = ruote_effettive[i]
            ruota2 = ruote_effettive[j]
            
            # Algoritmo di calcolo delle combinazioni basato sui passati estratti
            estratti_r1 = ultima_estrazione[ruota1]
            estratti_r2 = ultima_estrazione[ruota2]
            
            if len(estratti_r1) >= 2 and len(estratti_r2) >= 2:
                # Esempio di elaborazione distanze matematiche applicate al lotto
                num1 = (estratti_r1[0] + 45) % 90 or 90
                num2 = (estratti_r2[1] + 15) % 90 or 90
                
                if num1 == num2:
                    num2 = (num1 + 45) % 90 or 90
                
                # Assegnazione dello score di base geometrico nativo (172% o 18ato a 180%)
                score_geometrico = 172
                if (num1 + num2) % 90 == 0 or abs(num1 - num2) == 45:
                    score_geometrico = 180
                
                # ---------------------------------------------------------------------
                # FILTRO STATO DI FORMA / FREQUENTI
                # ---------------------------------------------------------------------
                # Controlla se i numeri sono attivi o totalmente assenti nelle ruote scelte
                presenza_n1 = stato_forma.get(ruota1, {}).get(num1, 0)
                presenza_n2 = stato_forma.get(ruota2, {}).get(num2, 0)
                
                # Se entrambi i numeri sono totalmente freddi (0 uscite recenti),
                # il motore applica una penalizzazione di sicurezza (-8%) sullo score geometrico 
                # per evitare lo sfaldamento laterale (+1/-1) che causa perdite
                if presenza_n1 == 0 and presenza_n2 == 0:
                    score_finale = score_geometrico - 8
                else:
                    score_finale = score_geometrico
                # ---------------------------------------------------------------------

                # Creazione dell'oggetto Card per il sito web
                card_previsione = {
                    "ruote": f"{ruota1} - {ruota2}",
                    "numeri": [num1, num2],
                    "score": f"{score_finale}%",
                    "colore_r1": mappa_calore.get(ruota1, "gialla"),
                    "colore_r2": mappa_calore.get(ruota2, "gialla")
                }

                # Distribuzione automatica nei tabelloni in base al nuovo
