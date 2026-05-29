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

def esegui_elaborazione_motore():
    print("=== AVVIO MOTORE GEOMETRICO STRUTTURALE v6.0 ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    # 1. Normalizzazione e lettura estratti reali
    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()
        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    # Mappa calore fissa richiesta
    ruote_rosse = ["Palermo", "Roma", "Torino"]
    ruote_grigie = ["Milano"]
    mappa_calore = {r: "rossa" if r in ruote_rosse else "grigia" if r in ruote_grigie else "gialla" for r in ruote_pulite}

    elenco_ruote = sorted(list(ruote_pulite.keys()))
    
    # Dizionari di appoggio per evitare doppioni di ambi invertiti tra ruote speculari
    previsioni_generate = {}

    # 2. Calcolo a Quadratura Ciclometrica Perfetta
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            for p in range(5):
                n1 = ruote_pulite[r1][p]
                n2 = ruote_pulite[r2][p]

                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    # Calcolo basato sulla Somma Comune (Principio di Chiusura Ciclometrica)
                    somma_isotopa = (n1 + n2) % 90 or 90
                    
                    # L'ambata è il punto di equilibrio (Diametrale della Somma)
                    ambata = (somma_isotopa + 45) % 90 or 90
                    
                    # L'abbinamento chiude la tripletta dell'esagono sul cerchio a 90 numeri
                    if dist == 15:
                        abbinamento = (max(n1, n2) + 15) % 90 or 90
                    elif dist == 30:
                        abbinamento = (min(n1, n2) + 15) % 90 or 90
                    else:
                        abbinamento = (ambata + 15) % 90 or 90

                    # Controllo di sicurezza matematico anti-collasso
                    if ambata == abbinamento or ambata in [n1, n2] or abbinamento in [n1, n2]:
                        ambata = (n1 + 45) % 90 or 90
                        abbinamento = (n2 + 45) % 90 or 90
                    
                    if ambata == abbinamento:
                        abbinamento = (ambata + 15) % 90 or 90

                    # Ordiniamo i numeri per l'output grafico coerente
                    numeri_gioco = sorted([ambata, abbinamento])
                    chiave_ambo = f"{numeri_gioco[0]}-{numeri_gioco[1]}"

                    # Assegnazione del tabellone in base alla distanza originaria
                    tipo_tabellone = "nuovi" if dist == 15 else "colpo2" if dist == 30 else "colpo3"
                    score = "180%" if dist == 15 else "172%" if dist == 30 else "164%"

                    # Se l'ambo è già stato calcolato da un'altra coppia di ruote, fondiamo le ruote!
                    if chiave_ambo in previsioni_generate:
                        # Evitiamo di riscrivere se è lo stesso asse
                        if r1 not in previsioni_generate[chiave_ambo]["ruote"]:
                            previsioni_generate[chiave_ambo]["ruote"] += f", {r1}"
                    else:
                        previsioni_generate[chiave_ambo] = {
                            "ruote": f"{r1} - {r2}",
                            "numeri": numeri_gioco,
                            "score": score,
                            "colore_r1": mappa_calore[r1],
                            "colore_r2": mappa_calore[r2],
                            "tipo": tipo_tabellone
                        }

    # 3. Smistamento nei rispettivi tabelloni finali senza duplicati visivi
    tabellone_nuovi = []
    tabellone_colpo2 = []
    tabellone_colpo3 = []

    for pred in previsioni_generate.values():
        struttura = {
            "ruote": pred["ruote"],
            "numeri": pred["numeri"],
            "score": pred["score"],
            "colore_r1": pred["colore_r1"],
            "colore_r2": pred["colore_r2"]
        }
        if pred["tipo"] == "nuovi":
            tabellone_nuovi.append(struttura)
        elif pred["tipo"] == "colpo2":
            tabellone_colpo2.append(struttura)
        elif pred["tipo"] == "colpo3":
            tabellone_colpo3.append(struttura)

    # 4. Fallback di emergenza protetti (Se un tabellone è vuoto)
    if not tabellone_nuovi:
        tabellone_nuovi = [{"ruote": "Nessuna Struttura", "numeri": [15, 60], "score": "180%", "colore_r1": "gialla", "colore_r2": "gialla"}]
    if not tabellone_colpo2:
        tabellone_colpo2 = [{"ruote": "Nessuna Struttura", "numeri": [30, 75], "score": "172%", "colore_r1": "gialla", "colore_r2": "gialla"}]
    if not tabellone_colpo3:
        tabellone_colpo3 = [{"ruote": "Nessuna Struttura", "numeri": [45, 90], "score": "164%", "colore_r1": "gialla", "colore_r2": "gialla"}]

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
    print("=== MOTORE FINALE STRUTTURALE AGGIORNATO CON SUCCESSO ===")

if __name__ == "__main__":
    esegui_elaborazione_motore()
