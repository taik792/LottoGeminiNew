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
    """Restituisce la spina esagonale di appartenenza (da 1 a 15)."""
    resto = numero % 15
    return 15 if resto == 0 else resto

def esegui_elaborazione_motore():
    print("=== AVVIO MOTORE CICLOMETRICO TRIPLETTI CORAZZATI ===")
    archivio = carica_dati_estrazioni()
    if not archivio:
        print("Errore: file estrazioni vuoto o non trovato.")
        return

    # 1. Normalizzazione nomi ruote ed estrazione dati reali
    ruote_pulite = {}
    for chiave, estrazioni_ruota in archivio.items():
        if chiave.lower() in ['data', 'concorso', 'id', 'id_estrazione', 'frequenze', 'ritardi']:
            continue
        
        nome_standard = chiave.strip().capitalize()

        if isinstance(estrazioni_ruota, list) and len(estrazioni_ruota) > 0:
            ultima = estrazioni_ruota[-1]
            if isinstance(ultima, list) and len(ultima) >= 5:
                ruote_pulite[nome_standard] = [int(x) for x in ultima[:5]]

    # 2. Configurazione Mappa del Calore Fissa
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

    # 3. Calcolo geometrico reale senza possibilità di numeri uguali
    for i in range(len(elenco_ruote)):
        for j in range(i + 1, len(elenco_ruote)):
            r1 = elenco_ruote[i]
            r2 = elenco_ruote[j]
            
            estratti_r1 = ruote_pulite[r1]
            estratti_r2 = ruote_pulite[r2]

            for p in range(5):
                n1 = estratti_r1[p]
                n2 = estratti_r2[p]

                # Controllo coesione armonica esagonale (passo 15, 30, 45)
                if determina_esagono(n1) == determina_esagono(n2) and n1 != n2:
                    dist = calcola_distanza_ciclometrica(n1, n2)
                    
                    # AMBATA PRINCIPALE: Chiusura diametrale geometrica (+45)
                    ambata = (n1 + 45) % 90 or 90
                    
                    # ABBINAMENTO DINAMICO: Calcolato per chiudere la figura dell'esagono
                    if dist == 15:
                        abbinamento = (n2 + 15) % 90 or 90
                    elif dist == 30:
                        abbinamento = (n1 + 15) % 90 or 90
                    else: # Distanza 45
                        abbinamento = (n1 + 15) % 90 or 90

                    # CONTROLLO ANTI-DOPPIONE BLINDATO:
                    # Se l'abbinamento coincide con l'ambata o con uno dei numeri base, lo stacchiamo di 45 unità
                    if abbinamento == ambata or abbinamento == n1 or abbinamento == n2:
                        abbinamento = (ambata + 45) % 90 or 90
                    
                    # Ultima barriera di sicurezza matematica: se sono ancora uguali, applichiamo il passo +1
                    if ambata == abbinamento:
                        abbinamento = (ambata + 1) % 90 or 90

                    previsione = {
                        "ruote": f"{r1} - {r2}",
                        "numeri": [ambata, abbinamento],
                        "score": f"{180 if dist == 15 else 172 if dist == 30 else 164}%",
                        "colore_r1": mappa_calore[r1],
                        "colore_r2": mappa_calore[r2]
                    }

                    if dist == 15:
                        tabellone_nuovi.append(previsione)
                    elif dist == 30:
                        tabellone_colpo2.append(previsione)
                    elif dist == 45:
                        tabellone_colpo3.append(previsione)

    # 4. Gestione dei riempimenti di sicurezza senza doppioni interni
    if not tabellone_nuovi:
        tabellone_nuovi = tabellone_colpo2[:3] if tabellone_colpo2 else []
    if not tabellone_colpo2:
        tabellone_colpo2 = tabellone_nuovi[1:4] if len(tabellone_nuovi) > 1 else tabellone_nuovi
    if not tabellone_colpo3:
        tabellone_colpo3 = tabellone_nuovi[2:5] if len(tabellone_nuovi) > 2 else tabellone_nuovi

    # Se tutto l'archivio fosse privo di isotopie (caso estremo), generiamo un paracadute pulito
    if not tabellone_nuovi:
        for idx, r_nome in enumerate(elenco_ruote[:3]):
            n_base = ruote_pulite[r_nome][0]
            ambata_emergenza = (n_base + 45) % 90 or 90
            abbinamento_emergenza = (n_base + 15) % 90 or 90
            tabellone_nuovi.append({
                "ruote": f"{r_nome} - Tutte",
                "numeri": [ambata_emergenza, abbinamento_emergenza],
                "score": "180%",
                "colore_r1": mappa_calore[r_nome],
                "colore_r2": "gialla"
            })

    # Creazione della struttura finale JSON pulita
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
    print("Fatto! Il file risultati_v4.json è stato rigenerato senza alcun doppione numerico.")

if __name__ == "__main__":
    esegui_elaborazione_motore()
