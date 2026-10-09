import json
import os

def brute_force_bari():
    file_estrazioni = "estrazioni.json"
    
    if not os.path.exists(file_estrazioni):
        print(f"❌ ERRORE: Non trovo '{file_estrazioni}'!")
        return
        
    with open(file_estrazioni, "r", encoding="utf-8") as f:
        archivio = json.load(f)
        
    chiave_bari = "Bari" if "Bari" in archivio else "BARI"
    if chiave_bari not in archivio:
        print("❌ ERRORE: Ruota Bari non trovata nel JSON!")
        return
        
    estrazioni_bari = archivio[chiave_bari]
    tot_estrazioni = len(estrazioni_bari)
    
    # Analizziamo gli ultimi 50 concorsi (lasciando gli ultimi 3 per verificare i colpi)
    range_analisi = 50
    start_index = max(0, tot_estrazioni - range_analisi - 3)
    end_index = tot_estrazioni - 3
    
    classifica_fissi = {}
    
    print(f"🔮 Elaborazione Brute-Force su {end_index - start_index} concorsi storici di BARI...")
    
    # Scansione brute-force da +1 a +90
    for fisso in range(1, 91):
        vincite = 0
        casi_testati = 0
        
        for i in range(start_index, end_index):
            casi_testati += 1
            # Calcolo ambata teorica sul 1° estratto del concorso i
            primo_estratto = estrazioni_bari[i][0]
            ambata = primo_estratto + fisso
            if ambata > 90: ambata -= 90
            
            # Controlliamo nei 3 colpi successivi (i+1, i+2, i+3) se è uscita l'ambata
            colpi_successivi = [
                estrazioni_bari[i+1],
                estrazioni_bari[i+2],
                estrazioni_bari[i+3]
            ]
            
            for cinquina in colpi_successivi:
                if ambata in cinquina:
                    vincite += 1
                    break # Esito vincente nel ciclo dei 3 colpi, passiamo oltre
                    
        percentuale = (vincite / casi_testati) * 100 if casi_testati > 0 else 0
        classifica_fissi[fisso] = (vincite, percentuale)
        
    # Ordiniamo la classifica per percentuale decrescente
    classifica_ordinata = sorted(classifica_fissi.items(), key=lambda item: item[1][1], reverse=True)
    
    print("\n" + "="*50)
    print("      🎯 CLASSIFICA TOP 3 FISSI OTTIMIZZATI - BARI     ")
    print("="*50)
    for rank, (fisso, dati) in enumerate(classifica_ordinata[:3], 1):
        print(f"{rank}° Posto -> FISSO +{fisso} | Vincite: {dati[0]}/50 casi | Successo: {dati[1]:.2f}%")
    print("="*50)
    
    print(f"\n👉 Scegli il fisso al 1° Posto per aggiornare la dashboard!")

if __name__ == "__main__":
    brute_force_bari()
