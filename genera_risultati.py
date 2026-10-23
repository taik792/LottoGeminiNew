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

    # Il ciclo analizza la storia calcolando il fisso sulla cinquina corrente
    for i in range(2, tot_estrazioni):
        cinquina_att = ruota_bari[i]
        
        # NUOVA LOGICA OPZIONE 2: Somma Isocrona (1° + 5° Estratto) della cinquina attuale
        primo_att = int(cinquina_att[0])
        quinto_att = int(cinquina_att[4])
        
        fisso = fuori_90(primo_att + quinto_att)
        
        ambata_storica = fuori_90(primo_att + fisso)
        ambo1 = fuori_90(ambata_storica + 45)
        ambo2 = fuori_90(90 - ambata_storica)
        ambo3 = fuori_90(91 - ambata_storica)
        abbinamenti = [ambo1, ambo2, ambo3]
        for idx in range(3):
            if abbinamenti[idx] == ambata_storica:
                abbinamenti[idx] = fuori_90(abbinamenti[idx] + 1)
        
        esito = "In Corso / Perdente"
        colpo_uscita = "-"
        
        # Verifica nei 3 colpi successivi (i+1, i+2, i+3)
        for colpo in range(1, 4):
            if (i + colpo) < tot_estrazioni:
                cinquina_verifica = ruota_bari[i + colpo]
                cinquina_int = [int(n) for n in cinquina_verifica]
                
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
                elif ambata_storica in cinquina_int:
                    esito = "VINCITA AMBATA"
                    colpo_uscita = f"{colpo}° Colpo"
                    if colpo <= 3: vinte_ambata += 1
                    break
        
        if (i + 3) < tot_estrazioni or esito != "In Corso / Perdente":
            tot_casi_testati += 1
            storico_esiti.append({
                "id": i,
                "fisso": fisso,
                "ambata": ambata_storica,
                "esito": esito,
                "colpo": colpo_uscita
            })

    # --- CALCOLO PREVISIONE FUTURA REALE (APPLICATO ALL'ULTIMA ESTRAZIONE) ---
    c_attuale = ruota_bari[-1]
    p_attuale = int(c_attuale[0])
    q_attuale = int(c_attuale[4])

    # Calcolo Fisso Dinamico basato su Somma Isocrona
    fisso_dinamico = fuori_90(p_attuale + q_attuale)

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

    dati_output = {
        "ambiente": "LABORATORIO (PC) - STRATEGIA SOMMA ISOCRONA V1",
        "ruota_attiva": "BARI",
        "statistiche": {
            "casi_esaminati": tot_casi_testati,
            "vincite_ambata": vinte_ambata,
            "vincite_ambo": vinte_ambo,
            "efficacia_globale": f"{percentuale_successo}%"
        },
        "ultimo_calcolo": {
            "ultimo_primo_estratto": p_attuale,
            "ultimo_quinto_estratto": q_attuale,
            "fisso_dinamico_somma_isocrona": fisso_dinamico
        },
        "previsione": {
            "tipo_giocata": "STUDIO / REALE (Verifica Storico)",
            "ambata_principale": ambata,
            "ambi_secchi": [f"{ambata}-{abb_futuri[0]}", f"{ambata}-{abb_futuri[1]}", f"{ambata}-{abb_futuri[2]}"]
        },
        "storico": list(reversed(storico_esiti))[:8]
    }

    with open(nome_file_report_json, 'w', encoding='utf-8') as f_json:
        json.dump(dati_output, f_json, indent=4, ensure_ascii=False)
    print(f"[OK] Backtesting completato con Somma Isocrona. Efficacia: {percentuale_successo}%")

if __name__ == "__main__":
    genera_previsione_laboratorio()
