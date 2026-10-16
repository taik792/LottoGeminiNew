import json
import os

def calcola_distanza_ciclometrica(a, b):
    dist = abs(a - b)
    return dist if dist <= 45 else 90 - dist

def fuori_90(numero):
    while numero > 90:
        numero -= 90
    while numero <= 0:
        numero += 90
    return numero

def genera_previsione_laboratorio():
    nome_file_json = 'estrazioni.json'
    nome_file_report_json = 'risultati_v4.json'

    if not os.path.exists(nome_file_json):
        print(f"[ERRORE] File {nome_file_json} non trovato!")
        return

    with open(nome_file_json, 'r', encoding='utf-8') as f:
        dati = json.load(f)
    
    try:
        # Estraiamo la lista globale delle cinquine di Bari
        ruota_bari = dati['Bari']
    except KeyError:
        print("[ERRORE] Chiave 'Bari' non trovata nel JSON.")
        return

    tot_estrazioni = len(ruota_bari)
    if tot_estrazioni < 5:
        print("[ERRORE] Dati storici insufficienti per il backtesting.")
        return

    # --- SEZIONE BACKTESTING STORICO ---
    storico_esiti = []
    vinte_ambata = 0
    vinte_ambo = 0
    tot_casi_testati = 0

    # Analizziamo la storia fermandoci a 3 estrazioni dalla fine per dare il tempo di verifica dei colpi
    # Il ciclo parte dal terzo elemento disponibile per poter calcolare la distanza ciclometrica
    for i in range(2, tot_estrazioni):
        # 1. Recupero dati per il calcolo del fisso
        cinquina_prec = ruota_bari[i-1]
        cinquina_att = ruota_bari[i]
        
        primo_prec = int(cinquina_prec[0])
        primo_att = int(cinquina_att[0])
        
        # 2. Calcolo Fisso e Previsione del passato
        fisso = calcola_distanza_ciclometrica(primo_att, primo_prec)
        if fisso == 0 or fisso == 90: fisso = 40
        
        ambata_storica = fuori_90(primo_att + fisso)
        ambo1 = fuori_90(ambata_storica + 45)
        ambo2 = fuori_90(90 - ambata_storica)
        ambo3 = fuori_90(91 - ambata_storica)
        abbinamenti = [ambo1, ambo2, ambo3]
        for idx in range(3):
            if abbinamenti[idx] == ambata_storica:
                abbinamenti[idx] = fuori_90(abbinamenti[idx] + 1)
        
        # 3. Verifica esito nei 3 colpi successivi
        esito = "In Corso / Perdente"
        colpo_uscita = "-"
        
        # Controlliamo i 3 concorsi successivi all'elaborazione (i+1, i+2, i+3)
        for colpo in range(1, 4):
            if (i + colpo) < tot_estrazioni:
                cinquina_verifica = ruota_bari[i + colpo]
                cinquina_int = [int(n) for n in cinquina_verifica]
                
                # Verifica Ambo Secco
                ambo_centrato = False
                for abb in abbinamenti:
                    if ambata_storica in cinquina_int and abb in cinquina_int:
                        ambo_centrato = True
                        break
                
                if ambo_centrato:
                    esito = "VINCITA AMBO"
                    colpo_uscita = f"{colpo}° Colpo"
                    if colpo <= 3: vinte_ambo += 1
                    break
                # Verifica Ambata
                elif ambata_storica in cinquina_int:
                    esito = "VINCITA AMBATA"
                    colpo_uscita = f"{colpo}° Colpo"
                    if colpo <= 3: vinte_ambata += 1
                    break
        
        # Registriamo il caso solo se ha completato i colpi o se ha vinto prima
        if (i + 3) < tot_estrazioni or esito != "In Corso / Perdente":
            tot_casi_testati += 1
            storico_esiti.append({
                "id": i,
                "fisso": fisso,
                "ambata": ambata_storica,
                "esito": esito,
                "colpo": colpo_uscita
            })

    # --- CALCOLO PREVISIONE FUTURA REALE ---
    c_precedente = ruota_bari[-2]
    c_attuale = ruota_bari[-1]
    p_precedente = int(c_precedente[0])
    p_attuale = int(c_attuale[0])

    fisso_dinamico = calcola_distanza_ciclometrica(p_attuale, p_precedente)
    if fisso_dinamico == 0 or fisso_dinamico == 90: fisso_dinamico = 40

    ambata = fuori_90(p_attuale + fisso_dinamico)
    a1 = fuori_90(ambata + 45)
    a2 = fuori_90(90 - ambata)
    a3 = fuori_90(91 - ambata)
    abb_futuri = [a1, a2, a3]
    for idx in range(3):
        if abb_futuri[idx] == ambata: abb_futuri[idx] = fuori_90(abb_futuri[idx] + 1)

    percentuale_successo = 0
    if tot_casi_testati > 0:
        percentuale_successo = round(((vinte_ambata + vinte_ambo) / tot_casi_testati) * 100, 2)

    # Output JSON Strutturato
    dati_output = {
        "ambiente": "LABORATORIO (PC) - BACKTESTING ATTIVO",
        "ruota_attiva": "BARI",
        "statistiche": {
            "casi_esaminati": tot_casi_testati,
            "vincite_ambata": vinte_ambata,
            "vincite_ambo": vinte_ambo,
            "efficacia_globale": f"{percentuale_successo}%"
        },
        "ultimo_calcolo": {
            "primo_precedente": p_precedente,
            "primo_attuale": p_attuale,
            "fisso_dinamico_applicato": fisso_dinamico
        },
        "previsione": {
            "tipo_giocata": "STUDIO / REALE (Verifica Storico)",
            "ambata_principale": ambata,
            "ambi_secchi": [f"{ambata}-{abb_futuri[0]}", f"{ambata}-{abb_futuri[1]}", f"{ambata}-{abb_futuri[2]}"]
        },
        "storico": list(reversed(storico_esiti))[:8] # Mostriamo gli ultimi 8 esiti passati
    }

    with open(nome_file_report_json, 'w', encoding='utf-8') as f_json:
        json.dump(dati_output, f_json, indent=4, ensure_ascii=False)
    print(f"[OK] Backtesting completato. Efficacia: {percentuale_successo}%")

if __name__ == "__main__":
    genera_previsione_laboratorio()
